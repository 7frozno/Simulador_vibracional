# 🔬 Referencia Técnica - Análisis Vibracional

## Conceptos Fundamentales

### 1. Vibración

Movimiento oscilatorio de un objeto alrededor de su posición de equilibrio.

**Tipos:**

- **Libre**: Oscilación sin fuerzas externas (después de perturbación inicial)
- **Forzada**: Oscilación bajo acción de fuerzas periódicas
- **Amortiguada**: Oscilación con pérdida de energía

### 2. Dominio del Tiempo vs Frecuencia

**Dominio del Tiempo:**

- Gráfica x(t): amplitud vs tiempo
- Muestra comportamiento instantáneo
- Difícil de interpretar para señales complejas

**Dominio de Frecuencia:**

- Gráfica X(f): amplitud vs frecuencia
- Muestra contenido de energía
- Ideal para diagnóstico

---

## Características Principales

### RMS (Root Mean Square) / Valor Eficaz

$$RMS = \sqrt{\frac{1}{N}\sum_{i=1}^{N} x_i^2}$$

**Significado:**

- Valor promedio de energía
- Base para clasificación de severidad
- Integra toda la señal

**Interpretación:**

- RMS bajo → Operación normal
- RMS alto → Problema presente

**Estándar ISO 20816:**

```
Zona A: < 0.71 mm/s    → Aceptable
Zona B: 0.71-2.8 mm/s  → Tolerable
Zona C: 2.8-7.1 mm/s   → Inaceptable (parada próxima)  
Zona D: > 7.1 mm/s     → Inaceptable (parada inmediata)
```

### Pico y Pico-Pico

$$Peak = \max(|x(t)|)$$

$$Peak\_to\_Peak = \max(x(t)) - \min(x(t))$$

**Significado:**

- Extremos de la oscilación
- Importante para diseño mecánico
- Indicador de impactos

**Relación:**

```
Pico-Pico ≈ 2 × Pico (para señal sinusoidal pura)
Pico-Pico > 2 × Pico (indica no-linealidad)
```

### Factor de Cresta (Crest Factor, CF)

$$CF = \frac{\text{Valor Pico}}{\text{RMS}}$$

**Rango Típico:**

- **Sinusoide pura**: CF ≈ 1.414
- **Equipo normal**: CF = 2-4
- **Impacto moderado**: CF = 4-6
- **Defecto severo**: CF > 8

**Interpretación:**

- CF alto → Impactos transitorios
- Muy sensible a fallas de rodamiento
- Puede detectar falla incipiente

**Ventaja sobre RMS:**

```
RMS = 1 g (puede ser normal o alarma)
CF = 8 (claramente hay impactos)
→ CF da información adicional
```

### Kurtosis

$$Kurtosis = \frac{E[(X-\mu)^4]}{\sigma^4}$$

Donde:

- μ = media
- σ = desviación estándar
- E[] = esperanza (promedio)

**Interpretación:**

- **K = 3.0**: Distribución normal (equipo sano)
- **K = 3-5**: Distribución con colas ligeras (ligero deterioro)
- **K = 5-10**: Distribución con picos (defecto moderado)
- **K > 10**: Distribución muy punteada (falla severa)

**Por qué es importante:**

```
RMS alto no siempre = falla
Kurtosis alto = casi siempre hay impactos
```

### Asimetría (Skewness)

$$Skewness = E\left[\left(\frac{X-\mu}{\sigma}\right)^3\right]$$

**Interpretación:**

- = 0: Distribución simétrica
- > 0: Cola hacia derechas (impactos positivos)
- < 0: Cola hacia izquierda (impactos negativos)

---

## Análisis Frecuencial

### FFT (Fast Fourier Transform)

Convierte señal tiempo → frecuencia

$$X(f) = \int_{-\infty}^{\infty} x(t) e^{-j2\pi ft} dt$$

**Parámetros importantes:**

- **Resolución**: Δf = fs / N
  - fs = frecuencia muestreo
  - N = puntos FFT
- **Rango Nyquist**: 0 - fs/2

**Ejemplo:**

```
fs = 10000 Hz
N = 1024 puntos
Δf = 10000 / 1024 ≈ 9.77 Hz
```

### Armónicos (Componentes de RPM)

**Definición:**

- **1X**: Frecuencia de rotación fundamental = RPM/60
- **nX**: Múltiplo de 1X para n = 2, 3, 4...

**Ejemplo (1500 RPM):**

```
f0 = 1500/60 = 25 Hz
1X = 25 Hz
2X = 50 Hz
3X = 75 Hz
4X = 100 Hz
...
```

### Espectro de Potencia

$$P(f) = |X(f)|^2$$

**Características:**

- Valor absoluto elevado al cuadrado
- Representa energía por frecuencia
- Simétrico en frecuencias positivas/negativas

---

## Patrones de Diagnóstico

### Desbalance

**Ecuación característica:**
$$F_{centrifuga} = m \cdot e \cdot \omega^2$$

Donde:

- m = masa desbalanceada
- e = excentricidad
- ω = velocidad angular

**Patrón espectral:**

```
1X: ALTO (dominant)
2X: BAJO
3X: MUY BAJO
...
Resultado: 1X/2X >> 1
```

**Fórmula de vibración:**
$$A_1X \propto \text{Desbalance} \propto RPM^2$$

### Desalineamiento

**Tipos:**

1. **Paralelo**: Offset entre ejes (radial)
2. **Angular**: Ángulo entre ejes

**Patrón espectral:**

```
1X: MODERADO
2X: ALTO (> 1X)
4X: SIGNIFICATIVO
6X: VISIBLE
Bandas laterales: ± 1X alrededor de 2X, 4X
```

**Razón física:**
$$F = k \cdot \Delta x$$

- Fuerza proporcional al desplazamiento  
- Componentes pares dominan

### Falla de Rodamiento

**Frecuencias características:**

Sea un rodamiento con:

- Bd = diámetro bola/rodillo (mm)
- Pd = diámetro paso (mm)
- Nb = número elementos
- fr = frecuencia rotación jaula

**Frecuencias de defecto:**

1. **BPFO** (Ball Pass Frequency Outer):
   $$f_{BPFO} = \frac{Nb}{2} \cdot f0 \left(1 + \frac{Bd}{Pd}\cos\theta\right)$$

2. **BPFI** (Ball Pass Frequency Inner):
   $$f_{BPFI} = \frac{Nb}{2} \cdot f0 \left(1 - \frac{Bd}{Pd}\cos\theta\right)$$

3. **FTF** (Fundamental Train Frequency):
   $$f_{FTF} = \frac{f0}{2}\left(1 - \frac{Bd}{Pd}\cos\theta\right)$$

4. **BSF** (Ball Spin Frequency):
   $$f_{BSF} = \frac{Pd}{2Bd} \cdot f0 \left(1 - \left(\frac{Bd}{Pd}\right)^2\cos^2\theta\right)$$

**Patrón espectral:**

```
Alta Frecuencia: Impulsos a 2000-5000 Hz
Modulación: A velocidad de jaula (FTF)
Bandas laterales: ± FTF alrededor de BPFO
Envolvente: Característica del tipo de defecto
```

**Índices de diagnóstico:**

- Kurtosis > 8
- CF > 6  
- Bandas laterales espaciadas a FTF

### Cavitación

**Cambios mecánicos:**

1. Formación de burbujas: Zona de baja presión
2. Transporte: Flujo del líquido lleva burbujas
3. Colapso: Implosión cuando presión aumenta

**Patrón espectral:**

```
Ancho de banda: > 3000 Hz (plano, ruido)
Impulsos: Aperiódicos, aleatorios
1X: MUY BAJO
Energía: Distribuida uniformemente
Característica: "Ruido blanco" con picos
```

---

## Severidad ISO

### Estándar ISO 20816-1 (Vibración Mecánica)

**Zonas de severidad:**

Para máquinas del Grupo 2 (bombas, compresores):

| Parámetro | Zona A | Zona B | Zona C | Zona D |
|-----------|--------|--------|--------|--------|
| **RMS mm/s** | <0.71 | 0.71-2.8 | 2.8-7.1 | >7.1 |
| **Acción** | Normal | Tolerante | Monitor | Parar |
| **Tiempo** | Indefinido | < 7 días | < 24h | Inmediato |

### Escala Personalizada (Este Simulador)

| Severidad | RMS (g) | Kurtosis | CF | Acción |
|-----------|---------|----------|----|---------|
| NORMAL | <0.3 | ≈3.0 | <4 | Monitoreo rutinario |
| LEVE | 0.3-0.5 | 3.5-4.5 | 4-5 | Próxima parada |
| MODERADA | 0.5-1.5 | 4.5-6 | 5-6 | Parada planeada |
| SEVERA | 1.5-2.5 | 6-8 | 6-8 | En < 48h |
| CRÍTICA | >2.5 | >8 | >8 | Inmediato |

---

## Señales Común

### Sinusoide Pura

$$x(t) = A \sin(2\pi ft + \phi)$$

Parámetros:

- A = Amplitud
- f = Frecuencia
- φ = Fase

Propiedades:

- RMS = A/√2
- CF = √2 ≈  1.414
- Kurtosis = 3.0
- Espectro: Pico único a frecuencia f

### Ruido Blanco Gaussiano

Propiedades:

- RMS = Depende de amplitud
- CF = 3-4 (tipicamente)
- Kurtosis = 3.0
- Espectro: Plano, energía uniforme

### Impulsos Periódicos

$$x(t) = \sum_{n} A \delta(t - nT)$$

Propiedades:

- RMS = Bajo (impulsos son escasos)
- CF = Muy alto (picos grandes)
- Kurtosis = Muy elevada (>10)
- Espectro: Líneas armónicas

---

## Relaciones Útiles

### Conversión Amplitud-Energía

**Para sinusoide:**
$$RMS = \frac{A_{pico}}{\sqrt{2}} = \frac{A_{pico-pico}}{2\sqrt{2}}$$

**Para proceso aleatorio:**
$$RMS = \sqrt{\sigma^2} = \sqrt{var(x)}$$

### Relación CF-Kurtosis

Para ruido gaussiano:

- Kurtosis ≈ 3
- CF ≈ 3-4  
- Relación: K ≈ 1 + CF/4 (aproximada)

Para impactos:

- Kurtosis >> 3
- CF >> 4
- Kurtosis es más sensible que CF

### Conversión RPM-Frecuencia

$$f_0 = \frac{RPM}{60}$$

Ejemplo:

- 1500 RPM → 25 Hz (1X)
- 3600 RPM → 60 Hz (1X)

---

## Tablas de Referencia

### Rodamientos Típicos

| Tipo | Diámetro | BPFO/FTF | f0 1500RPM |
|------|----------|----------|-----------|
| 6205 | 15 mm | 4.95 / 0.38 | ~31-38 Hz |
| 6206 | 20 mm | 4.95 / 0.38 | ~31-38 Hz |
| 6207 | 25 mm | 4.95 / 0.38 | ~31-38 Hz |

Fórmula general:

- BPFO ≈ 3.5-5.5 × f0 (depende geometría)
- FTF ≈ 0.3-0.4 × f0

### Criterios Rápidos

**¿Es Desbalance?**  
→ 1X > 0.3, 2X < 0.1, Kurtosis ≈3, CF <5 → SÍ

**¿Es Desalineamiento?**  
→ 2X > 1X, 4X > 0.2, bandas laterales presentes → SÍ

**¿Es Rodamiento?**  
→ Kurtosis > 8, CF > 6, impulsos HF → SÍ

**¿Es Cavitación?**  
→ Ruido ancho, RMS muy alto, 1X bajo → SÍ

---

## Normativas Aplicables

### ISO 10816 (Derogada, cambiada a 20816)

Vibración mecánica en máquinas

### ISO 20816-1

Requisitos y evaluación de vibración en máquinas rotativas

### ISO 13373-1

Diagnóstico y monitoreo de vibraciones

### ISO 13373-2  

Monitoreo basado en condición y análisis de datos

### API 670

Machinery Protection Systems

---

## Unidades Comunes

### Aceleración

- **g** (aceleración gravitacional): 1 g = 9.81 m/s²
- **m/s²**)
- **mm/s²**

Conversión:
$$1 \text{ g} = 1000 \text{ mm/s}^2$$

### Velocidad

- **mm/s** (muy común)
- **m/s**
- **ips** (pulgadas/segundo)

Conversión (para sinusoide):
$$V = A \times 2\pi f$$
donde A = amplitud, f = frecuencia

### Desplazamiento

- **μm** (micrómetros)
- **mm**
- **mils** (milésimas de pulgada)

Conversión (para sinusoide):
$$D = \frac{A}{2\pi f}$$

---

**Esta referencia técnica complementa el simulador práctico**
