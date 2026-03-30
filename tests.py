"""
Suite de pruebas para el Simulador de Análisis Vibracional
Valida que todos los módulos funcionen correctamente
"""

import sys
from pathlib import Path
import numpy as np

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent))

from src.signal_generator import SignalGenerator, SignalConfig
from src.signal_analyzer import SignalAnalyzer
from src.fault_simulator import FaultSimulator, FaultType, FaultSeverity
from src.diagnostics import DiagnosticEngine


def test_signal_generator():
    """Prueba del generador de señales"""
    print("\n" + "="*50)
    print("TEST 1: Generador de Señales")
    print("="*50)
    
    config = SignalConfig(
        sampling_rate=10000,
        duration=1.0,
        rpm=1500,
        amplitude=1.0
    )
    
    gen = SignalGenerator(config)
    
    # Prueba 1: Señal sana
    t_h, sig_h = gen.generate_healthy()
    assert len(t_h) == len(sig_h), "❌ Longitud inconsistente"
    assert len(sig_h) == 10000, "❌ Número de muestras incorrecto"
    print("✓ generate_healthy(): OK")
    
    # Prueba 2: Desbalance
    t_u, sig_u = gen.generate_unbalance(severity=0.5)
    assert np.any(sig_u != sig_h), "❌ Signals should be different"
    assert len(sig_u) == 10000, "❌ Muestras incorrectas"
    print("✓ generate_unbalance(): OK")
    
    # Prueba 3: Desalineamiento
    t_m, sig_m = gen.generate_misalignment(severity=0.5)
    assert len(sig_m) == 10000, "❌ Muestras incorrectas"
    print("✓ generate_misalignment(): OK")
    
    # Prueba 4: Rodamiento
    t_b, sig_b = gen.generate_beating_fault(beat_freq=20)
    assert len(sig_b) == 10000, "❌ Muestras incorrectas"
    print("✓ generate_beating_fault(): OK")
    
    # Prueba 5: Cavitación
    t_c, sig_c = gen.generate_cavitation()
    assert len(sig_c) == 10000, "❌ Muestras incorrectas"
    print("✓ generate_cavitation(): OK")
    
    # Prueba 6: Ruido
    sig_noise = gen.generate_with_noise(sig_h, snr_db=30)
    assert len(sig_noise) == len(sig_h), "❌ Longitud incorrecto"
    assert np.any(sig_noise != sig_h), "❌ Ruido no añadido"
    print("✓ generate_with_noise(): OK")
    
    print("\n✅ Generador de Señales: TODAS LAS PRUEBAS PASARON")


def test_signal_analyzer():
    """Prueba del analizador de señales"""
    print("\n" + "="*50)
    print("TEST 2: Analizador de Señales")
    print("="*50)
    
    config = SignalConfig(sampling_rate=10000)
    gen = SignalGenerator(config)
    analyzer = SignalAnalyzer(config.sampling_rate)
    
    _, signal = gen.generate_healthy()
    
    # Prueba 1: FFT
    freqs, spectrum = analyzer.calculate_fft(signal)
    assert len(freqs) > 0, "❌ FFT sin frecuencias"
    assert len(spectrum) == len(freqs), "❌ FFT inconsistente"
    print("✓ calculate_fft(): OK")
    
    # Prueba 2: Espectro
    freqs_sp, spec_sp = analyzer.get_spectrum(signal, max_freq=5000)
    assert np.all(freqs_sp <= 5000), "❌ Frecuencias fuera de límite"
    assert np.max(spec_sp) <= 1.0, "❌ Espectro no normalizado"
    print("✓ get_spectrum(): OK")
    
    # Prueba 3: RMS
    rms = analyzer.calculate_rms(signal)
    assert rms > 0, "❌ RMS debe ser positivo"
    assert rms < 10, "❌ RMS muy alto (revisión de unidades)"
    print(f"✓ calculate_rms(): {rms:.6f} g")
    
    # Prueba 4: Pico
    peak = analyzer.calculate_peak(signal)
    assert peak >= rms, "❌ Pico debe ser >= RMS"
    print(f"✓ calculate_peak(): {peak:.6f} g")
    
    # Prueba 5: Pico-Pico
    pp = analyzer.calculate_peak_to_peak(signal)
    assert pp > 0, "❌ Pico-pico debe ser positivo"
    print(f"✓ calculate_peak_to_peak(): {pp:.6f} g")
    
    # Prueba 6: Factor de cresta
    cf = analyzer.calculate_crest_factor(signal)
    assert cf > 1, "❌ CF debe ser > 1"
    assert cf < 20, "❌ CF muy alto"
    print(f"✓ calculate_crest_factor(): {cf:.2f}")
    
    # Prueba 7: Kurtosis
    kurt = analyzer.calculate_kurtosis(signal)
    assert kurt > 0, "❌ Kurtosis debe ser positiva"
    print(f"✓ calculate_kurtosis(): {kurt:.2f}")
    
    # Prueba 8: Asimetría
    skew = analyzer.calculate_skewness(signal)
    assert -10 < skew < 10, "❌ Asimetría fuera de rango"
    print(f"✓ calculate_skewness(): {skew:.2f}")
    
    # Prueba 9: Frecuencias dominantes
    dom_freqs, dom_mags = analyzer.get_dominant_frequencies(signal, n_peaks=3)
    assert len(dom_freqs) <= 3, "❌ Demasiados picos"
    print(f"✓ get_dominant_frequencies(): {len(dom_freqs)} picos")
    
    # Prueba 10: Características
    features = analyzer.get_all_features(signal, rpm=1500)
    assert 'time_domain' in features, "❌ Features incompletas"
    assert 'frequency_domain' in features, "❌ Features incompletas"
    print("✓ get_all_features(): OK")
    
    print("\n✅ Analizador de Señales: TODAS LAS PRUEBAS PASARON")


def test_fault_simulator():
    """Prueba del simulador de fallas"""
    print("\n" + "="*50)
    print("TEST 3: Simulador de Fallas")
    print("="*50)
    
    config = SignalConfig()
    simulator = FaultSimulator(config)
    
    # Prueba cada tipo de falla
    fault_types = [
        FaultType.HEALTHY,
        FaultType.UNBALANCE,
        FaultType.MISALIGNMENT,
        FaultType.BEARING,
        FaultType.CAVITATION,
        FaultType.COMBINED
    ]
    
    for fault in fault_types:
        for severity in [FaultSeverity.MILD, FaultSeverity.MODERATE, FaultSeverity.SEVERE]:
            t, sig = simulator.generate_fault(fault, severity)
            
            assert len(t) > 0, f"❌ {fault.value}: Tiempo vacío"
            assert len(sig) == len(t), f"❌ {fault.value}: Longitud inconsistente"
            assert len(sig) == 10000, f"❌ {fault.value}: Número muestras incorrecto"
        
        print(f"✓ {fault.value}: OK")
    
    # Prueba descripciones
    for fault in FaultType:
        desc = simulator.get_fault_description(fault)
        assert desc, f"❌ {fault.value}: Sin descripción"
        assert 'name' in desc, f"❌ {fault.value}: Sin nombre"
    
    print("✓ get_fault_description(): OK")
    
    # Prueba indicadores
    indicators = simulator.get_fault_indicators(FaultType.UNBALANCE)
    assert 'primary' in indicators, "❌ Indicadores incompletos"
    assert 'secondary' in indicators, "❌ Indicadores incompletos"
    assert 'tertiary' in indicators, "❌ Indicadores incompletos"
    
    print("✓ get_fault_indicators(): OK")
    
    print("\n✅ Simulador de Fallas: TODAS LAS PRUEBAS PASARON")


def test_diagnostic_engine():
    """Prueba del motor de diagnóstico"""
    print("\n" + "="*50)
    print("TEST 4: Motor de Diagnóstico")
    print("="*50)
    
    config = SignalConfig(rpm=1500)
    simulator = FaultSimulator(config)
    engine = DiagnosticEngine(config.sampling_rate, config.rpm)
    
    # Prueba 1: Diagnostico equipo sano
    _, sig_healthy = simulator.generate_fault(FaultType.HEALTHY)
    diag_h = engine.diagnose(sig_healthy)
    
    assert 'primary_fault' in diag_h, "❌ Diagnóstico incompleto"
    assert 'confidence' in diag_h, "❌ Diagnóstico incompleto"
    assert 'severity_level' in diag_h, "❌ Diagnóstico incompleto"
    assert 0 <= diag_h['confidence'] <= 1, "❌ Confianza fuera de rango"
    print(f"✓ Diagnóstico Sano: {diag_h['primary_fault'].value} ({diag_h['confidence']:.1%})")
    
    # Prueba 2: Diagnostico desbalance
    _, sig_unbal = simulator.generate_fault(FaultType.UNBALANCE, FaultSeverity.MODERATE)
    diag_u = engine.diagnose(sig_unbal)
    
    assert diag_u['primary_fault'] == FaultType.UNBALANCE, "❌ Desbalance no detectado"
    assert diag_u['confidence'] > 0.5, "❌ Confianza baja"
    print(f"✓ Diagnóstico Desbalance: Confianza {diag_u['confidence']:.1%}")
    
    # Prueba 3: Diagnostico rodamiento
    _, sig_bearing = simulator.generate_fault(FaultType.BEARING, FaultSeverity.SEVERE)
    diag_b = engine.diagnose(sig_bearing)
    
    assert diag_b['primary_fault'] == FaultType.BEARING, "❌ Rodamiento no detectado"
    print(f"✓ Diagnóstico Rodamiento: Confianza {diag_b['confidence']:.1%}")
    
    # Prueba 4: Verificar recomendaciones
    for fault in FaultType:
        recommendations = engine._get_recommendations(fault)
        assert isinstance(recommendations, list), "❌ Recomendaciones incorrecto formato"
        assert len(recommendations) > 0, "❌ Sin recomendaciones"
    
    print("✓ _get_recommendations(): OK")
    
    # Prueba 5: Verifi evaluacion severidad
    severities = {'NORMAL', 'LEVE', 'MODERADA', 'SEVERA', 'CRÍTICA'}
    assert diag_h['severity_level'] in severities, "❌ Severidad desconocida"
    print(f"✓ _assess_severity(): {diag_h['severity_level']}")
    
    print("\n✅ Motor de Diagnóstico: TODAS LAS PRUEBAS PASARON")


def test_consistency():
    """Pruebas de consistencia entre módulos"""
    print("\n" + "="*50)
    print("TEST 5: Consistencia entre Módulos")
    print("="*50)
    
    config = SignalConfig(rpm=1500, sampling_rate=10000, duration=1.0)
    
    # Generar y analizar
    gen = SignalGenerator(config)
    analyzer = SignalAnalyzer(config.sampling_rate)
    engine = DiagnosticEngine(config.sampling_rate, config.rpm)
    
    t, sig = gen.generate_unbalance(severity=0.6)
    
    # Análisis
    features = analyzer.get_all_features(sig, config.rpm)
    diagnosis = engine.diagnose(sig)
    
    # Verificar consistencia
    assert len(t) == len(sig), "❌ Inconsistencia tiempo-señal"
    assert features['time_domain']['rms'] > 0, "❌ RMS inconsistente"
    assert diagnosis['confidence'] > 0, "❌ Diagnóstico inconsistente"
    
    print("✓ Consistencia temporal")
    print("✓ Consistencia de análisis")
    print("✓ Consistencia de diagnóstico")
    
    print("\n✅ Consistencia: TODAS LAS PRUEBAS PASARON")


def test_edge_cases():
    """Pruebas de casos extremos"""
    print("\n" + "="*50)
    print("TEST 6: Casos Extremos")
    print("="*50)
    
    analyzer = SignalAnalyzer(10000)
    
    # Prueba 1: Señal constante (sin vibración)
    sig_const = np.ones(1000) * 0.5
    rms = analyzer.calculate_rms(sig_const)
    assert abs(rms - 0.5) < 1e-6, "❌ RMS de constante incorrecto"
    cf = analyzer.calculate_crest_factor(sig_const)
    assert cf == 1.0, "❌ CF de constante debe ser 1"
    print("✓ Señal constante: OK")
    
    # Prueba 2: Señal cero
    sig_zero = np.zeros(1000)
    rms = analyzer.calculate_rms(sig_zero)
    assert rms == 0, "❌ RMS de cero debe ser 0"
    print("✓ Señal cero: OK")
    
    # Prueba 3: Frecuencia muy baja
    gen = SignalGenerator(SignalConfig(rpm=100))  # RPM muy bajo
    t, sig = gen.generate_healthy()
    assert len(sig) > 0, "❌ RPM bajo falla"
    print("✓ RPM muy bajo: OK")
    
    # Prueba 4: Frecuencia muy alta
    gen = SignalGenerator(SignalConfig(rpm=10000))  # RPM muy alto
    t, sig = gen.generate_healthy()
    assert len(sig) > 0, "❌ RPM alto falla"
    print("✓ RPM muy alto: OK")
    
    # Prueba 5: Duración muy corta
    gen = SignalGenerator(SignalConfig(duration=0.1))
    t, sig = gen.generate_healthy()
    assert len(sig) == 1000, "❌ Duración corta inconsistente"
    print("✓ Duración muy corta: OK")
    
    print("\n✅ Casos Extremos: TODAS LAS PRUEBAS PASARON")


def main():
    """Ejecuta todas las pruebas"""
    print("\n" + "█"*50)
    print("█ SUITE DE PRUEBAS - SIMULADOR VIBRACIONAL".ljust(50) + "█")
    print("█"*50)
    
    try:
        test_signal_generator()
        test_signal_analyzer()
        test_fault_simulator()
        test_diagnostic_engine()
        test_consistency()
        test_edge_cases()
        
        print("\n" + "█"*50)
        print("█ ✅ TODAS LAS PRUEBAS PASARON EXITOSAMENTE".ljust(50) + "█")
        print("█"*50 + "\n")
        
        return 0
        
    except AssertionError as e:
        print(f"\n❌ FALLO DE PRUEBA: {e}")
        return 1
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}")
        import traceback
        traceback.print_exc()
        return 2


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
