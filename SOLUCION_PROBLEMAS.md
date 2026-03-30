# 🔧 Solución de Problemas - Simulador Vibracional

## Instalación y Configuración

### Problema: "ModuleNotFoundError: No module named 'streamlit'"

**Causa:** Dependencias no instaladas

**Solución:**

```bash
# Opción 1: Instalar todas las dependencias
pip install -r requirements.txt

# Opción 2: Instalar solo lo que falta
pip install streamlit plotly scipy numpy pandas matplotlib scikit-learn

# Opción 3: Usar entorno virtual
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
```

### Problema: "Python version not compatible"

**Causa:** Versión de Python < 3.8

**Solución:**

```bash
# Verificar versión
python --version

# Si está desactualizada, descargar de:
# https://www.python.org/downloads/
# Se requiere Python 3.8+
```

### Problema: "Path/Ruta no encontrada" al ejecutar app.py

**Causa:** Ejecutar desde directorio incorrecto

**Solución:**

```bash
# Navegar a la carpeta del proyecto
cd d:\SIMULADORES\analisisVIBRA

# Ejecutar desde ahí
streamlit run app.py

# O usar ruta completa
streamlit run d:\SIMULADORES\analisisVIBRA\app.py
```

### Problema: "Port 8501 already in use"

**Causa:** Streamlit ya está ejecutándose en ese puerto

**Solución:**

```bash
# Opción 1: Usar puerto diferente
streamlit run app.py --server.port 8502

# Opción 2: Matar el proceso anterior
# Windows:
taskkill /IM streamlit.exe

# Linux/Mac:
pkill -f streamlit

# Opción 3: Esperar a que se cierre
# (Streamlit se cierra automáticamente si no se accede por 5 min)
```

---

## Errores de Ejecución

### Problema: "ValueError: x and y must have same length"

**Causa:** Las arrays de tiempo y señal no tienen la misma longitud

**Posible solución:**

```python
# Asegurarse que la configuración es consistente
config = SignalConfig(
    sampling_rate=10000,
    duration=1.0  # segundos
)
# Debe generar exactamente 10000 muestras
```

### Problema: FFT da valores muy grandes

**Causa:** Amplitud de entrada excesiva o configuración incorrecta

**Solución:**

```python
# Verificar amplitud
config = SignalConfig(amplitude=1.0)  # No usar > 2.0

# Verificar que la señal no contenga NaN
signal = np.nan_to_num(signal, nan=0.0)

# Normalizar si es necesario
signal = signal / np.max(np.abs(signal))
```

### Problema: Diagnóstico siempre devuelve la misma falla

**Causa:** Parámetros de entrada incorrectos o sigma baja

**Solución:**

```python
# Aumentar diferencia entre fallas
fault_sim = FaultSimulator(config)

# Usar severidad más clara
_, sig1 = fault_sim.generate_fault(FaultType.UNBALANCE, FaultSeverity.SEVERE)
_, sig2 = fault_sim.generate_fault(FaultType.BEARING, FaultSeverity.SEVERE)

# Ahora las diferencias deben ser claras
```

---

## Problemas de Precisión

### Problema: El diagnóstico no detecta mi falla

**Causa Posible 1: Severidad muy baja**

```python
# Incrementar severidad
_, signal = fault_sim.generate_fault(
    FaultType.BEARING,
    FaultSeverity.SEVERE  # No MILD
)
```

**Causa Posible 2: SNR muy bajo**

```python
# Aumentar relación señal-ruido
gen = SignalGenerator(config)
signal = gen.generate_with_noise(signal, snr_db=40)  # No 10
```

**Causa Posible 3: Parámetros RPM inconsistentes**

```python
# Verificar consistencia
config = SignalConfig(rpm=1500)
engine = DiagnosticEngine(sampling_rate=10000, rpm=1500)  # Mismo RPM
```

### Problema: RMS muy alto o muy bajo

**Diagnóstico:**

```python
# Verificar amplitud usada
analyzer = SignalAnalyzer(10000)
rms = analyzer.calculate_rms(signal)
print(f"RMS actual: {rms:.6f} g")

# Comparar con típicos
if rms > 5:
    print("⚠️ Amplitud excesiva en configuración")
elif rms < 0.01:
    print("⚠️ Amplitud muy baja")
```

---

## Problemas Visuales

### Problema: "No module named 'plotly'" en la app

**Causa:** Plotly no instalado en el entorno usado por Streamlit

**Solución:**

```bash
# Reinstalar explícitamente
pip install --upgrade plotly

# O usar matplotlib en su lugar (requiere editar app.py)
# Buscar: "st.plotly_chart" 
# Reemplazar con: "st.pyplot(fig)"
```

### Problema: Los gráficos se ven pixelados

**Solución:**
En **app.py**, aumentar DPI:

```python
st.set_page_config(
    page_title="...",
    initial_sidebar_state="expanded"
    # Agregar:
    # page_icon="📊",
    # layout="wide"
)
```

### Problema: La app es muy lenta

**Causas y soluciones:**

1. **Muestreo muy alto (>20 kHz)**

   ```python
   config = SignalConfig(sampling_rate=10000)  # Reducir a esto
   ```

2. **Duración muy larga (>10s)**

   ```python
   config = SignalConfig(duration=1.0)  # Usar máximo 2-3s
   ```

3. **FFT con muchos puntos**
   - Es normal que FFT sea lento
   - No aumentar más de 2048 puntos

4. **Limite de memoria**

   ```bash
   # Reiniciar Streamlit
   streamlit run app.py --logger.level=debug
   ```

---

## Problemas de Datos

### Problema: "Division by zero" en análisis

**Ubicación:** `signal_analyzer.py` - `calculate_crest_factor`

**Solución automática:** Ya está manejado en el código

```python
return peak / rms if rms > 0 else 0
```

### Problema: Señal contiene valores infinitos (inf) o no-números (nan)

**Diagnóstico:**

```python
import numpy as np

# Verificar
print(f"NaN: {np.isnan(signal).any()}")
print(f"Inf: {np.isinf(signal).any()}")

# Limpiar
signal = np.nan_to_num(signal, nan=0.0, posinf=1e10, neginf=-1e10)
```

### Problema: Frecuencias negativas en espectro

**Causa:** FFT incluye frecuencias negativas por defecto

**Solución:** Ya está implementada en `get_spectrum()`

```python
# El código filtra automáticamente
positive_idx = self.frequencies >= 0
return self.frequencies[positive_idx], self.fft_magnitude[positive_idx]
```

---

## Problemas Avanzados

### Cómo extender el simulador

**1. Añadir nuevo tipo de falla:**

```python
# En fault_simulator.py, agregar a FaultType enum:
class FaultType(Enum):
    # ... existentes ...
    CUSTOM = "mi_falla"

# Agregar método generador:
def generate_custom_fault(self, severity: float = 1.0):
    t, signal = self.generator.generate_healthy()
    f0 = self.frequency_fundamental
    
    # Agregar tu lógica aquí
    signal += 0.5 * severity * np.sin(...)
    
    return t, signal

# Actualizar generate_fault():
elif fault_type == FaultType.CUSTOM:
    return self.generate_custom_fault(severity=severity_value)
```

**2. Personalizar umbral de diagnóstico:**

```python
# En diagnostics.py, modificar scores:
def _score_bearing(self, time_feat, freq_feat):
    score = 0.0
    kurtosis = time_feat['kurtosis']
    
    # Ajustar sensibilidad aquí
    if kurtosis > 6:  # Reducir de 8 para más sensibilidad
        score += 0.8
```

### Problema: Necesito usar datos reales

**Solución:**

```python
import numpy as np
import pandas as pd
from src.signal_analyzer import SignalAnalyzer
from src.diagnostics import DiagnosticEngine

# Cargar datos  
datos = pd.read_csv('mi_vibration.csv')
# Esperado: columnas = [tiempo, aceleración_x, aceleración_y, aceleración_z]

# Usar una componente (ej: X)
signal = datos['aceleracion_x'].values

# Análisis
analyzer = SignalAnalyzer(sampling_rate=10000)  # Ajustar a tu fs actual
features = analyzer.get_all_features(signal, rpm=1500)  # Ajustar RPM

# Diagnóstico
engine = DiagnosticEngine(sampling_rate=10000, rpm=1500)
diagnosis = engine.diagnose(signal)

print(diagnosis['primary_fault'])
```

---

## Validación y Testing

### Ejecutar suite de pruebas

```bash
python tests.py
```

Debería mostrar:

```
TEST 1: Generador de Señales ... ✅
TEST 2: Analizador de Señales ... ✅
TEST 3: Simulador de Fallas ... ✅
TEST 4: Motor de Diagnóstico ... ✅
TEST 5: Consistencia ... ✅
TEST 6: Casos Extremos ... ✅

✅ TODAS LAS PRUEBAS PASARON
```

Si alguna falla:

1. Verificar instalación de dependencias
2. Revisar versión de Python
3. Verificar rutas de archivos

---

## Mejora de Rendimiento

### Si el programa es lento

**1. Reducir resolución FFT:**

```python
# De config.py, modificar
NUM_FFT_POINTS = 1024  # En lugar de 2048
```

**2. Reducir duración:**

```python
config = SignalConfig(duration=0.5)  # En lugar de 1.0
```

**3. Reducir frecuencia de muestreo:**

```python
# Solo si no pierdes información importante
config = SignalConfig(sampling_rate=5000)  # De 10000
```

**4. Usar análisis en paralelo:**

```python
# Requiere multiprocessing, no implementado por defecto
# Para casos muy grandes, considerar:
from multiprocessing import Pool
```

---

## Preguntas Frecuentes

**P: ¿Puedo usar esto con OpenFOAM/datos CFD?**  
A: Sí, pero primero extrae la vibración de la simulación a un formato compatible

**P: ¿Funciona en Mac/Linux?**  
A: Sí, igual que en Windows. Solo cambiar rutas (usar / en lugar de \)

**P: ¿Qué pasa si tengo múltiples rodamientos?**  
A: Simula como un único rodamiento equivalente

**P: ¿Puedo exportar los resultados?**  
A: Sí, hay función `save_analysis_to_json()` en utils.py

**P: ¿Cómo calibro con datos reales?**  
A: Compara con tu equipo real y ajusta parámetros de `signal_generator.py`

---

## Contacto y Soporte

Si los problemas persisten:

1. **Verificar README.md** - Documentación general
2. **Revisar docstrings** - Documentación en código
3. **Ejecutar examples/** - Ejemplos de uso
4. **Revisar config.py** - Parámetros ajustables
5. **Ejecutar tests.py** - Validación del sistema

---

**¡La mayoría de problemas se resuelven reinstalando dependencias!**

```bash
pip install --upgrade pip
pip install --upgrade -r requirements.txt
```
