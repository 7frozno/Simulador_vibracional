# 🚀 Guía Rápida de Inicio - Simulador Vibracional

## 📋 Contenido del Proyecto

Tu simulador tiene la siguiente estructura:

```
analisisVIBRA/
├── src/                          # Módulos principales
│   ├── signal_generator.py       # Generación de señales sintéticas
│   ├── signal_analyzer.py        # Análisis FFT y características
│   ├── fault_simulator.py        # Simulación de fallas
│   ├── diagnostics.py            # Motor de diagnóstico automático
│   └── utils.py                  # Funciones auxiliares
├── app.py                        # Interfaz Streamlit (INICIO RECOMENDADO)
├── examples/
│   └── sample_analysis.py        # Ejemplos de código
├── config.py                     # Configuración
├── requirements.txt              # Dependencias Python
└── README.md                     # Documentación completa
```

## ⚡ Instalación Rápida

### 1. Instalar Dependencias

```bash
cd d:\SIMULADORES\analisisVIBRA
pip install -r requirements.txt
```

**Dependencias principales:**

- numpy, scipy (análisis numérico)
- matplotlib, plotly (visualización)
- streamlit (interfaz gráfica)
- scikit-learn (procesamiento)

### 2. Crear Entorno Virtual (Recomendado)

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

## 🎮 Uso de la Aplicación

### Opción 1: Interfaz Gráfica (RECOMENDADA)

```bash
streamlit run app.py
```

Se abrirá automáticamente en `http://localhost:8501`

**Pasos:**

1. **Pestaña Configuración**: Ajusta RPM, duración, frecuencia de muestreo
2. **Pestaña Simulación**: Selecciona tipo de falla y severidad
3. **Pestaña Análisis**: Visualiza FFT, tendencias temporales y diagnóstico automático

### Opción 2: Ejemplos de Código

```bash
python examples/sample_analysis.py
```

Ejecutará 6 ejemplos completos demostrando:

- Análisis de equipo sano
- Diagnóstico de fallas
- Comparación sano vs defectuoso
- Análisis de severidad
- Análisis espectral detallado
- Simulación de degradación temporal

### Opción 3: Uso Programático

```python
from src.signal_generator import SignalGenerator, SignalConfig
from src.fault_simulator import FaultSimulator, FaultType, FaultSeverity
from src.diagnostics import DiagnosticEngine

# Configurar
config = SignalConfig(rpm=1500, sampling_rate=10000, duration=1.0)

# Generar falla
simulator = FaultSimulator(config)
time, signal = simulator.generate_fault(
    FaultType.UNBALANCE,
    FaultSeverity.MODERATE
)

# Diagnosticar
engine = DiagnosticEngine(config.sampling_rate, config.rpm)
diagnosis = engine.diagnose(signal)

print(f"Falla: {diagnosis['primary_fault'].value}")
print(f"Confianza: {diagnosis['confidence']:.1%}")
print(f"Severidad: {diagnosis['severity_level']}")
```

## 🎯 Funcionalidades Principales

### 1. **Generación de Señales Sintéticas**

5 tipos de falla + equipo sano:

```python
FaultType.HEALTHY           # Equipo sin defectos
FaultType.UNBALANCE         # Desbalance (masa distribuida irregularmente)
FaultType.MISALIGNMENT      # Desalineamiento (ejes no alineados)
FaultType.BEARING           # Falla de rodamiento (defectos en elementosrodantes)
FaultType.CAVITATION        # Cavitación (burbujas colapsando)
```

### 2. **Análisis Espectral**

- **FFT**: Transformada Rápida de Fourier
- **Armónicos**: 1X, 2X, 3X... (múltiplos de RPM)
- **Espectro de Potencia**: Energía por frecuencia
- **Frecuencias Dominantes**: Picos más significativos

### 3. **Características del Dominio del Tiempo**

| Parámetro | Significado | Rango Típico (Sano) |
|-----------|-------------|-------------------|
| **RMS** | Valor eficaz | 0.1 - 0.3 g |
| **Pico** | Máxima amplitud | 0.2 - 0.6 g |
| **Pico-Pico** | Diferencia pico | 0.4 - 1.2 g |
| **Factor Cresta** | Pico/RMS | 2.5 - 4.0 |
| **Kurtosis** | Indice de impactos | ≈ 3.0 |
| **Asimetría** | Sesgo distribución | -1 a +1 |

### 4. **Diagnóstico Automático**

El motor de IA analiza características y determina:

- **Tipo de falla** detectada
- **Nivel de confianza** (0-100%)
- **Severidad** (NORMAL → CRÍTICA)
- **Recomendaciones** de mantenimiento

## 📊 Indicadores por Tipo de Falla

### DESBALANCE

```
✓ 1X DOMINANTE (> 50% energía)
✓ 2X muy baja (< 0.1 / 1X)
✓ Kurtosis ≈ 3-4
✓ Comportamiento lineal con RPM
```

### DESALINEAMIENTO

```
✓ 2X > 1X (invirtiendo relación)
✓ 4X, 6X significativos
✓ Bandas laterales alrededor de armónicos
✓ Kurtosis ≈ 4-5
```

### FALLA DE RODAMIENTO

```
✓ Kurtosis >> 3 (típicamente >8)
✓ Factor de Cresta > 6
✓ Impulsos de alta frecuencia (1-5 kHz) modulados
✓ Espectro con envolvente característica
```

### CAVITACIÓN

```
✓ Ruido de banda ancha
✓ RMS muy elevado (>1.5 g)
✓ Ancho de banda > 3000 Hz
✓ Impulsos aperiódicos
```

## 🔍 Ejemplo Rápido: Detectar Desbalance

```python
from src.signal_generator import SignalConfig
from src.fault_simulator import FaultSimulator, FaultType, FaultSeverity
from src.diagnostics import DiagnosticEngine

# 1. Configurar
config = SignalConfig(rpm=1500, amplitude=1.0, duration=1.0)

# 2. Generar desbalance moderado
simulator = FaultSimulator(config)
time, signal = simulator.generate_fault(FaultType.UNBALANCE, FaultSeverity.MODERATE)

# 3. Diagnosticar
engine = DiagnosticEngine(10000, 1500)
result = engine.diagnose(signal)

# 4. Ver resultado
print("DIAGNÓSTICO:")
print(f"  Falla: {result['primary_fault'].value}")          # desbalance
print(f"  Confianza: {result['confidence']:.1%}")           # ~95%
print(f"  Severidad: {result['severity_level']}")           # MODERADA
print(f"  Acciones: {result['recommendations'][:2]}")       # Qué hacer
```

## 💡 Consejos y Trucos

### Visualización en Temps Real

```bash
# Terminal 1
streamlit run app.py

# Terminal 2 (opcional)
python examples/sample_analysis.py
```

### Ajustar Parámetros para Tu Caso

```python
config = SignalConfig(
    sampling_rate=20000,  # Mayor resolución (defectos pequeños)
    duration=2.0,         # Análisis más largo
    rpm=3600,             # Equipo más rápido (compresor)
    amplitude=2.0         # Mayor amplitud
)
```

### Exportar Resultados

```python
from src.utils import save_analysis_to_json

diagnosis = engine.diagnose(signal)
save_analysis_to_json(diagnosis, 'mi_diagnostico.json')
```

## 🎓 Siguiente Paso: Casos de Estudio

1. **Fase 1**: Familiarizarse con parámetros básicos
   - Ejecutar app.py
   - Generar cada tipo de falla
   - Observar patrones

2. **Fase 2**: Análisis discriminador
   - ¿Cómo diferenciar desbalance de desalineamiento?
   - Ratio 1X/2X es clave
   - Espectro es diferente

3. **Fase 3**: Diagnóstico en cascada
   - Falla combina síntomas
   - Severidad indica urgencia
   - Recomendaciones son específicas

## 📚 Recursos Adicionales

- **README.md**: Documentación completa
- **Docstrings**: Cada función tiene documentación
- **examples/**: 6 ejemplos educativos
- **config.py**: Parámetros configurables

## ❓ Preguntas Frecuentes

**P: ¿Por qué mi diagnóstico no coincide?**
A: Las señales sintéticas son aproximaciones. Ajusta severidad y parámetros.

**P: ¿Puedo usar datos reales?**
A: Sí, carga tu .csv y pásalo a `engine.diagnose(tu_señal)`

**P: ¿Qué RPM debo usar?**
A: Típicos:

- Bombas: 1200-3600 RPM
- Compresores: 3600+ RPM
- Motores: 1500-3600 RPM

**P: ¿Cómo mejoro la precisión del diagnóstico?**
A:

1. Aumenta duración de medición (duration=2-5s)
2. Mejora SNR (snr_db > 30)
3. Calibra con datos reales

## 🚀 Próximos Pasos

```bash
# 1. Instalar
pip install -r requirements.txt

# 2. Explorar interfaz
streamlit run app.py

# 3. Ejecutar ejemplos
python examples/sample_analysis.py

# 4. Personalizar para tu caso
# Edita src/signal_generator.py con tus parámetros
```

---

**¡Bienvenido al análisis vibracional profesional!**

¿Preguntas? Revisa los docstrings del código o los ejemplos incluidos.
