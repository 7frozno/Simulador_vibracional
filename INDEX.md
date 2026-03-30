doc # 📑 ÍNDICE - Simulador de Análisis Vibracional

## 🎯 Resumen del Proyecto

Tu simulador de **Análisis Vibracional** para bombas y equipos rotativos está **100% completado**.

Es un sistema profesional diseñado para:

- ✅ Generar señales sintéticas realistas
- ✅ Analizar espectro de frecuencia (FFT)
- ✅ Detectar 5 tipos de falla automáticamente
- ✅ Diagnosticar con algoritmo inteligente
- ✅ Mostrar tendencias temporales
- ✅ Interfaz gráfica interactiva

---

## 📂 Estructura del Proyecto

```
analisisVIBRA/
│
├── 🚀 INICIO RÁPIDO
│   ├── QUICK_START.md            ← 🔥 LEE ESTO PRIMERO (5 min)
│   ├── setup.py                  ← Instalación automática
│   └── run.py                    ← Script de prueba rápida
│
├── 💻 CÓDIGO PRINCIPAL
│   ├── app.py                    ← Interfaz Streamlit (EJECUTAR)
│   ├── config.py                 ← Configuración global
│   ├── requirements.txt           ← Dependencias Python
│   │
│   └── src/                       ← Módulos principales
│       ├── __init__.py
│       ├── signal_generator.py   ← Generador de señales (6 tipos)
│       ├── signal_analyzer.py    ← Análisis FFT y características
│       ├── fault_simulator.py    ← Simulador de 5 tipos de falla
│       ├── diagnostics.py        ← Motor de diagnóstico automático
│       └── utils.py              ← Funciones auxiliares
│
├── 📚 DOCUMENTACIÓN COMPLETA
│   ├── README.md                 ← Documentación principal
│   ├── QUICK_START.md            ← Guía de inicio rápido
│   ├── CASOS_ESTUDIO.md          ← 5 casos educativos detallados
│   ├── REFERENCIA_TECNICA.md     ← Formulas y conceptos teóricos
│   ├── SOLUCION_PROBLEMAS.md     ← FAQ y troubleshooting
│   └── INTEGRACION_SENSORES.md   ← 🔌 FUTURO: Guía completa para sensores reales
│
├── 📖 EJEMPLOS Y PRUEBAS
│   ├── examples/
│   │   └── sample_analysis.py    ← 6 ejemplos ejecutables
│   │
│   ├── tests.py                  ← Suite de pruebas (validación)
│   │
│   └── data/                     ← Carpeta para datos futuros
│
└── ⚙️ SCRIPTS AUXILIARES
    ├── setup.py                  ← Configuración inicial
    └── run.py                    ← Launcher rápido
```

---

## 🎮 Cómo Comenzar (3 Pasos)

### Paso 1️⃣ - Instalar (2 minutos)

```bash
cd d:\SIMULADORES\analisisVIBRA
pip install -r requirements.txt
```

### Paso 2️⃣ - Ejecutar la App (1 minuto)

```bash
streamlit run app.py
```

Se abrirá en: `http://localhost:8501`

### Paso 3️⃣ - Usar

1. **Pestaña "Configuración"**: Ajusta RPM, duración, tipo de equipo
2. **Pestaña "Simulación"**: Selecciona falla y severidad → Genera señal
3. **Pestaña "Análisis"**: Visualiza FFT, armónicos, diagnóstico automático

---

## 📖 Documentación por Tema

### Para Comenzar

- **QUICK_START.md** (5 min) - Lo básico
- **CASOS_ESTUDIO.md** - Ejemplos reales con solución
- **examples/sample_analysis.py** - Código de ejemplo

### Para Entender la Teoría

- **REFERENCIA_TECNICA.md** - Fórmulas, conceptos, normativas
- **README.md** - Características detalladas
- Docstrings en el código

### Para Resolver Problemas

- **SOLUCION_PROBLEMAS.md** - FAQ y troubleshooting
- **tests.py** - Validación del sistema
- **REFERENCIA_TECNICA.md** - Sección de unidades

---

## 🎯 Funcionalidades Por Tipo de Falla

### 1. **DESBALANCE** (Distribución desigual de masa)

```
Indicador: 1X ELEVADO, 2X BAJO
Tipo FF: Sano vs Defectuoso
Equipo: Claramente diagnosticable
Tiempo de Fallo: 200-300h sin acción
```

### 2. **DESALINEAMIENTO** (Ejes no paralelos)

```
Indicador: 2X > 1X, Armónicos pares
Tipo: Más lento a progresar
Equipo: Detectable en FFT
Tiempo de Fallo: 500-1000h
```

### 3. **FALLA RODAMIENTO** (Defecto en bolas/pistas)

```
Indicador: Kurtosis >>3, CF >6
Tipo: Más urgente
Equipo: CRÍTICO si detectado
Tiempo de Fallo: 50-200h
```

### 4. **CAVITACIÓN** (Burbujas colapsando)

```
Indicador: Ruido ancho, RMS alto
Tipo: Genera daño rápido
Equipo: Requiere intervención hidráulica
Tiempo de Fallo: Rápido
```

### 5. **COMBINADA** (Múltiples defectos)

```
Indicador: Síntomas mixtos, Kurtosis muy alta
Tipo: Compleja de diagnosticar
Equipo: Requiere análisis cuidadoso
Tiempo de Fallo: Variable, generalmente rápido
```

---

## 📊 Matriz de Diagnóstico Rápida

| Síntoma | Desbalance | Desalin. | Rodamient. | Cavitación |
|---------|------------|----------|-----------|------------|
| **1X/2X** | >> 1 | << 1 | Bajo | Muy bajo |
| **Kurtosis** | ~3 | 4-5 | >> 8 | 5-8 |
| **CF** | 3-4 | 3-4 | > 6 | 4-7 |
| **Acción** | Balanceo | Alineación | Reemplazo | Mantenim. |

---

## 🔬 Módulos del Sistema

### `signal_generator.py` - Generador de Señales

```python
SignalGenerator.generate_healthy()      # Equipo normal
SignalGenerator.generate_unbalance()    # Desbalance
SignalGenerator.generate_misalignment() # Alineamiento
SignalGenerator.generate_beating_fault()# Rodamiento
SignalGenerator.generate_cavitation()   # Cavitación
```

### `signal_analyzer.py` - Análisis

```python
SignalAnalyzer.calculate_fft()         # Transformada Fourier
SignalAnalyzer.calculate_rms()         # Valor eficaz
SignalAnalyzer.calculate_kurtosis()    # Índice impactos
SignalAnalyzer.get_all_features()      # Todas características
```

### `fault_simulator.py` - Fallas

```python
FaultSimulator.generate_fault()         # Genera con severidad
FaultSimulator.get_fault_description()  # Info sobre falla
FaultSimulator.get_fault_indicators()   # Indicadores clave
```

### `diagnostics.py` - Diagnóstico

```python
DiagnosticEngine.diagnose()             # Análisis completo
# Retorna: falla, confianza, severidad, recomendaciones
```

---

## 🚀 Casos de Uso

### 1. **Educación e Inherencia**

Perfecto para estudiantes de ingeniería y técnicos de mantenimiento

```bash
streamlit run app.py
# Jugar con diferentes fallas y severidades
```

### 2. **Entrenamiento Enfocado**

Aprender a reconocer patrones vibratorios

```bash
python examples/sample_analysis.py
# 6 ejemplos que muestran cada concepto
```

### 3. **Desarrollo de Algoritmos**

Base para crear clasificadores propios

```python
from src.signal_analyzer import SignalAnalyzer
from src.diagnostics import DiagnosticEngine
# Personalizar y extender
```

### 4. **Adaptación a Otros Equipos**

Fácil de ajustar para compresores, ventiladores, etc.

```python
# En config.py, agregar equipos
EQUIPMENT_TYPES = {
    'compresor': {'rpm_typical': 3600, ...},
    'ventilador': {'rpm_typical': 1200, ...},
}
```

---

## 📋 Checklist de Instalación

- [ ] Python 3.8+ instalado
- [ ] Carpeta `analisisVIBRA` creada
- [ ] `pip install -r requirements.txt` ejecutado
- [ ] `streamlit run app.py` funciona
- [ ] Interfaz se abre en navegador
- [ ] `python tests.py` pasa todas pruebas ✅
- [ ] `python examples/sample_analysis.py` se ejecuta
- [ ] ¡Listo para usar!

---

## ⚡ Atajos Útiles

```bash
# Instalar
pip install -r requirements.txt

# Ejecutar app
streamlit run app.py

# Ejecutar ejemplos
python examples/sample_analysis.py

# Validar
python tests.py

# Configuración
python setup.py

# En Python
from src import SignalGenerator, FaultSimulator, DiagnosticEngine
```

---

## 🎓 Ruta de Aprendizaje Recomendada

**Semana 1: Conceptos Básicos** (3 horas)

1. Leer: QUICK_START.md
2. Ejecutar: app.py
3. Jugar con parámetros básicos
4. Leer: REFERENCIA_TECNICA.md (secciones 1-3)

**Semana 2: Diagnóstico** (4 horas)

1. Estudiar: CASOS_ESTUDIO.md
2. Ejecutar: examples/sample_analysis.py
3. Aprender a diferenciar fallas
4. Práctica con la app

**Semana 3: Uso Avanzado** (3 horas)

1. Leer: README.md completo
2. Personalizar generador de señales
3. Crear función para grabar/cargar datos
4. Integrar con datos reales (opcional)

---

## 🔧 Personalización

### Añadir Nuevo Equipo

En `config.py`:

```python
EQUIPMENT_TYPES = {
    'mi_equipo': {
        'rpm_typical': 2000,
        'description': 'Mi máquina personalizada'
    }
}
```

### Cambiar Severidad

En `fault_simulator.py`:

```python
def generate_custom():
    _, signal = self.generator.generate_healthy()
    signal += 0.7 * np.sin(...)  # Ajustar factor
    return signal
```

### Usar Datos Reales

En tu código:

```python
import pandas as pd
datos = pd.read_csv('mi_ventilador.csv')
signal = datos['vibracion'].values
diagnosis = engine.diagnose(signal)
```

---

## 📞 Soporte Rápido

| Problema | Solución |
|----------|----------|
| No instala | `pip install --upgrade pip` luego retry |
| App lenta | Reducir `sampling_rate` o `duration` |
| Diagnóstico equivocado | Aumentar `FaultSeverity` |
| Módulo no encontrado | Ejecutar desde carpeta correcta |
| Error de puerto | `streamlit run app.py --server.port 8502` |

Más detalles: **SOLUCION_PROBLEMAS.md**

---

## 📊 Estadísticas del Proyecto

| Métrica | Valor |
|---------|-------|
| Líneas de código | ~2,500 |
| Módulos | 6 principales |
| Tipos de falla | 5 + 1 combinada |
| Características analizadas | 15+ |
| Documentación | 4,000+ líneas |
| Ejemplos | 6 executables |
| Pruebas automatizadas | 30+ validaciones |

---

## 🎯 Próximas Mejoras Opcionales

Aquí está el simulador base. Mejoras futuras podrían incluir:

1. **Análisis de Envolvente** - Detectar falla rodamiento más temprano
2. **Machine Learning** - Clasificador de red neuronal
3. **Análisis Tiempo-Frecuencia** - Espectrograma wavelet
4. **Tendencia Histórica** - Seguimiento de degradación
5. **Exportación de Reportes** - PDF con análisis completo
6. **Modelos 3D** - Visualización de vibraciones
7. **API REST** - Para integración con sistemas
8. **Base de datos** - Guardar análisis históricos

---

## 🔌 Integración con Sensores Reales (Para Futuro)

**📄 Documento completo disponible**: `INTEGRACION_SENSORES.md`

Este documento contiene guías y código listo para adaptar el simulador a un sistema real de:

✅ **Interfaz de Sensores**

- Clase base `SensorInterface` para cualquier tipo de sensor
- Implementaciones específicas: USB, WiFi, DAQ
- Manejo de errores y conexión robusta

✅ **Recolección en Tiempo Real**

- `RealtimeDataCollector` con threading
- Procesamiento automático de ventanas de datos
- Callbacks para eventos de análisis

✅ **Almacenamiento en Base de Datos**

- SQLite schema completo
- Tabla de mediciones, dispositivos y alertas
- Historial y tendencias

✅ **Sistema de Alertas**

- Alertas por email (SMTP)
- Notificaciones SMS (Twilio)
- Escalado automático por severidad

✅ **Dashboard Multi-Dispositivo**

- Monitoreo de múltiples bombas/compresores simultáneamente
- Vista de resumen, historial y alertas
- Configuración de dispositivos

**Cuándo usar INTEGRACION_SENSORES.md:**

- [ ] Tengo sensor acelerómetro físico
- [ ] Necesito monitorear equipo en producción real
- [ ] Quiero almacenar datos históricos
- [ ] Requiero sistema de alertas automáticas
- [ ] Monitoreando múltiples máquinas simultáneamente

**Contenido Disponible:**

1. **Paso 1**: Clase base SensorInterface + 3 tipos específicos
2. **Paso 2**: RealtimeDataCollector con threading
3. **Paso 3**: Base de datos con SQLite
4. **Paso 4**: Sistema de alertas por email/SMS
5. **Paso 5**: Dashboard Streamlit multi-dispositivo
6. **Bonus**: Configuración completa y scripts de inicio

---

## ✅ Checklist Final

- [x] Generación de 5 tipos de falla + sano
- [x] Análisis espectral (FFT)
- [x] Cálculo de características (RMS, pico, kurtosis, CF)
- [x] Comparación sano vs defectuoso
- [x] Motor de diagnóstico automático
- [x] Tendencias temporales (RMS/pico móvil)
- [x] Interfaz gráfica con Streamlit
- [x] Documentación completa
- [x] Ejemplos ejecutables
- [x] Suite de pruebas
- [x] Solución de problemas

---

## 🎉 ¡LISTO PARA USAR

```bash
# 1. Navegar a la carpeta
cd d:\SIMULADORES\analisisVIBRA

# 2. Instalar dependencias (si no lo hiciste)
pip install -r requirements.txt

# 3. Ejecutar la app
streamlit run app.py

# ¡Disfruta tu simulador profesional!
```

---

**Simulador de Análisis Vibracional v1.0**  
*Diseñado para análisis educativo y diagnóstico de bombas y equipos rotativos*  
*Datos sintéticos realistas con fidelidad comparable a casos reales*
