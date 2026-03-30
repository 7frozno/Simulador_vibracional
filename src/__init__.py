"""
Simulador de Análisis Vibracional
Módulo para análisis y diagnóstico de fallas en equipos rotacionales
"""

__version__ = "1.0.0"
__author__ = "Simulador Vibracional"

from .signal_generator import SignalGenerator
from .signal_analyzer import SignalAnalyzer
from .fault_simulator import FaultSimulator
from .diagnostics import DiagnosticEngine

__all__ = [
    "SignalGenerator",
    "SignalAnalyzer", 
    "FaultSimulator",
    "DiagnosticEngine"
]
