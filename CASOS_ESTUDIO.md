# 📚 Casos de Estudio - Análisis Vibracional

## Caso 1: Diagnóstico de Desbalance Progresivo

### Escenario

Una bomba centrífuga de 1500 RPM ha estado funcionando durante varios meses. Los operadores reportan vibraciones anormales que han ido aumentando con el tiempo.

### Síntomas Observados

- Vibraciones perceptibles a mano
- Ruido más fuerte que lo normal
- Aumento gradual con cada día que pasa

### Diagnóstico Esperado

```
Falla Detectada: DESBALANCE

Indicadores Clave:
✓ 1X Amplitude: 0.65 (DOMINANTE)
✓ 2X Amplitude: 0.08 (muy baja)
✓ Relación 1X/2X: 8.1 (>> 1)
✓ Kurtosis: 3.2 (cerca de 3)
✓ Factor de Cresta: 3.5 (moderado)
✓ RMS: 0.85 g

Conclusión: Claramente DESBALANCE
Severidad: MODERADA → SEVERA
```

### Plan de Acción

1. **Inmediato**: Reducir velocidad si es posible
2. **Urgente (< 24h)**: Planificar balanceo dinámico
3. **Antes de parada**: Obtener peso/ubicación del desbalance
4. **Ejecutar**: Balanceo ISO 21940

### Tiempo Estimado de Fallo

- Progresión: Lineal (desbalance puro)
- Sin acción: 200-300 horas adicionales
- Riesgo: Daño de rodamientos por sobrecarga

---

## Caso 2: Falla de Rodamiento Incipiente

### Escenario

Un ventilador industrial de 1800 RPM muestra signos de fatiga. El personal técnico sospecha problema en rodamiento pero no es evidente solo con inspección visual.

### Síntomas Observados

- Pequeños clics intermitentes
- Ligero aumento de temperatura en rodamiento
- Vibración muy alta en banda 2-5 kHz

### Diagnóstico Esperado

```
Falla Detectada: RODAMIENTO

Indicadores Clave:
✓ Kurtosis: 9.2 (>>> 3)
✓ Factor de Cresta: 7.8 (muy alto)
✓ RMS: 1.4 g
✓ Espectro: Impulsos a 2000-4000 Hz
✓ Envolvente: Modulada a frecuencia de rodamiento
✓ Bandas laterales: Claramente visibles

Conclusión: FALLA DE RODAMIENTO confirmada
Severidad: SEVERA → CRÍTICA
```

### Plan de Acción

1. **Urgente (< 48h)**: Procurar rodamiento de repuesto
2. **Crítico**: Monitoreo cada 2 horas
3. **Parada planificada**: Próxima 48-72 horas
4. **Prevención**: Revisar lubricación y sellos

### Tiempo Estimado de Fallo

- Progresión: Acelerada (exponencial)
- Sin acción: 50-150 horas
- Riesgo: Bloqueo total, daño irreversible

---

## Caso 3: Desalineamiento de Ejes

### Escenario

Una bomba acoplada con motor eléctrico mediante acoplamiento elástico. Después de mantenimiento, se reinstalaron pero con alineamiento "aproximado".

### Síntomas Observados

- Vibraciones axiales anormales
- Calentamiento en cojinete axial
- Ruido en frecuencias múltiplos de RPM

### Diagnóstico Esperado

```
Falla Detectada: DESALINEAMIENTO

Indicadores Clave:
✓ 2X Amplitude: 0.48 (> 1X)
✓ 1X Amplitude: 0.30 (segundo lugar)
✓ 4X Amplitude: 0.35 (significativo)
✓ 6X Amplitude: 0.25 (visible)
✓ Armónicos pares dominantes
✓ Kurtosis: 4.7
✓ Bandas laterales en armónicos

Conclusión: DESALINEAMIENTO angular
Severidad: MODERADA
```

### Plan de Acción

1. **Próxima parada programada**: Alineamiento láser completo
2. **Verificar**:
   - Alineamiento angular (coaxialidad)
   - Alineamiento radial (distancia entre ejes)
   - Condición de flexibles/acoplamiento
3. **Después**: Monitoreo de seguimiento

### Tiempo Estimado de Fallo

- Progresión: Moderada (crecimiento lineal)
- Sin acción: 500-1000 horas
- Riesgo: Daño acelerado de rodamientos, fugas en sello

---

## Caso 4: Cavitación en Bomba

### Escenario

Una bomba de agua industrial ha estado operando en condiciones de caudal reducido. Los operadores notan ruido anormal y vibración creciente.

### Síntomas Observados

- Ruido similar a grava en la bomba
- Vibración de banda ancha
- Posible erosión visible en impelente

### Diagnóstico Esperado

```
Falla Detectada: CAVITACIÓN

Indicadores Clave:
✓ RMS: 2.1 g (muy elevado)
✓ Ancho de Banda: 4200 Hz (extendido)
✓ Energía Alta Frecuencia: 45% total
✓ Espectro: Plano y denso
✓ Impulsos: Aperiódicos, aleatorios
✓ Kurtosis: 5.8
✓ 1X Amplitude: muy baja (0.05)

Conclusión: CAVITACIÓN activa
Severidad: SEVERA
```

### Plan de Acción

1. **Inmediato**: Revisar condiciones hidráulicas
   - NPSH disponible vs requerido
   - Presión de succión
   - Temperatura del fluido
2. **Correcciones**:
   - Aumentar presión de succión
   - Reducir caudal si en curva pobre
   - Revisar filtros de succión
3. **Inspección**: Erosión en impelente

### Tiempo Estimado de Fallo

- Progresión: Rápida en cavitación activa
- Sin acción: 50-200 horas
- Riesgo: Perforación de componentes, daño catastrófico

---

## Caso 5: Falla Combinada

### Escenario

Un compresor de aire de 3600 RPM ha sido operado bajo condiciones adversas: sobrecarga, misalineación y falta de mantenimiento.

### Síntomas Observados

- Vibración muy alta (>3 g)
- Múltiples componentes de ruido
- Espectro muy complejo

### Diagnóstico Esperado

```
Falla Detectada: FALLA COMBINADA (Probabilidades)

Scores:
- Desbalance: 45% (componente 1X elevada)
- Desalineamiento: 35% (armónicos pares presentes)
- Rodamiento: 25% (kurtosis moderadamente elevada)
- Cavitación: 10% (banda ancha parcial)

Indicadores Clave:
✓ RMS: 2.8 g (muy elevado)
✓ Kurtosis: 7.2 (impactos presentes)
✓ Factor de Cresta: 6.5
✓ Múltiples picos en espectro
✓ Bandas laterales complejas

Conclusión: MÚLTIPLES DEFECTOS SIMULTÁNEOS
Severidad: CRÍTICA
```

### Plan de Acción

1. **URGENTE**: Parada inmediata del equipo
2. **Análisis secuencial**:
   - Primero abordar desbalance (más evidente)
   - Luego verificar alineamiento
   - Finalmente evaluar rodamientos
3. **Inspección completa**:
   - Desmontaje completo
   - Revisión de todos los componentes
   - Reemplazo de rodamientos si necesario
4. **Reconstrucción**: Con nuevo balanceo y alineamiento

### Tiempo Estimado de Fallo

- Progresión: Rápida y acelerada
- Sin acción: 24-72 horas
- Riesgo: Fallo catastrófico inminente

---

## Guía de Interpretación Rápida

### Matriz de Decisión

| Resultado      | 1X  | 2X  | Kurtosis | Factor Cresta | Acción |
|--------------|-----|-----|----------|---------------|--------|
| Desbalance   | ⬆️   | ⬇️   | ≈3       | 3-4           | Balanceo |
| Desalineamiento | ⬇️ | ⬆️ | 4-5      | 3-4.5         | Alineamiento |
| Rodamiento   | ⬇️   | ⬇️   | >>8      | >6            | Reemplazo urgente |
| Cavitación   | ⬇️   | ⬇️   | 5-8      | 4-7           | Revisar NPSH |

### Severidad por Parámetro

**RMS (g)**

- 0.0-0.3: NORMAL
- 0.3-0.5: LEVE
- 0.5-1.5: MODERADA
- 1.5-2.5: SEVERA
- >2.5: CRÍTICA

**Kurtosis**

- <4: Equipo normal
- 4-6: Indicio de impactos
- 6-10: Falla probable
- >10: Falla severa

**Factor de Cresta**

- <4: Normal
- 4-6: Moderado
- >8: Severo

---

## 📋 Checklist de Diagnóstico

### Paso 1: Recolección de Datos

- [ ] RPM del equipo
- [ ] Puntos de medición (radial, axial, tangencial)
- [ ] Condiciones de operación (carga, temperatura)
- [ ] Tiempo de operación

### Paso 2: Análisis Inicial

- [ ] Calcular RMS
- [ ] Obtener factor de cresta
- [ ] Calcular kurtosis
- [ ] Realizar FFT

### Paso 3: Análisis Armónico

- [ ] Identificar 1X
- [ ] Comparar 1X vs 2X
- [ ] Buscar armónicos significativos
- [ ] Verificar bandas laterales

### Paso 4: Diagnóstico Diferencial

- [ ] ¿1X > 2X? → Considerar desbalance
- [ ] ¿2X > 1X con 4X, 6X? → Desalineamiento
- [ ] ¿Kurtosis > 8? → Rodamiento específicamente
- [ ] ¿Espectro plano ancho? → Cavitación

### Paso 5: Recomendación

- [ ] Identificar falla primaria
- [ ] Evaluar severidad
- [ ] Proponer acciones correctivas
- [ ] Establecer cronograma

---

## 🎓 Lecciones Aprendidas

### Desbalance vs Desalineamiento

- **Desbalance**: Fenómeno de inercia pura (depende de peso)
- **Desalineamiento**: Interferencia mecánica (depende de rigidez)
- La relación 1X/2X distingue estos dos casos

### Rodamiento: Detección Temprana

- Kurtosis es el indicador más confiable
- Mucho antes de fallo catastrófico
- Ventana de diagnosis: 50-200 horas

### Cavitación: Urgencia

- Causa daño rápido e irreversible
- Debe corregirse inmediatamente
- Revisión del diseño hidráulico necesaria

### Falla Combinada: Compleja

- Síntomas solapados y confusos
- Requiere análisis sistemático
- Muchas veces necesita desmontaje

---

## 📝 Plantilla de Reporte

```
REPORTE DE ANÁLISIS VIBRACIONAL

Equipo: _________________
Fecha: _________________
Técnico: _________________

MEDICIONES:
- RMS: _____ g
- Pico: _____ g
- Kurtosis: _____
- Factor Cresta: _____

ANÁLISIS:
Falla Identificada: _________________
Confianza: ____%
Severidad: _________________

INDICADORES CLAVE:
1X Amplitude: _____
2X Amplitude: _____
Ratio 1X/2X: _____
Ancho de Banda: _____ Hz

RECOMENDACIONES:
1. _________________________
2. _________________________
3. _________________________

PLAZO:
Próxima Acción: _________________
Próximo Análisis: _________________
```

---

**Usa estos casos como referencia para tus propios diagnósticos**
