/**
 * Simulador de fallas en equipos rotativos
 */

const FaultType = {
    HEALTHY: 'sano',
    BEARING: 'rodamiento',
    CAVITATION: 'cavitacion',
    MISALIGNMENT: 'desalineamiento',
    UNBALANCE: 'desbalance',
    COMBINED: 'combinada'
};

const FaultSeverity = {
    NONE: 0.0,
    MILD: 0.3,
    MODERATE: 0.6,
    SEVERE: 0.9,
    CRITICAL: 1.0
};

class FaultSimulator {
    constructor(config = null) {
        this.config = config || new SignalConfig();
        this.generator = new SignalGenerator(config);
        this.currentFault = null;
        this.currentSeverity = null;
    }

    generateFault(faultType, severity = FaultSeverity.MODERATE) {
        this.currentFault = faultType;
        this.currentSeverity = severity;

        switch (faultType) {
            case FaultType.HEALTHY:
                return this.generator.generateHealthy();

            case FaultType.BEARING:
                return this.generator.generateBeatingFault(20.0 * severity);

            case FaultType.CAVITATION:
                const cavSignal = this.generator.generateCavitation();
                return {
                    time: cavSignal.time,
                    signal: cavSignal.signal.map(x => x * (0.5 + 0.5 * severity))
                };

            case FaultType.MISALIGNMENT:
                return this.generator.generateMisalignment(severity);

            case FaultType.UNBALANCE:
                return this.generator.generateUnbalance(severity);

            case FaultType.COMBINED:
                return this.generateCombinedFault(severity);

            default:
                return this.generator.generateHealthy();
        }
    }

    generateCombinedFault(severity) {
        const unbal = this.generator.generateUnbalance(0.6 * severity);
        const misalign = this.generator.generateMisalignment(0.4 * severity);
        const bearing = this.generator.generateBeatingFault(10.0 * severity);

        const combined = new Array(unbal.signal.length);
        const maxVal = Math.max(...unbal.signal.map(x => Math.abs(x)), ...misalign.signal.map(x => Math.abs(x)), ...bearing.signal.map(x => Math.abs(x)));

        for (let i = 0; i < combined.length; i++) {
            combined[i] = (0.5 * unbal.signal[i] + 0.3 * misalign.signal[i] + 0.2 * bearing.signal[i]) / maxVal * this.config.amplitude;
        }

        return { time: unbal.time, signal: combined };
    }

    getFaultDescription(faultType) {
        const descriptions = {
            [FaultType.HEALTHY]: {
                name: 'Equipo Sano',
                description: 'Funcionamiento normal sin defectos detectables',
                characteristics: [
                    'Bajos niveles de vibración',
                    'Componente 1X moderado',
                    'Bajo factor de cresta (< 4)',
                    'Espectro limpio y bien definido'
                ],
                typical_values: {
                    rms: '0.1 - 0.3 g',
                    kurtosis: '3.0 - 3.5',
                    crest_factor: '2.5 - 4.0'
                }
            },
            [FaultType.BEARING]: {
                name: 'Falla de Rodamiento',
                description: 'Defecto en elementos rodantes o pistas del rodamiento',
                characteristics: [
                    'Impulsos de alta frecuencia (1-5 kHz)',
                    'Modulación por velocidad de rotación',
                    'Factor de cresta elevado (> 6)',
                    'Kurtosis muy elevada (> 8)',
                    'Espectro con bandas laterales'
                ],
                typical_values: {
                    rms: '0.5 - 2.0 g',
                    kurtosis: '> 8.0',
                    crest_factor: '> 6.0'
                }
            },
            [FaultType.CAVITATION]: {
                name: 'Cavitación',
                description: 'Formación y colapso de burbujas en la bomba',
                characteristics: [
                    'Ruido de banda ancha intenso',
                    'Picos aleatorios e impulsivos',
                    'RMS muy elevado',
                    'Espectro extendido',
                    'Deterioro acelerado'
                ],
                typical_values: {
                    rms: '1.0 - 3.0 g',
                    kurtosis: '> 6.0',
                    crest_factor: '> 5.0'
                }
            },
            [FaultType.MISALIGNMENT]: {
                name: 'Desalineamiento',
                description: 'Desaligne axial o angular entre ejes',
                characteristics: [
                    'Amplificación de armónicos pares (2X, 4X)',
                    '2X > 1X en magnitud',
                    'Bandas laterales amplias',
                    'Contenido de baja frecuencia significativo',
                    'Patrón simétrico en FFT'
                ],
                typical_values: {
                    rms: '0.3 - 1.0 g',
                    kurtosis: '3.5 - 5.0',
                    crest_factor: '3.0 - 5.0'
                }
            },
            [FaultType.UNBALANCE]: {
                name: 'Desbalance',
                description: 'Distribución no uniforme de masa',
                characteristics: [
                    'Componente 1X dominante',
                    '1X >> 2X',
                    'Contenido de baja frecuencia',
                    'RMS moderado',
                    'Espectro con estructura clara'
                ],
                typical_values: {
                    rms: '0.2 - 0.8 g',
                    kurtosis: '3.0 - 4.0',
                    crest_factor: '2.5 - 4.0'
                }
            },
            [FaultType.COMBINED]: {
                name: 'Falla Combinada',
                description: 'Múltiples fallas presentes simultáneamente',
                characteristics: [
                    'Componentes de múltiples fallas',
                    'Espectro complejo',
                    'Elevada variabilidad',
                    'Múltiples bandas laterales',
                    'Diagnóstico difícil'
                ],
                typical_values: {
                    rms: '0.5 - 2.0 g',
                    kurtosis: '> 5.0',
                    crest_factor: '> 4.0'
                }
            }
        };

        return descriptions[faultType] || descriptions[FaultType.HEALTHY];
    }
}
