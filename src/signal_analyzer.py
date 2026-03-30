"""
Analizador de señales vibratorias
Realiza FFT, cálculo de características y análisis espectral
"""

import numpy as np
from scipy import signal as scipy_signal
from scipy.fft import fft, fftfreq
from typing import Tuple, Dict, Optional
import warnings

warnings.filterwarnings('ignore')


class SignalAnalyzer:
    """Analizador de señales vibratorias"""
    
    def __init__(self, sampling_rate: float = 10000):
        """
        Inicializa el analizador
        
        Args:
            sampling_rate: Frecuencia de muestreo (Hz)
        """
        self.sampling_rate = sampling_rate
        self.frequencies = None
        self.fft_magnitude = None
        
    def calculate_fft(self, signal: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calcula la FFT de una señal
        
        Args:
            signal: Señal de entrada
            
        Returns:
            Tupla (frecuencias, magnitudes)
        """
        n = len(signal)
        self.fft_magnitude = np.abs(fft(signal))
        self.frequencies = fftfreq(n, 1/self.sampling_rate)
        
        # Retornar solo frecuencias positivas
        positive_idx = self.frequencies >= 0
        return self.frequencies[positive_idx], self.fft_magnitude[positive_idx]
    
    def get_spectrum(self, signal: np.ndarray, 
                     max_freq: Optional[float] = None) -> Tuple[np.ndarray, np.ndarray]:
        """
        Obtiene el espectro de potencia normalizado
        
        Args:
            signal: Señal de entrada
            max_freq: Frecuencia máxima a analizar
            
        Returns:
            Tupla (frecuencias, potencia normalizada)
        """
        freqs, magnitude = self.calculate_fft(signal)
        
        # Normalizar
        spectrum = magnitude / np.max(magnitude)
        
        if max_freq:
            idx = freqs <= max_freq
            freqs = freqs[idx]
            spectrum = spectrum[idx]
        
        return freqs, spectrum
    
    def calculate_rms(self, signal: np.ndarray) -> float:
        """
        Calcula el RMS (Root Mean Square) de la señal
        
        Args:
            signal: Señal de entrada
            
        Returns:
            Valor RMS
        """
        return np.sqrt(np.mean(signal ** 2))
    
    def calculate_peak(self, signal: np.ndarray) -> float:
        """
        Calcula el valor de pico de la señal
        
        Args:
            signal: Señal de entrada
            
        Returns:
            Valor de pico (máxima amplitud absoluta)
        """
        return np.max(np.abs(signal))
    
    def calculate_peak_to_peak(self, signal: np.ndarray) -> float:
        """
        Calcula el valor pico a pico
        
        Args:
            signal: Señal de entrada
            
        Returns:
            Valor pico a pico
        """
        return np.max(signal) - np.min(signal)
    
    def calculate_crest_factor(self, signal: np.ndarray) -> float:
        """
        Calcula el factor de cresta (Peak / RMS)
        Valores altos indican la presencia de impactos
        
        Args:
            signal: Señal de entrada
            
        Returns:
            Factor de cresta
        """
        peak = self.calculate_peak(signal)
        rms = self.calculate_rms(signal)
        return peak / rms if rms > 0 else 0
    
    def calculate_skewness(self, signal: np.ndarray) -> float:
        """
        Calcula la asimetría (skewness) de la distribución
        Indica presencia de impactos transitorios
        
        Args:
            signal: Señal de entrada
            
        Returns:
            Coeficiente de asimetría
        """
        mean = np.mean(signal)
        std = np.std(signal)
        if std == 0:
            return 0
        return np.mean(((signal - mean) / std) ** 3)
    
    def calculate_kurtosis(self, signal: np.ndarray) -> float:
        """
        Calcula la curtosis de la distribución
        Valor > 3 indica presencia de impactos (fallas)
        
        Args:
            signal: Señal de entrada
            
        Returns:
            Coeficiente de curtosis
        """
        mean = np.mean(signal)
        std = np.std(signal)
        if std == 0:
            return 3
        return np.mean(((signal - mean) / std) ** 4)
    
    def get_dominant_frequencies(self, signal: np.ndarray, 
                                 n_peaks: int = 5) -> Tuple[np.ndarray, np.ndarray]:
        """
        Identifica las frecuencias dominantes
        
        Args:
            signal: Señal de entrada
            n_peaks: Número de picos a identificar
            
        Returns:
            Tupla (frecuencias dominantes, magnitudes)
        """
        freqs, spectrum = self.get_spectrum(signal)
        
        # Encontrar picos
        peaks, _ = scipy_signal.find_peaks(spectrum, height=0.05)
        
        if len(peaks) == 0:
            return np.array([]),np.array([])
        
        # Ordenar por amplitud
        heights = spectrum[peaks]
        sorted_idx = np.argsort(-heights)[:n_peaks]
        dominant_peaks = peaks[sorted_idx]
        
        return freqs[dominant_peaks], spectrum[dominant_peaks]
    
    def calculate_bandwidth(self, signal: np.ndarray, 
                           threshold_db: float = 3) -> float:
        """
        Calcula el ancho de banda de -3dB
        
        Args:
            signal: Señal de entrada
            threshold_db: Umbral en dB
            
        Returns:
            Ancho de banda en Hz
        """
        freqs, spectrum = self.get_spectrum(signal)
        spectrum_db = 20 * np.log10(spectrum + 1e-10)
        
        max_db = np.max(spectrum_db)
        threshold = max_db - threshold_db
        
        above_threshold = spectrum_db >= threshold
        if not np.any(above_threshold):
            return 0
        
        indices = np.where(above_threshold)[0]
        return freqs[indices[-1]] - freqs[indices[0]]
    
    def get_time_domain_features(self, signal: np.ndarray) -> Dict[str, float]:
        """
        Calcula características en el dominio del tiempo
        
        Args:
            signal: Señal de entrada
            
        Returns:
            Diccionario con características
        """
        return {
            'rms': self.calculate_rms(signal),
            'peak': self.calculate_peak(signal),
            'peak_to_peak': self.calculate_peak_to_peak(signal),
            'crest_factor': self.calculate_crest_factor(signal),
            'skewness': self.calculate_skewness(signal),
            'kurtosis': self.calculate_kurtosis(signal),
            'mean': np.mean(signal),
            'std': np.std(signal),
            'variance': np.var(signal)
        }
    
    def get_frequency_domain_features(self, signal: np.ndarray,
                                     rpm: float = 1500) -> Dict[str, float]:
        """
        Calcula características en el dominio de la frecuencia
        
        Args:
            signal: Señal de entrada
            rpm: Revoluciones por minuto
            
        Returns:
            Diccionario con características
        """
        freqs, spectrum = self.get_spectrum(signal)
        f0 = rpm / 60.0  # Frecuencia fundamental
        
        # Definir bandas
        features = {}
        for n in range(1, 8):
            target_freq = n * f0
            # Buscar magnitud en ±10% de la frecuencia
            band = np.abs(freqs - target_freq) < 0.1 * target_freq
            if np.any(band):
                features[f'{n}X_amplitude'] = np.max(spectrum[band])
            else:
                features[f'{n}X_amplitude'] = 0
        
        # Total energía en diferentes rangos
        low_band = (freqs > 0) & (freqs < 500)
        mid_band = (freqs >= 500) & (freqs < 2000)
        high_band = (freqs >= 2000)
        
        features['low_freq_energy'] = np.sum(spectrum[low_band] ** 2)
        features['mid_freq_energy'] = np.sum(spectrum[mid_band] ** 2)
        features['high_freq_energy'] = np.sum(spectrum[high_band] ** 2)
        features['bandwidth'] = self.calculate_bandwidth(signal)
        
        return features
    
    def get_all_features(self, signal: np.ndarray, 
                        rpm: float = 1500) -> Dict[str, Dict[str, float]]:
        """
        Obtiene todas las características de la señal
        
        Args:
            signal: Señal de entrada
            rpm: Revoluciones por minuto
            
        Returns:
            Diccionario con características de tiempo y frecuencia
        """
        return {
            'time_domain': self.get_time_domain_features(signal),
            'frequency_domain': self.get_frequency_domain_features(signal, rpm)
        }
