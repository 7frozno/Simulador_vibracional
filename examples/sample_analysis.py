"""
Ejemplo de uso del simulador de análisis vibracional
Análisis completo de diferentes tipos de falla
"""

import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
import sys

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.signal_generator import SignalGenerator, SignalConfig
from src.signal_analyzer import SignalAnalyzer
from src.fault_simulator import FaultSimulator, FaultType, FaultSeverity
from src.diagnostics import DiagnosticEngine
import config


def example_basic_analysis():
    """Ejemplo básico: Analizar una señal sana"""
    print("=" * 60)
    print("EJEMPLO 1: Análisis de Equipo Sano")
    print("=" * 60)
    
    # Configuración
    cfg = SignalConfig(
        sampling_rate=10000,
        duration=1.0,
        rpm=1500,
        amplitude=1.0
    )
    
    # Generar señal sana
    gen = SignalGenerator(cfg)
    time, signal = gen.generate_healthy()
    
    # Analizar
    analyzer = SignalAnalyzer(cfg.sampling_rate)
    features = analyzer.get_all_features(signal, cfg.rpm)
    
    print("\nCaracterísticas de Dominio del Tiempo:")
    print("-" * 40)
    for key, value in features['time_domain'].items():
        print(f"  {key:20s}: {value:10.6f}")
    
    print("\nCaracterísticas de Dominio de Frecuencia:")
    print("-" * 40)
    for key, value in features['frequency_domain'].items():
        if 'amplitude' in key:
            print(f"  {key:20s}: {value:10.6f}")
    
    print("\n✓ Equipo sano: Bajos niveles de vibración, espectro limpio\n")


def example_fault_detection():
    """Ejemplo: Detectar y diagnosticar diferentes tipos de falla"""
    print("=" * 60)
    print("EJEMPLO 2: Detección y Diagnóstico de Fallas")
    print("=" * 60)
    
    cfg = SignalConfig(rpm=1500)
    fault_sim = FaultSimulator(cfg)
    engine = DiagnosticEngine(cfg.sampling_rate, cfg.rpm)
    
    # Probar diferentes fallas
    faults_to_test = [
        (FaultType.UNBALANCE, FaultSeverity.MODERATE, "Desbalance Moderado"),
        (FaultType.MISALIGNMENT, FaultSeverity.MODERATE, "Desalineamiento Moderado"),
        (FaultType.BEARING, FaultSeverity.SEVERE, "Falla de Rodamiento Severa"),
        (FaultType.CAVITATION, FaultSeverity.MODERATE, "Cavitación Moderada"),
    ]
    
    for fault_type, severity, description in faults_to_test:
        print(f"\n{description}")
        print("-" * 40)
        
        # Generar falla
        time, signal = fault_sim.generate_fault(fault_type, severity)
        
        # Diagnosticar
        diagnosis = engine.diagnose(signal)
        
        print(f"Falla Detectada: {diagnosis['primary_fault'].value.upper()}")
        print(f"Confianza: {diagnosis['confidence']:.1%}")
        print(f"Severidad: {diagnosis['severity_level']}")
        
        # Mostrar otros scores
        print("\nScores de Confianza:")
        for fault, score in diagnosis['all_scores'].items():
            print(f"  {fault.value:20s}: {score:6.1%}")
        
        # Recomendaciones
        print("\nRecomendaciones:")
        for i, rec in enumerate(diagnosis['recommendations'][:2], 1):
            print(f"  {i}. {rec}")


def example_comparative_analysis():
    """Ejemplo: Comparar señal sana vs defectuosa"""
    print("=" * 60)
    print("EJEMPLO 3: Comparación Sano vs Defectuoso")
    print("=" * 60)
    
    cfg = SignalConfig(rpm=1500)
    fault_sim = FaultSimulator(cfg)
    analyzer = SignalAnalyzer(cfg.sampling_rate)
    
    # Generar señales
    _, signal_healthy = fault_sim.generate_fault(FaultType.HEALTHY)
    _, signal_unbalance = fault_sim.generate_fault(FaultType.UNBALANCE, FaultSeverity.MODERATE)
    
    print("\n" + "Parámetro".ljust(20) + "| Sano".ljust(15) + "| Desbalance")
    print("-" * 50)
    
    for signal, name in [(signal_healthy, "healthy"), (signal_unbalance, "unbalance")]:
        features = analyzer.get_all_features(signal, cfg.rpm)
        time_feat = features['time_domain']
        freq_feat = features['frequency_domain']
        
        if name == "healthy":
            rms_h = time_feat['rms']
            cfg_h = time_feat['crest_factor']
            k_h = time_feat['kurtosis']
            x1_h = freq_feat['1X_amplitude']
            x2_h = freq_feat['2X_amplitude']
        else:
            rms_d = time_feat['rms']
            cfg_d = time_feat['crest_factor']
            k_d = time_feat['kurtosis']
            x1_d = freq_feat['1X_amplitude']
            x2_d = freq_feat['2X_amplitude']
    
    print(f"{'RMS (g)':20s}| {rms_h:14.6f} | {rms_d:.6f}")
    print(f"{'Factor de Cresta':20s}| {cfg_h:14.6f} | {cfg_d:.6f}")
    print(f"{'Kurtosis':20s}| {k_h:14.6f} | {k_d:.6f}")
    print(f"{'1X Amplitud':20s}| {x1_h:14.6f} | {x1_d:.6f}")
    print(f"{'2X Amplitud':20s}| {x2_h:14.6f} | {x2_d:.6f}")
    
    ratio_healthy = x1_h / (x2_h + 1e-10)
    ratio_unbalance = x1_d / (x2_d + 1e-10)
    print(f"{'Relación 1X/2X':20s}| {ratio_healthy:14.2f} | {ratio_unbalance:.2f}")


def example_severity_analysis():
    """Ejemplo: Analizar diferentes niveles de severidad"""
    print("=" * 60)
    print("EJEMPLO 4: Análisis de Severidad de Desbalance")
    print("=" * 60)
    
    cfg = SignalConfig(rpm=1500)
    fault_sim = FaultSimulator(cfg)
    engine = DiagnosticEngine(cfg.sampling_rate, cfg.rpm)
    
    severities = [
        FaultSeverity.NONE,
        FaultSeverity.MILD,
        FaultSeverity.MODERATE,
        FaultSeverity.SEVERE,
        FaultSeverity.CRITICAL
    ]
    
    print(f"\n{'Severidad':20s} | {'Diag.':15s} | {'Conf.':8s} | {'Sev.':10s}")
    print("-" * 60)
    
    for severity in severities:
        _, signal = fault_sim.generate_fault(FaultType.UNBALANCE, severity)
        diagnosis = engine.diagnose(signal)
        
        sev_name = severity.name.ljust(20)
        diag_name = diagnosis['primary_fault'].value[:15].ljust(15)
        conf = f"{diagnosis['confidence']:.1%}".ljust(8)
        sev_level = diagnosis['severity_level'].ljust(10)
        
        print(f"{sev_name} | {diag_name} | {conf} | {sev_level}")


def example_frequency_analysis():
    """Ejemplo: Análisis frecuencial detallado"""
    print("=" * 60)
    print("EJEMPLO 5: Análisis Espectral Detallado")
    print("=" * 60)
    
    cfg = SignalConfig(rpm=1500)
    fault_sim = FaultSimulator(cfg)
    analyzer = SignalAnalyzer(cfg.sampling_rate)
    
    _, signal = fault_sim.generate_fault(FaultType.MISALIGNMENT, FaultSeverity.MODERATE)
    
    # FFT
    freqs, spectrum = analyzer.get_spectrum(signal, max_freq=5000)
    
    # Frecuencias dominantes
    dom_freqs, dom_mags = analyzer.get_dominant_frequencies(signal, n_peaks=5)
    
    print("\nFrecuencias Dominantes:")
    print("-" * 40)
    print(f"{'Ranking':10s} | {'Frecuencia (Hz)':20s} | {'Magnitud':10s}")
    print("-" * 40)
    
    for i, (freq, mag) in enumerate(zip(dom_freqs, dom_mags), 1):
        print(f"{i:10d} | {freq:20.2f} | {mag:10.6f}")
    
    # Ancho de banda
    bw = analyzer.calculate_bandwidth(signal)
    print(f"\nAncho de Banda (-3dB): {bw:.2f} Hz")
    
    # Energía por banda
    feats = analyzer.get_frequency_domain_features(signal, cfg.rpm)
    total_energy = (feats['low_freq_energy'] + feats['mid_freq_energy'] + feats['high_freq_energy'])
    
    if total_energy > 0:
        print(f"\nDistribución de Energía:")
        print(f"  Baja (0-500 Hz):     {feats['low_freq_energy']/total_energy:6.1%}")
        print(f"  Media (500-2k Hz):   {feats['mid_freq_energy']/total_energy:6.1%}")
        print(f"  Alta (2k+ Hz):       {feats['high_freq_energy']/total_energy:6.1%}")


def example_temporal_trends():
    """Ejemplo: Tendencias temporales de degradación"""
    print("=" * 60)
    print("EJEMPLO 6: Simulación de Degradación Temporal")
    print("=" * 60)
    
    cfg = SignalConfig(rpm=1500)
    fault_sim = FaultSimulator(cfg)
    engine = DiagnosticEngine(cfg.sampling_rate, cfg.rpm)
    
    print("\nProgresión de Desbalance:")
    print("-" * 50)
    print(f"{'Tiempo (horas)':15s} | {'RMS (g)':12s} | {'Severidad':15s}")
    print("-" * 50)
    
    for hours, severity in [
        (0, FaultSeverity.NONE),
        (100, FaultSeverity.MILD),
        (200, FaultSeverity.MODERATE),
        (300, FaultSeverity.SEVERE),
        (400, FaultSeverity.CRITICAL),
    ]:
        _, signal = fault_sim.generate_fault(FaultType.UNBALANCE, severity)
        diagnosis = engine.diagnose(signal)
        
        from src.signal_analyzer import SignalAnalyzer
        analyzer = SignalAnalyzer(cfg.sampling_rate)
        rms = analyzer.calculate_rms(signal)
        
        print(f"{hours:15d} | {rms:12.6f} | {diagnosis['severity_level']:15s}")


def main():
    """Ejecuta todos los ejemplos"""
    
    print("\n")
    print("█" * 60)
    print("█  SIMULADOR DE ANÁLISIS VIBRACIONAL - EJEMPLOS".ljust(60) + "█")
    print("█" * 60)
    print()
    
    example_basic_analysis()
    example_fault_detection()
    example_comparative_analysis()
    example_severity_analysis()
    example_frequency_analysis()
    example_temporal_trends()
    
    print("\n")
    print("█" * 60)
    print("█  Ejemplos completados exitosamente".ljust(60) + "█")
    print("█" * 60)
    print()


if __name__ == "__main__":
    main()
