"""
Scripts útiles para el simulador
"""

import sys
from pathlib import Path

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent))

print("\n✓ Simulador de Análisis Vibracional iniciado correctamente")
print("\nPara ejecutar la interfaz gráfica:")
print("  streamlit run app.py")
print("\nPara ejecutar ejemplos:")
print("  python examples/sample_analysis.py")
print("\nPara usar en código:")
print("""
from src.signal_generator import SignalGenerator, SignalConfig
from src.signal_analyzer import SignalAnalyzer
from src.fault_simulator import FaultSimulator, FaultType, FaultSeverity
from src.diagnostics import DiagnosticEngine
""")
