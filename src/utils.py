"""
Utilidades y funciones auxiliares
"""

import numpy as np
from typing import Tuple, List, Dict
import json


def normalize_signal(signal: np.ndarray, method: str = 'minmax') -> np.ndarray:
    """
    Normaliza una señal
    
    Args:
        signal: Señal a normalizar
        method: 'minmax' o 'zscore'
        
    Returns:
        Señal normalizada
    """
    if method == 'minmax':
        min_val = np.min(signal)
        max_val = np.max(signal)
        if max_val == min_val:
            return signal
        return (signal - min_val) / (max_val - min_val)
    
    elif method == 'zscore':
        mean = np.mean(signal)
        std = np.std(signal)
        if std == 0:
            return signal
        return (signal - mean) / std
    
    else:
        raise ValueError(f"Método desconocido: {method}")


def apply_window(signal: np.ndarray, window_type: str = 'hann') -> np.ndarray:
    """
    Aplica ventana a una señal
    
    Args:
        signal: Señal de entrada
        window_type: Tipo de ventana ('hann', 'hamming', 'blackman', 'tukey')
        
    Returns:
        Señal ventanada
    """
    n = len(signal)
    
    if window_type == 'hann':
        window = np.hanning(n)
    elif window_type == 'hamming':
        window = np.hamming(n)
    elif window_type == 'blackman':
        window = np.blackman(n)
    elif window_type == 'tukey':
        window = signal.tukey(n, alpha=0.5)
    else:
        raise ValueError(f"Tipo de ventana desconocido: {window_type}")
    
    return signal * window


def calculate_psd(signal: np.ndarray, fs: float) -> Tuple[np.ndarray, np.ndarray]:
    """
    Calcula la Densidad Espectral de Potencia
    
    Args:
        signal: Señal de entrada
        fs: Frecuencia de muestreo
        
    Returns:
        Tupla (frecuencias, PSD)
    """
    from scipy import signal as scipy_signal
    freqs, psd = scipy_signal.welch(signal, fs, nperseg=min(1024, len(signal)))
    return freqs, psd


def apply_bandpass_filter(signal: np.ndarray, fs: float, 
                         lowcut: float, highcut: float, 
                         order: int = 4) -> np.ndarray:
    """
    Aplica filtro paso banda
    
    Args:
        signal: Señal de entrada
        fs: Frecuencia de muestreo
        lowcut: Frecuencia baja (Hz)
        highcut: Frecuencia alta (Hz)
        order: Orden del filtro
        
    Returns:
        Señal filtrada
    """
    from scipy import signal as scipy_signal
    
    nyquist = fs / 2
    low = lowcut / nyquist
    high = highcut / nyquist
    
    # Asegurar que los valores están en rango válido
    low = max(0.001, min(low, 0.999))
    high = max(0.001, min(high, 0.999))
    
    if low >= high:
        high = min(low + 0.1, 0.999)
    
    b, a = scipy_signal.butter(order, [low, high], btype='band')
    return scipy_signal.filtfilt(b, a, signal)


def apply_highpass_filter(signal: np.ndarray, fs: float, 
                         cutoff: float, order: int = 4) -> np.ndarray:
    """
    Aplica filtro paso alto
    
    Args:
        signal: Señal de entrada
        fs: Frecuencia de muestreo
        cutoff: Frecuencia de corte (Hz)
        order: Orden del filtro
        
    Returns:
        Señal filtrada
    """
    from scipy import signal as scipy_signal
    
    nyquist = fs / 2
    normalized_cutoff = cutoff / nyquist
    normalized_cutoff = max(0.001, min(normalized_cutoff, 0.999))
    
    b, a = scipy_signal.butter(order, normalized_cutoff, btype='high')
    return scipy_signal.filtfilt(b, a, signal)


def extract_envelope(signal: np.ndarray, fs: float, 
                    lowcut: float = 5, highcut: float = None) -> np.ndarray:
    """
    Extrae la envolvente de una señal (demodulación)
    
    Args:
        signal: Señal de entrada
        fs: Frecuencia de muestreo
        lowcut: Frecuencia baja del pase banda (Hz)
        highcut: Frecuencia alta del pase banda (Hz)
        
    Returns:
        Envolvente de la señal
    """
    if highcut is None:
        highcut = fs / 2 - 100
    
    # Filtraré paso banda para aislar componente
    filtered = apply_bandpass_filter(signal, fs, lowcut, highcut)
    
    # Demodular usando magnitud de analítica
    analytical_signal = np.hilbert(filtered)
    envelope = np.abs(analytical_signal)
    
    return envelope


def moving_rms(signal: np.ndarray, window_size: int) -> np.ndarray:
    """
    Calcula RMS móvil
    
    Args:
        signal: Señal de entrada
        window_size: Tamaño de la ventana
        
    Returns:
        Array con RMS móvil
    """
    rms_values = []
    for i in range(len(signal) - window_size + 1):
        window = signal[i:i + window_size]
        rms = np.sqrt(np.mean(window ** 2))
        rms_values.append(rms)
    
    return np.array(rms_values)


def moving_peak(signal: np.ndarray, window_size: int) -> np.ndarray:
    """
    Calcula pico móvil
    
    Args:
        signal: Señal de entrada
        window_size: Tamaño de la ventana
        
    Returns:
        Array con pico móvil
    """
    peak_values = []
    for i in range(len(signal) - window_size + 1):
        window = signal[i:i + window_size]
        peak = np.max(np.abs(window))
        peak_values.append(peak)
    
    return np.array(peak_values)


def moving_kurtosis(signal: np.ndarray, window_size: int) -> np.ndarray:
    """
    Calcula kurtosis móvil
    
    Args:
        signal: Señal de entrada
        window_size: Tamaño de la ventana
        
    Returns:
        Array con kurtosis móvil
    """
    from scipy.stats import kurtosis
    
    kurt_values = []
    for i in range(len(signal) - window_size + 1):
        window = signal[i:i + window_size]
        kurt = kurtosis(window, fisher=False)  # Usar kurtosis de Pearson
        kurt_values.append(kurt)
    
    return np.array(kurt_values)


def save_analysis_to_json(diagnosis_result: Dict, filepath: str) -> None:
    """
    Guarda resultado de diagnóstico en JSON
    
    Args:
        diagnosis_result: Diccionario con resultado de diagnóstico
        filepath: Ruta del archivo
    """
    # Convertir valores numpy a tipos serializables
    def convert_for_json(obj):
        if isinstance(obj, (np.integer, np.floating)):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: convert_for_json(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_for_json(item) for item in obj]
        return obj
    
    converted = convert_for_json(diagnosis_result)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(converted, f, indent=2, ensure_ascii=False)


def load_analysis_from_json(filepath: str) -> Dict:
    """
    Carga resultado de diagnóstico desde JSON
    
    Args:
        filepath: Ruta del archivo JSON
        
    Returns:
        Diccionario con resultado
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)
