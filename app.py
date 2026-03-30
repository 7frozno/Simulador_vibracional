"""
Aplicación Streamlit para el Simulador de Análisis Vibracional
Interfaz interactiva para simular, analizar y diagnosticar fallas
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path
import sys

# Añadir src al path
sys.path.insert(0, str(Path(__file__).parent))

from src.signal_generator import SignalGenerator, SignalConfig
from src.signal_analyzer import SignalAnalyzer
from src.fault_simulator import FaultSimulator, FaultType, FaultSeverity
from src.diagnostics import DiagnosticEngine
from src.utils import normalize_signal, moving_rms, moving_peak
import config

# Configurar página
st.set_page_config(
    page_title="Simulador Vibracional",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilo CSS personalizado
st.markdown("""
<style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .fault-healthy { color: #2ecc71; font-weight: bold; }
    .fault-light { color: #f39c12; font-weight: bold; }
    .fault-moderate { color: #e74c3c; font-weight: bold; }
    .fault-severe { color: #c0392b; font-weight: bold; }
    .fault-critical { color: #8b0000; font-weight: bold; }
</style>
""", unsafe_allow_html=True)


def initialize_session():
    """Inicializa variables de sesión"""
    if 'signal' not in st.session_state:
        st.session_state.signal = None
    if 'time' not in st.session_state:
        st.session_state.time = None
    if 'diagnosis' not in st.session_state:
        st.session_state.diagnosis = None
    if 'config' not in st.session_state:
        st.session_state.config = SignalConfig()


def plot_waveform(time: np.ndarray, signal: np.ndarray, title: str = "Forma de Onda"):
    """Grafica la forma de onda"""
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=time,
        y=signal,
        mode='lines',
        name='Señal',
        line=dict(color='#1f77b4', width=1)
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Tiempo (s)",
        yaxis_title="Amplitud (g)",
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    
    return fig


def plot_spectrum(frequencies: np.ndarray, spectrum: np.ndarray, 
                 title: str = "Espectro de Frecuencia", max_freq: float = 5000):
    """Grafica el espectro de frecuencia"""
    fig = go.Figure()
    
    # Limitar a frecuencias de interés
    idx = frequencies <= max_freq
    freq_limited = frequencies[idx]
    spec_limited = spectrum[idx]
    
    fig.add_trace(go.Scatter(
        x=freq_limited,
        y=spec_limited,
        mode='lines',
        name='Espectro',
        line=dict(color='#ff7f0e', width=1),
        fill='tozeroy'
    ))
    
    fig.update_layout(
        title=title,
        xaxis_title="Frecuencia (Hz)",
        yaxis_title="Magnitud Normalizada",
        hovermode='x',
        template='plotly_white',
        height=400
    )
    
    return fig


def plot_harmonic_bars(rpm: float, spectrum_dict: dict):
    """Grafica barras de armónicos"""
    f0 = rpm / 60.0
    
    harmonics = []
    values = []
    
    for n in range(1, 8):
        key = f'{n}X_amplitude'
        if key in spectrum_dict:
            harmonics.append(f'{n}X')
            values.append(spectrum_dict[key])
    
    fig = go.Figure(data=[
        go.Bar(
            x=harmonics,
            y=values,
            marker_color=['#e74c3c' if v > 0.3 else '#2ecc71' for v in values]
        )
    ])
    
    fig.update_layout(
        title="Amplitudes Armónicas",
        xaxis_title="Armónico",
        yaxis_title="Amplitud Normalizada",
        template='plotly_white',
        height=300,
        showlegend=False
    )
    
    return fig


def plot_time_series_features(time: np.ndarray, signal: np.ndarray):
    """Grafica características temporales"""
    # Ventana móvil de 1000 muestras
    window_size = min(1000, len(signal) // 10)
    
    rms_values = moving_rms(signal, window_size)
    peak_values = moving_peak(signal, window_size)
    
    # Ajustar tiempo para RMS/PEAK
    time_rms = time[window_size//2:-window_size//2+1][:len(rms_values)]
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=time_rms,
        y=rms_values,
        mode='lines',
        name='RMS Móvil',
        line=dict(color='#2ecc71', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=time_rms,
        y=peak_values,
        mode='lines',
        name='Pico Móvil',
        line=dict(color='#e74c3c', width=2)
    ))
    
    fig.update_layout(
        title="Tendencia Temporal (Ventana Móvil)",
        xaxis_title="Tiempo (s)",
        yaxis_title="Amplitud (g)",
        template='plotly_white',
        height=400,
        hovermode='x unified'
    )
    
    return fig


def main():
    """Función principal de la aplicación"""
    
    # Inicializar sesión
    initialize_session()
    
    # Barra lateral
    st.sidebar.title("⚙️ Configuración")
    
    tab_config, tab_sim, tab_analysis = st.tabs(
        ["Configuración", "Simulación", "Análisis & Diagnóstico"]
    )
    
    # ==================== TAB CONFIGURACIÓN ====================
    with tab_config:
        st.header("Configuración del Simulador")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Parámetros de Señal")
            
            sampling_rate = st.number_input(
                "Frecuencia de Muestreo (Hz)",
                min_value=1000,
                max_value=50000,
                value=10000,
                step=1000
            )
            
            duration = st.number_input(
                "Duración (segundos)",
                min_value=0.1,
                max_value=10.0,
                value=1.0,
                step=0.1
            )
            
            rpm = st.number_input(
                "RPM del Equipo",
                min_value=300,
                max_value=10000,
                value=1500,
                step=100
            )
            
            amplitude = st.number_input(
                "Amplitud Base (g)",
                min_value=0.1,
                max_value=10.0,
                value=1.0,
                step=0.1
            )
        
        with col2:
            st.subheader("Tipo de Equipo")
            
            equipment = st.selectbox(
                "Seleccione equipo",
                list(config.EQUIPMENT_TYPES.keys()),
                format_func=lambda x: config.EQUIPMENT_TYPES[x]['description']
            )
            
            st.info(f"**RPM Típico**: {config.EQUIPMENT_TYPES[equipment]['rpm_typical']}")
            
            st.subheader("Parámetros de Análisis")
            
            fft_max_freq = st.slider(
                "Frecuencia Máxima visualización FFT (Hz)",
                min_value=500,
                max_value=5000,
                value=5000,
                step=500
            )
            
            snr_db = st.slider(
                "Relación Señal-Ruido (dB)",
                min_value=10,
                max_value=50,
                value=30,
                step=5
            )
        
        # Actualizar configuración
        config_obj = SignalConfig(
            sampling_rate=sampling_rate,
            duration=duration,
            rpm=rpm,
            amplitude=amplitude
        )
        st.session_state.config = config_obj
        
        st.success("✓ Configuración actualizada")
    
    # ==================== TAB SIMULACIÓN ====================
    with tab_sim:
        st.header("Generador de Fallas Sintéticas")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("Seleccione Tipo de Falla")
            
            fault_type_name = st.selectbox(
                "Tipo de Falla",
                options=[ft.value for ft in FaultType],
                index=0
            )
            
            # Convertir a enum
            fault_type = FaultType(fault_type_name)
            
            # Mostrar descripción
            fault_sim = FaultSimulator(st.session_state.config)
            fault_info = fault_sim.get_fault_description(fault_type)
            
            if fault_info:
                st.info(f"**{fault_info.get('name', 'N/A')}**\n{fault_info.get('description', '')}")
                
                with st.expander("Ver características y valores típicos"):
                    chars = fault_info.get('characteristics', [])
                    for char in chars:
                        st.write(f"• {char}")
                    
                    st.write("**Valores Típicos:**")
                    for param, value in fault_info.get('typical_values', {}).items():
                        st.write(f"• {param}: {value}")
        
        with col2:
            st.subheader("Severidad")
            
            severity_name = st.select_slider(
                "Nivel de Severidad",
                options=[fs.name for fs in FaultSeverity],
                value="MODERATE"
            )
            
            severity = FaultSeverity[severity_name]
            st.metric("Valor de Severidad", f"{severity.value:.1f}")
        
        # Generar falla
        if st.button("🔄 Generar Señal", key="gen_signal", use_container_width=True):
            with st.spinner("Generando señal sintética..."):
                fault_sim = FaultSimulator(st.session_state.config)
                time, signal = fault_sim.generate_fault(fault_type, severity)
                
                # Añadir ruido
                gen = SignalGenerator(st.session_state.config)
                signal = gen.generate_with_noise(signal, snr_db)
                
                st.session_state.time = time
                st.session_state.signal = signal
                st.session_state.current_fault = fault_type
                
                st.success(f"✓ Señal generada: {len(signal)} muestras")
        
        # Mostrar señal generada
        if st.session_state.signal is not None:
            st.subheader("Forma de Onda Generada")
            
            fig_waveform = plot_waveform(
                st.session_state.time,
                st.session_state.signal,
                f"Señal: {st.session_state.current_fault.value.upper()}"
            )
            st.plotly_chart(fig_waveform, use_container_width=True)
            
            # Estadísticas básicas
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "RMS",
                    f"{np.sqrt(np.mean(st.session_state.signal**2)):.4f} g"
                )
            
            with col2:
                st.metric(
                    "Pico",
                    f"{np.max(np.abs(st.session_state.signal)):.4f} g"
                )
            
            with col3:
                rms = np.sqrt(np.mean(st.session_state.signal**2))
                peak = np.max(np.abs(st.session_state.signal))
                st.metric(
                    "Factor de Cresta",
                    f"{peak/rms if rms > 0 else 0:.2f}"
                )
            
            with col4:
                from scipy.stats import kurtosis
                st.metric(
                    "Kurtosis",
                    f"{kurtosis(st.session_state.signal, fisher=False):.2f}"
                )
    
    # ==================== TAB ANÁLISIS ====================
    with tab_analysis:
        if st.session_state.signal is None:
            st.warning("⚠️ Primero genere una señal en la pestaña 'Simulación'")
        else:
            st.header("Análisis Espectral y Diagnóstico")
            
            # Analizar
            analyzer = SignalAnalyzer(st.session_state.config.sampling_rate)
            freqs, spectrum = analyzer.get_spectrum(
                st.session_state.signal,
                max_freq=fft_max_freq
            )
            
            # Tabs de análisis
            tab_spectrum, tab_harmonics, tab_temporal, tab_diagnosis = st.tabs([
                "Espectro FFT",
                "Armónicos",
                "Análisis Temporal",
                "Diagnóstico"
            ])
            
            with tab_spectrum:
                st.subheader("Análisis Espectral (FFT)")
                
                fig_spectrum = plot_spectrum(
                    freqs,
                    spectrum,
                    f"Espectro de Frecuencia", 
                    max_freq=fft_max_freq
                )
                st.plotly_chart(fig_spectrum, use_container_width=True)
                
                # Frecuencias dominantes
                dom_freqs, dom_mags = analyzer.get_dominant_frequencies(
                    st.session_state.signal,
                    n_peaks=5
                )
                
                st.subheader("Frecuencias Dominantes")
                
                col_freq_content = st.columns(5)
                for i, (freq, mag) in enumerate(zip(dom_freqs, dom_mags)):
                    with col_freq_content[i % 5]:
                        st.metric(f"#{i+1}", f"{freq:.1f} Hz", f"{mag:.4f} mag")
            
            with tab_harmonics:
                st.subheader("Análisis de Armónicos")
                
                freq_features = analyzer.get_frequency_domain_features(
                    st.session_state.signal,
                    st.session_state.config.rpm
                )
                
                fig_harmonics = plot_harmonic_bars(
                    st.session_state.config.rpm,
                    freq_features
                )
                st.plotly_chart(fig_harmonics, use_container_width=True)
                
                # Tabla de armónicos
                st.subheader("Tabla de Amplitudes")
                
                harmonic_data = []
                f0 = st.session_state.config.rpm / 60.0
                
                for n in range(1, 8):
                    key = f'{n}X_amplitude'
                    amp = freq_features.get(key, 0)
                    freq_val = n * f0
                    harmonic_data.append({
                        'Armónico': f'{n}X',
                        'Frecuencia (Hz)': f'{freq_val:.2f}',
                        'Amplitud': f'{amp:.4f}',
                        'Estado': '🔴 Alto' if amp > 0.3 else '🟡 Moderado' if amp > 0.1 else '🟢 Bajo'
                    })
                
                st.dataframe(harmonic_data, use_container_width=True)
            
            with tab_temporal:
                st.subheader("Análisis de Tendencia Temporal")
                
                fig_temporal = plot_time_series_features(
                    st.session_state.time,
                    st.session_state.signal
                )
                st.plotly_chart(fig_temporal, use_container_width=True)
                
                # Características de tiempo
                st.subheader("Características del Dominio del Tiempo")
                
                time_features = analyzer.get_time_domain_features(
                    st.session_state.signal
                )
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("RMS (g)", f"{time_features['rms']:.4f}")
                    st.metric("Pico (g)", f"{time_features['peak']:.4f}")
                    st.metric("Pico-Pico (g)", f"{time_features['peak_to_peak']:.4f}")
                
                with col2:
                    st.metric("Crest Factor", f"{time_features['crest_factor']:.2f}")
                    st.metric("Kurtosis", f"{time_features['kurtosis']:.2f}")
                    st.metric("Asimetría", f"{time_features['skewness']:.2f}")
                
                with col3:
                    st.metric("Media", f"{time_features['mean']:.4f}")
                    st.metric("Desv. Estándar", f"{time_features['std']:.4f}")
                    st.metric("Varianza", f"{time_features['variance']:.4f}")
            
            with tab_diagnosis:
                st.subheader("🔍 Diagnóstico Automático")
                
                if st.button("🤖 Ejecutar Diagnóstico", use_container_width=True):
                    with st.spinner("Analizando falla..."):
                        engine = DiagnosticEngine(
                            st.session_state.config.sampling_rate,
                            st.session_state.config.rpm
                        )
                        diagnosis = engine.diagnose(st.session_state.signal)
                        st.session_state.diagnosis = diagnosis
                
                if st.session_state.diagnosis is not None:
                    diagnosis = st.session_state.diagnosis
                    
                    # Resultado principal
                    primary_fault = diagnosis['primary_fault']
                    confidence = diagnosis['confidence']
                    severity = diagnosis['severity_level']
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        fault_name = primary_fault.value.upper()
                        st.markdown(
                            f"### 🎯 Falla Detectada\n**{fault_name}**",
                            unsafe_allow_html=True
                        )
                    
                    with col2:
                        st.metric("Confianza", f"{confidence:.1%}")
                    
                    with col3:
                        color_map = {
                            'NORMAL': '🟢',
                            'LEVE': '🟡',
                            'MODERADA': '🟠',
                            'SEVERA': '🔴',
                            'CRÍTICA': '⚫'
                        }
                        icon = color_map.get(severity, '❓')
                        st.metric("Severidad", f"{icon} {severity}")
                    
                    # Scores de todas las fallas
                    st.subheader("Scores de Diagnóstico para Todas las Fallas")
                    
                    scores = diagnosis['all_scores']
                    score_data = [
                        {
                            'Tipo de Falla': ft.value.upper(),
                            'Score': f"{scores[ft]:.1%}",
                            'Confianza': '█' * int(scores[ft] * 10) + '░' * (10 - int(scores[ft] * 10))
                        }
                        for ft in FaultType
                    ]
                    
                    st.dataframe(score_data, use_container_width=True)
                    
                    # Recomendaciones
                    st.subheader("📋 Recomendaciones")
                    
                    recommendations = diagnosis['recommendations']
                    for i, rec in enumerate(recommendations, 1):
                        st.write(f"{i}. {rec}")
                    
                    # Análisis detallado
                    with st.expander("Ver Análisis Detallado"):
                        st.text(diagnosis['analysis'])
                    
                    # Indicadores clave
                    st.subheader("Indicadores Clave por Tipo de Falla")
                    
                    fault_sim = FaultSimulator(st.session_state.config)
                    indicators = fault_sim.get_fault_indicators(primary_fault)
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.write("**Indicador Primario:**")
                        st.write(f"```{indicators.get('primary', 'N/A')}```")
                    
                    with col2:
                        st.write("**Indicador Secundario:**")
                        st.write(f"```{indicators.get('secondary', 'N/A')}```")
                    
                    with col3:
                        st.write("**Indicador Terciario:**")
                        st.write(f"```{indicators.get('tertiary', 'N/A')}```")


if __name__ == "__main__":
    main()
