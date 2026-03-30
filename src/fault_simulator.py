"""
Simulador de fallas en equipos rotativos
Crea señales vibratorias con defectos realistas
"""

from enum import Enum
from typing import Tuple, Dict
import numpy as np
from .signal_generator import SignalGenerator, SignalConfig


class FaultType(Enum):
    """Tipos de fallas simulables"""
    HEALTHY = "sano"
    BEARING = "rodamiento"
    CAVITATION = "cavitacion"
    MISALIGNMENT = "desalineamiento"
    UNBALANCE = "desbalance"
    COMBINED = "combinada"


class FaultSeverity(Enum):
    """Niveles de severidad de falla"""
    NONE = 0.0
    MILD = 0.3
    MODERATE = 0.6
    SEVERE = 0.9
    CRITICAL = 1.0


class FaultSimulator:
    """Simulador de fallas en bombas y equipos rotativos"""
    
    def __init__(self, config: SignalConfig = None):
        """
        Inicializa el simulador de fallas
        
        Args:
            config: Configuración de la señal
        """
        self.config = config or SignalConfig()
        self.generator = SignalGenerator(config)
        self.current_fault = None
        self.current_severity = None
        
    def generate_fault(self, fault_type: FaultType, 
                      severity: FaultSeverity = FaultSeverity.MODERATE) -> Tuple[np.ndarray, np.ndarray]:
        """
        Genera una señal vibracional con una falla específica
        
        Args:
            fault_type: Tipo de falla
            severity: Nivel de severidad
            
        Returns:
            Tupla (tiempo, señal con falla)
        """
        self.current_fault = fault_type
        self.current_severity = severity
        
        severity_value = severity.value
        
        if fault_type == FaultType.HEALTHY:
            return self.generator.generate_healthy()
        
        elif fault_type == FaultType.BEARING:
            return self.generator.generate_beating_fault(beat_freq=20.0 * severity_value)
        
        elif fault_type == FaultType.CAVITATION:
            t, signal = self.generator.generate_cavitation()
            # Aumentar amplitud según severidad
            return t, signal * (0.5 + 0.5 * severity_value)
        
        elif fault_type == FaultType.MISALIGNMENT:
            return self.generator.generate_misalignment(severity=severity_value)
        
        elif fault_type == FaultType.UNBALANCE:
            return self.generator.generate_unbalance(severity=severity_value)
        
        elif fault_type == FaultType.COMBINED:
            return self._generate_combined_fault(severity_value)
        
        else:
            raise ValueError(f"Tipo de falla desconocido: {fault_type}")
    
    def _generate_combined_fault(self, severity: float) -> Tuple[np.ndarray, np.ndarray]:
        """
        Genera una señal combinada con múltiples fallas
        
        Args:
            severity: Nivel de severidad general
            
        Returns:
            Tupla (tiempo, señal combinada)
        """
        # Combinar desbalance + desalineamiento + ligero defecto de rodamiento
        t1, unbalance = self.generator.generate_unbalance(severity=0.6 * severity)
        t2, misalign = self.generator.generate_misalignment(severity=0.4 * severity)
        t3, bearing = self.generator.generate_beating_fault(beat_freq=10.0 * severity)
        
        # Combinar proporcionalmente
        combined = (0.5 * unbalance + 0.3 * misalign + 0.2 * bearing)
        combined = combined / np.max(np.abs(combined)) * self.config.amplitude
        
        return t1, combined
    
    def get_fault_description(self, fault_type: FaultType) -> str:
        """
        Obtiene descripción de un tipo de falla
        
        Args:
            fault_type: Tipo de falla
            
        Returns:
            Descripción detallada
        """
        descriptions = {
            FaultType.HEALTHY: {
                'name': 'Equipo Sano',
                'description': 'Funcionamiento normal sin defectos detectables',
                'characteristics': [
                    'Bajos niveles de vibración',
                    'Componente 1X moderado',
                    'Bajo factor de cresta (< 4)',
                    'Espectro limpio y bien definido'
                ],
                'typical_values': {
                    'rms': '0.1 - 0.3 g',
                    'kurtosis': '3.0 - 3.5',
                    'crest_factor': '2.5 - 4.0'
                }
            },
            FaultType.BEARING: {
                'name': 'Falla de Rodamiento',
                'description': 'Defecto en elementosrodantes o pistas del rodamiento',
                'characteristics': [
                    'Impulsos de alta frecuencia (1-5 kHz)',
                    'Modulación por velocidad de rotación',
                    'Factor de cresta elevado (> 6)',
                    'Kurtosis muy elevada (> 8)',
                    'Espectro con bandas laterales'
                ],
                'typical_values': {
                    'rms': '0.5 - 2.0 g',
                    'kurtosis': '> 8.0',
                    'crest_factor': '> 6.0'
                }
            },
            FaultType.CAVITATION: {
                'name': 'Cavitación',
                'description': 'Formación y colapso de burbujas en el fluido',
                'characteristics': [
                    'Ruido de banda ancha',
                    'Impulsos aleatorios',
                    'Rápido incremento de amplitud',
                    'Espectro plano en amplio rango',
                    'Posible daño físico de componentes'
                ],
                'typical_values': {
                    'rms': '0.8 - 3.0 g',
                    'bandwidth': '> 3000 Hz',
                    'crest_factor': '4.0 - 7.0'
                }
            },
            FaultType.MISALIGNMENT: {
                'name': 'Desalineamiento',
                'description': 'Desaliche axial o angular entre ejes',
                'characteristics': [
                    'Amplificación de armónicos pares (2X, 4X, 6X)',
                    'Componentes axiales elevadas',
                    'Bandas laterales alrededor de armónicos',
                    'Incremento gradual con temperatura',
                    'Posible resonancia'
                ],
                'typical_values': {
                    'rms': '0.4 - 1.5 g',
                    '2X_amplitude': 'Mayor que 1X',
                    'kurtosis': '3.5 - 5.0'
                }
            },
            FaultType.UNBALANCE: {
                'name': 'Desbalance',
                'description': 'Distribución no uniforme de masa rotacional',
                'characteristics': [
                    'Dominancia de componente 1X',
                    'Bajo o nulo contenido de 2X y 3X',
                    'Vibración sincrónica con RPM',
                    'Incremento lineal con velocidad',
                    'Direcciones radiales principalmente'
                ],
                'typical_values': {
                    'rms': '0.3 - 1.2 g',
                    '1X_amplitude': '> 50% de total',
                    'kurtosis': '3.0 - 4.0'
                }
            },
            FaultType.COMBINED: {
                'name': 'Falla Combinada',
                'description': 'Múltiples defectos simultáneamente',
                'characteristics': [
                    'Síntomas de varios tipos de falla',
                    'Espectro complejo y denso',
                    'Múltiples picos de energía',
                    'Comportamiento impredecible',
                    'Requiere análisis cuidadoso'
                ],
                'typical_values': {
                    'rms': '0.8 - 3.0 g',
                    'kurtosis': '5.0 - 10.0+',
                    'spectrum': 'Denso y complejo'
                }
            }
        }
        
        return descriptions.get(fault_type, {})
    
    def get_fault_indicators(self, fault_type: FaultType) -> Dict[str, str]:
        """
        Obtiene los indicadores clave para cada tipo de falla
        
        Args:
            fault_type: Tipo de falla
            
        Returns:
            Diccionario de indicadores clave
        """
        indicators = {
            FaultType.HEALTHY: {
                'primary': 'RMS bajo, kurtosis ≈ 3',
                'secondary': 'Espectro limpio, picos bien definidos',
                'tertiary': 'Factor de cresta moderado'
            },
            FaultType.BEARING: {
                'primary': 'Kurtosis >> 3, factor de cresta > 6',
                'secondary': 'Impulsos de HF con bandas laterales',
                'tertiary': 'Espectro con envolvente modulada'
            },
            FaultType.CAVITATION: {
                'primary': 'Ruido de banda ancha, RMS alto',
                'secondary': 'Aumento rápido con tiempo',
                'tertiary': 'Espectro extendido, poco estructurado'
            },
            FaultType.MISALIGNMENT: {
                'primary': '2X >> 1X, armónicos pares grandes',
                'secondary': 'Bandas laterales en armónicos',
                'tertiary': 'Componente axial elevada'
            },
            FaultType.UNBALANCE: {
                'primary': '1X dominante, 2X muy baja',
                'secondary': 'Relación 1X/2X > 5',
                'tertiary': 'Kurtosis cercana a 3'
            },
            FaultType.COMBINED: {
                'primary': 'Síntomas mixtos, espectro denso',
                'secondary': 'Kurtosis elevada, múltiples picos',
                'tertiary': 'Requiere análisis discriminador'
            }
        }
        
        return indicators.get(fault_type, {})
