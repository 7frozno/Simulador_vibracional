"""
Generador de señales vibratorias sintéticas
Simula vibraciones realistas de bombas y equipos rotativos
"""

import numpy as np
from dataclasses import dataclass
from typing import Tuple, Dict


@dataclass
class SignalConfig:
    """Configuración de la señal vibracional"""
    sampling_rate: float = 10000  # Hz
    duration: float = 1.0  # segundos
    rpm: float = 1500  # revoluciones por minuto
    amplitude: float = 1.0  # amplitud base (unidades de aceleración g)


class SignalGenerator:
    """Generador de señales vibratorias sintéticas"""
    
    def __init__(self, config: SignalConfig = None):
        """
        Inicializa el generador de señales
        
        Args:
            config: Configuración de la señal
        """
        self.config = config or SignalConfig()
        self.time = None
        self.signal = None
        
    @property
    def frequency_fundamental(self) -> float:
        """Frequencia fundamental (revoluciones por segundo)"""
        return self.config.rpm / 60.0
    
    def generate_healthy(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Genera una señal de una bomba sana
        Contiene ruido aleatorio y componentes de baja amplitud
        
        Returns:
            Tupla (tiempo, señal)
        """
        fs = self.config.sampling_rate
        duration = self.config.duration
        t = np.linspace(0, duration, int(fs * duration), endpoint=False)
        self.time = t
        
        # Ruido blanco base
        signal = np.random.normal(0, self.config.amplitude * 0.1, len(t))
        
        # Agregar componentes armónicos de baja amplitud (características normales)
        f0 = self.frequency_fundamental
        
        # 1X - Velocidad sincrónica
        signal += self.config.amplitude * 0.05 * np.sin(2 * np.pi * f0 * t)
        
        # 2X - Armónico
        signal += self.config.amplitude * 0.03 * np.sin(2 * np.pi * 2 * f0 * t)
        
        # Ruido de fluido (baja frecuencia)
        signal += self.config.amplitude * 0.08 * np.sin(2 * np.pi * 50 * t)
        
        self.signal = signal
        return t, signal
    
    def generate_beating_fault(self, beat_freq: float = 20.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Genera señal con falla de rodamiento (modulación del beat)
        La falla de rodamiento produce impactos modulados por velocidad
        
        Args:
            beat_freq: Frecuencia de modulación (Hz)
            
        Returns:
            Tupla (tiempo, señal)
        """
        fs = self.config.sampling_rate
        duration = self.config.duration
        t = np.linspace(0, duration, int(fs * duration), endpoint=False)
        self.time = t
        
        f0 = self.frequency_fundamental
        
        # Impulsos de rodamiento a alta frecuencia
        carrier_freq = 2000  # Frecuencia portadora para impactos
        
        # Modulación AM (amplitud modulada)
        modulation = 0.5 * (1 + np.sin(2 * np.pi * beat_freq * t))
        
        # Portadora (impactos de rodamiento)
        carrier = self.config.amplitude * 0.8 * np.sin(
            2 * np.pi * carrier_freq * t + 
            0.3 * np.cos(2 * np.pi * beat_freq * t)  # Modulación de fase
        )
        
        # Signal modulada
        signal = modulation * carrier
        
        # Añadir componentes de 1X y 2X
        signal += self.config.amplitude * 0.1 * np.sin(2 * np.pi * f0 * t)
        signal += self.config.amplitude * 0.05 * np.sin(2 * np.pi * 2 * f0 * t)
        
        # Ruido de fondo
        signal += np.random.normal(0, self.config.amplitude * 0.05, len(t))
        
        self.signal = signal
        return t, signal
    
    def generate_cavitation(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Genera señal con cavitación
        Caracterizada por ruido de banda ancha con picos repetitivos
        
        Returns:
            Tupla (tiempo, señal)
        """
        fs = self.config.sampling_rate
        duration = self.config.duration
        t = np.linspace(0, duration, int(fs * duration), endpoint=False)
        self.time = t
        
        f0 = self.frequency_fundamental
        
        # Ruido de banda ancha (características de cavitación)
        signal = np.random.normal(0, self.config.amplitude * 0.6, len(t))
        
        # Impulsos periódicos (burbujas colapsando)
        impulse_freq = 5 * f0  # Impulsos a múltiplos de RPM
        impulse_times = np.arange(0, duration, 1/impulse_freq)
        
        for imp_time in impulse_times:
            # Ventana gaussiana para cada impulso
            impulse_window = np.exp(-((t - imp_time)**2) / (0.001**2))
            signal += self.config.amplitude * 0.7 * impulse_window * \
                     np.sin(2 * np.pi * 3000 * (t - imp_time))
        
        # Componente de f0
        signal += self.config.amplitude * 0.15 * np.sin(2 * np.pi * f0 * t)
        
        self.signal = signal
        return t, signal
    
    def generate_misalignment(self, severity: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Genera señal con desalineamiento
        Caracterizado por amplificación de armónicos pares (2X, 4X, 6X...)
        
        Args:
            severity: Severidad del desalineamiento (0-1)
            
        Returns:
            Tupla (tiempo, señal)
        """
        fs = self.config.sampling_rate
        duration = self.config.duration
        t = np.linspace(0, duration, int(fs * duration), endpoint=False)
        self.time = t
        
        f0 = self.frequency_fundamental
        
        # Ruido base
        signal = np.random.normal(0, self.config.amplitude * 0.1, len(t))
        
        # Amplificación de armónicos pares (característica de desalineamiento)
        signal += self.config.amplitude * 0.15 * severity * np.sin(2 * np.pi * 1 * f0 * t)
        signal += self.config.amplitude * 0.25 * severity * np.sin(2 * np.pi * 2 * f0 * t)
        signal += self.config.amplitude * 0.18 * severity * np.sin(2 * np.pi * 3 * f0 * t)
        signal += self.config.amplitude * 0.22 * severity * np.sin(2 * np.pi * 4 * f0 * t)
        signal += self.config.amplitude * 0.12 * severity * np.sin(2 * np.pi * 5 * f0 * t)
        signal += self.config.amplitude * 0.15 * severity * np.sin(2 * np.pi * 6 * f0 * t)
        
        self.signal = signal
        return t, signal
    
    def generate_unbalance(self, severity: float = 1.0) -> Tuple[np.ndarray, np.ndarray]:
        """
        Genera señal con desbalance
        Caracterizado por amplificación dominante de 1X y baja de 2X
        
        Args:
            severity: Severidad del desbalance (0-1)
            
        Returns:
            Tupla (tiempo, señal)
        """
        fs = self.config.sampling_rate
        duration = self.config.duration
        t = np.linspace(0, duration, int(fs * duration), endpoint=False)
        self.time = t
        
        f0 = self.frequency_fundamental
        
        # Ruido base
        signal = np.random.normal(0, self.config.amplitude * 0.1, len(t))
        
        # Componente 1X dominante (característica de desbalance)
        signal += self.config.amplitude * 0.6 * severity * np.sin(2 * np.pi * f0 * t)
        
        # 2X y 3X significativamente menores
        signal += self.config.amplitude * 0.05 * np.sin(2 * np.pi * 2 * f0 * t)
        signal += self.config.amplitude * 0.08 * np.sin(2 * np.pi * 3 * f0 * t)
        
        # Armónicos menores
        for n in range(4, 7):
            signal += self.config.amplitude * 0.03 * np.sin(2 * np.pi * n * f0 * t)
        
        self.signal = signal
        return t, signal
    
    def generate_with_noise(self, base_signal: np.ndarray, 
                           snr_db: float = 30) -> np.ndarray:
        """
        Agrega ruido a una señal existente
        
        Args:
            base_signal: Señal base
            snr_db: Relación señal-ruido en dB
            
        Returns:
            Señal con ruido
        """
        signal_power = np.mean(base_signal ** 2)
        noise_power = signal_power / (10 ** (snr_db / 10))
        noise = np.random.normal(0, np.sqrt(noise_power), len(base_signal))
        
        return base_signal + noise
