# Simulador de Análisis Vibracional

Un simulador profesional para análisis de vibraciones en bombas y otros equipos rotativos, diseñado para practicar con datos sintéticos que simulan casos reales.

## 🎯 Características

### Análisis Espectral

- **FFT (Fast Fourier Transform)**: Análisis completo del espectro de frecuencias
- **Espectrograma**: Visualización tiempo-frecuencia
- **Densidad Espectral de Potencia (PSD)**: Análisis energético

### Análisis Temporal

- **RMS (Root Mean Square)**: Valor eficaz de la vibración
- **Pico y Pico-Pico**: Amplitudes máximas
- **Factor de Cresta**: Indicador de impactos
- **Kurtosis**: Detecta transitorios e impactos
- **Asimetría**: Características de distribución

### Tipos de Falla Simulables

#### 1. **Desbalance**

- Distribución no uniforme de masa
- Dominancia clara en 1X
- Bajo contenido de 2X
- *Patrón:* Componente sincrónica fuerte

#### 2. **Desalineamiento**

- Desaligne axial/angular entre ejes
- Amplificación de armónicos pares (2X, 4X, 6X)
- Bandas laterales significativas
- *Patrón:* 2X > 1X, armónicos pares dominantes

#### 3. **Falla de Rodamiento**

- Defectos en pistas o elementos rodantes
- Impulsos de alta frecuencia modulados
- Kurtosis muy elevada (>8)
- Factor de cresta alto (>6)
- *Patrón:* Impactos periódicos con envolvente

#### 4. **Cavitación**

- Formación y colapso de burbujas
- Ruido de banda ancha
- RMS muy elevado
- Rápido deterioro
- *Patrón:* Espectro extendido, impulsos aleatorios

#### 5. **Equipo Sano**

- Funcionamiento normal
- Bajos niveles de vibración
- Espectro limpio
- Kurtosis cercana a 3
- *Patrón:* Componentes armónicas definidas

## 🚀 Instalación

1. **Clonar o descargar el repositorio**

```bash
cd analisisVIBRA
```

1. **Crear entorno virtual (opcional pero recomendado)**

```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

1. **Instalar dependencias**

```bash
pip install -r requirements.txt
```

## 📊 Uso

### Interfaz Gráfica (Streamlit)

Ejecutar la aplicación interactiva:

```bash
streamlit run app.py
```

La aplicación se abrirá en `http://localhost:8501`

### Uso Programático

```python
from src.signal_generator import SignalGenerator, SignalConfig
from src.signal_analyzer import SignalAnalyzer
from src.fault_simulator import FaultSimulator, FaultType, FaultSeverity
from src.diagnostics import DiagnosticEngine

# Configurar
config = SignalConfig(
    sampling_rate=10000,
    duration=1.0,
    rpm=1500,
    amplitude=1.0
)

# Generar señal con falla
fault_sim = FaultSimulator(config)
time, signal = fault_sim.generate_fault(
    FaultType.UNBALANCE, 
    FaultSeverity.MODERATE
)

# Analizar
analyzer = SignalAnalyzer(config.sampling_rate)
features = analyzer.get_all_features(signal, config.rpm)

# Diagnosticar
engine = DiagnosticEngine(config.sampling_rate, config.rpm)
diagnosis = engine.diagnose(signal)

print(f"Falla detectada: {diagnosis['primary_fault'].value}")
print(f"Confianza: {diagnosis['confidence']:.2%}")
print(f"Severidad: {diagnosis['severity_level']}")
```

## 📈 Interpretación de Resultados

### Indicadores Clave por Tipo de Falla

| Parámetro | Desbalance | Desalineamiento | Rodamiento | Cavitación |
|-----------|-----------|-----------------|-----------|-----------|
| **1X** | Muy Alto | Moderado | Bajo | Muy Bajo |
| **2X** | Muy Bajo | Muy Alto | Bajo | Bajo |
| **Kurtosis** | ~3.5 | ~4-5 | >8 | 4-7 |
| **CF** | 3-4 | 3-4.5 | >6 | 4-7 |
| **RMS** | 0.5-1.5g | 0.4-1.5g | 1-3g | 1-3g |

### Niveles de Severidad

- **NORMAL**: RMS < 0.3g, Kurtosis ≈ 3
- **LEVE**: RMS 0.3-0.5g, Indicios leves
- **MODERADA**: RMS 0.5-1.5g, Falla claramente detectable
- **SEVERA**: RMS 1.5-2.5g, Requiere atención inmediata
- **CRÍTICA**: RMS > 2.5g, Riesgo de fallo inminente

## 📁 Estructura del Proyecto

```
analisisVIBRA/
├── src/
│   ├── __init__.py
│   ├── signal_generator.py      # Generación de señales sintéticas
│   ├── signal_analyzer.py       # Análisis FFT y características
│   ├── fault_simulator.py       # Simulación de tipos de falla
│   ├── diagnostics.py           # Motor de diagnóstico automático
│   └── utils.py                 # Funciones auxiliares
├── app.py                        # Interfaz Streamlit
├── config.py                     # Configuración del simulador
├── requirements.txt              # Dependencias
├── README.md                     # Este archivo
├── examples/
│   └── sample_analysis.py        # Ejemplo de uso
└── data/
    └── (archivos de datos análisis)
```

## 🔬 Ejemplos Educativos

El simulador es ideal para:

✅ **Estudiantes de Ingeniería Mecánica/Mantenimiento**

- Entender diagnóstico vibracional sin equipos costosos
- Practicar con datos realistas

✅ **Técnicos de Mantenimiento**

- Entrenar en identificación de fallas
- Desarrollo de habilidades de diagnóstico

✅ **Investigadores**

- Validar algoritmos de diagnóstico
- Generar datasets sintéticos

✅ **Consultores**

- Presentar casos a clientes
- Demonstraciones educativas

## 📖 Conceptos Teóricos

### Factor de Cresta (Crest Factor)

```
CF = (Valor Pico) / (RMS)
```

- **CF < 4**: Señal más con contenido periódico
- **CF 4-6**: Presencia moderada de impactos
- **CF > 6**: Impactos significativos (falla probable)

### Kurtosis

```
Segunda medida estadística del pico de una distribución
```

- **K ≈ 3.0**: Distribución normal (equipo sano)
- **K 4-6**: Indicios de impactos leves
- **K > 8**: Impactos severos (falla de rodamiento probable)

### Análisis Armónico

- **1X**: Frecuencia fundamental (RPM/60)
- **2X, 3X, etc.**: Armónicos superiores

## 🎓 Nivel de Experiencia Recomendado

- **Principiante**: Familiarizarse con parámetros básicos (RMS, pico)
- **Intermedio**: Análisis espectral, detección de patrones (OBJETIVO)
- **Avanzado**: Algoritmos de diagnóstico, análisis de envolvente

## ⚠️ Limitaciones

- Simulaciones sintéticas (no reemplazan datos reales)
- No incluye factores transitorios complejos
- RPM fijo (no varía con carga)

## 🔧 Personalización

### Crear tipo de falla personalizado

```python
# En fault_simulator.py
def generate_custom_fault(self):
    t, signal = self.generator.generate_healthy()
    # Añadir componentes personalizados
    f0 = self.frequency_fundamental
    signal += 0.5 * np.sin(2 * np.pi * f0 * 7.5 * t)  # 7.5X
    return t, signal
```

### Ajustar parámetros de señal

```python
config = SignalConfig(
    sampling_rate=20000,  # Mayor resolución frecuencial
    duration=2.0,         # Análisis más largo
    rpm=3600,             # Equipo más rápido
    amplitude=2.0         # Mayor amplitud
)
```

## 📞 Soporte

Para problemas o suggestions:

1. Revisar ejemplos en `examples/`
2. Consultar docstrings en código
3. Experimentar con diferentes parámetros

## 📝 Licencia

Este proyecto está disponible para uso educativo y de investigación.

---

**Versión**: 1.0.0  
**Última actualización**: 2026-02-22  
**Autor**: Simulador Vibracional v1.0
