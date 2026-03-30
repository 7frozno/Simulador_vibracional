/**
 * Motor de diagnóstico automático de fallas vibratorias
 */

class DiagnosticEngine {
    constructor(samplingRate = 10000, rpm = 1500) {
        this.analyzer = SignalAnalyzer;
        this.rpm = rpm;
        this.f0 = rpm / 60.0;
        this.samplingRate = samplingRate;
    }

    diagnose(signal) {
        // Obtener todas las características
        const allFeatures = SignalAnalyzer.getAllFeatures(signal, this.samplingRate, this.rpm);

        // Calcular scores
        const scores = this.calculateFaultScores(allFeatures);

        // Identificar falla principal
        let primaryFault = Object.keys(scores)[0];
        let maxScore = scores[primaryFault];

        for (const fault in scores) {
            if (scores[fault] > maxScore) {
                maxScore = scores[fault];
                primaryFault = fault;
            }
        }

        const confidence = maxScore;

        // Fallas secundarias
        const secondaryFaults = {};
        for (const fault in scores) {
            if (fault !== primaryFault && scores[fault] > 0.3) {
                secondaryFaults[fault] = scores[fault];
            }
        }

        return {
            primary_fault: primaryFault,
            confidence: confidence,
            all_scores: scores,
            secondary_faults: secondaryFaults,
            features: allFeatures,
            recommendations: this.getRecommendations(primaryFault),
            severity_level: this.assessSeverity(allFeatures),
            analysis: this.generateAnalysis(allFeatures, primaryFault)
        };
    }

    calculateFaultScores(features) {
        const timeFeatures = features.time_domain;
        const freqFeatures = features.frequency_domain;

        const scores = {
            [FaultType.HEALTHY]: this.scoreHealthy(timeFeatures, freqFeatures),
            [FaultType.BEARING]: this.scoreBearing(timeFeatures, freqFeatures),
            [FaultType.CAVITATION]: this.scoreCavitation(timeFeatures, freqFeatures),
            [FaultType.MISALIGNMENT]: this.scoreMisalignment(timeFeatures, freqFeatures),
            [FaultType.UNBALANCE]: this.scoreUnbalance(timeFeatures, freqFeatures),
            [FaultType.COMBINED]: this.scoreCombined(timeFeatures, freqFeatures)
        };

        // Normalizar
        const total = Object.values(scores).reduce((a, b) => a + b, 0);
        if (total > 0) {
            for (const key in scores) {
                scores[key] = scores[key] / total;
            }
        }

        return scores;
    }

    scoreHealthy(timeFeat, freqFeat) {
        let score = 1.0;

        if (timeFeat.rms > 0.5) score *= 0.5;
        else if (timeFeat.rms > 0.3) score *= 0.8;

        const kurtosis = timeFeat.kurtosis;
        if (Math.abs(kurtosis - 3.0) > 3.0) score *= 0.3;
        else if (Math.abs(kurtosis - 3.0) > 1.5) score *= 0.6;

        const cf = timeFeat.crest_factor;
        if (cf > 5) score *= 0.4;
        else if (cf > 4) score *= 0.7;

        return Math.max(0, score);
    }

    scoreBearing(timeFeat, freqFeat) {
        let score = 0.0;

        const kurtosis = timeFeat.kurtosis;
        if (kurtosis > 8) score += 0.8;
        else if (kurtosis > 6) score += 0.6;
        else if (kurtosis > 4) score += 0.3;

        const cf = timeFeat.crest_factor;
        if (cf > 8) score += 0.7;
        else if (cf > 6) score += 0.5;
        else if (cf > 4) score += 0.2;

        if (timeFeat.rms > 0.5) score += 0.3;

        return Math.min(1.0, score);
    }

    scoreCavitation(timeFeat, freqFeat) {
        let score = 0.0;

        if (timeFeat.rms > 1.0) score += 0.6;
        else if (timeFeat.rms > 0.5) score += 0.3;

        if (timeFeat.skewness > 1.0) score += 0.2;

        if (timeFeat.crest_factor > 4) score += 0.2;

        return Math.min(1.0, score);
    }

    scoreMisalignment(timeFeat, freqFeat) {
        let score = 0.0;

        const amp2x = freqFeat['2X_amplitude'] || 0;
        const amp1x = freqFeat['1X_amplitude'] || 0;

        // Característica: 2X > 1X
        if (amp2x > amp1x * 0.8) score += 0.6;
        if (amp2x > amp1x) score += 0.2;

        // Múltiples armónicos pares
        const amp4x = freqFeat['4X_amplitude'] || 0;
        const amp6x = freqFeat['6X_amplitude'] || 0;

        if (amp4x > 0.1) score += 0.2;
        if (amp6x > 0.05) score += 0.1;

        return Math.min(1.0, score);
    }

    scoreUnbalance(timeFeat, freqFeat) {
        let score = 0.0;

        const amp1x = freqFeat['1X_amplitude'] || 0;
        const amp2x = freqFeat['2X_amplitude'] || 0;
        const amp3x = freqFeat['3X_amplitude'] || 0;

        // Característica: 1X dominante
        if (amp1x > amp2x * 3) score += 0.7;
        if (amp1x > amp3x * 2) score += 0.2;

        if (timeFeat.crest_factor < 5) score += 0.1;

        return Math.min(1.0, score);
    }

    scoreCombined(timeFeat, freqFeat) {
        let score = 0.0;

        if (timeFeat.kurtosis > 4) score += 0.2;
        if (timeFeat.rms > 0.3) score += 0.2;

        const amp1x = freqFeat['1X_amplitude'] || 0;
        const amp2x = freqFeat['2X_amplitude'] || 0;

        // Múltiples armónicos presentes
        if (amp1x > 0.1 && amp2x > 0.1) score += 0.3;

        return Math.min(1.0, score);
    }

    assessSeverity(features) {
        const rms = features.time_domain.rms;

        if (rms < 0.5) return 'NORMAL';
        if (rms < 1.0) return 'LEVE';
        if (rms < 2.0) return 'MODERADA';
        if (rms < 3.5) return 'SEVERA';
        return 'CRÍTICA';
    }

    getRecommendations(faultType) {
        const recommendations = {
            [FaultType.HEALTHY]: [
                'Continuar con el monitoreo regular',
                'Programar inspección de rutina',
                'Mantener registros de tendencias'
            ],
            [FaultType.BEARING]: [
                'Inspeccionar rodamientos',
                'Verificar juego radial',
                'Considerar reemplazo preventivo',
                'Aumentar frecuencia de monitoreo'
            ],
            [FaultType.CAVITATION]: [
                'Revisar presión de succión',
                'Verificar condiciones de entrada',
                'Inspeccionar impulsores',
                'Acción inmediata recomendada'
            ],
            [FaultType.MISALIGNMENT]: [
                'Realinear máquinas',
                'Verificar soportes y cimentación',
                'Inspeccionar acoplamientos',
                'Realizar análisis de alineación'
            ],
            [FaultType.UNBALANCE]: [
                'Balancear rotor',
                'Verificar distribución de carga',
                'Inspeccionar álabes/discos',
                'Considerar balanceo dinámico'
            ],
            [FaultType.COMBINED]: [
                'Realizar inspección exhaustiva',
                'Revisar múltiples aspectos',
                'Solicitar análisis experto',
                'Considerar servicio técnico'
            ]
        };

        return recommendations[faultType] || [];
    }

    generateAnalysis(features, primaryFault) {
        const timeFeat = features.time_domain;
        const analysis = {
            summary: `Falla detectada: ${primaryFault}`,
            metrics: {
                rms: `${timeFeat.rms.toFixed(3)} g`,
                peak: `${timeFeat.peak.toFixed(3)} g`,
                kurtosis: `${timeFeat.kurtosis.toFixed(2)}`,
                crest_factor: `${timeFeat.crest_factor.toFixed(2)}`
            },
            detailed_findings: this.generateDetailedFindings(primaryFault, features)
        };

        return analysis;
    }

    generateDetailedFindings(faultType, features) {
        const findings = [];

        switch (faultType) {
            case FaultType.BEARING:
                findings.push('Se detectan impulsos característicos de falla de rodamiento');
                findings.push(`Kurtosis elevada: ${features.time_domain.kurtosis.toFixed(2)} (> 8 = crítico)`);
                findings.push(`Factor de cresta: ${features.time_domain.crest_factor.toFixed(2)} (> 6 = crítico)`);
                break;

            case FaultType.UNBALANCE:
                const amp1x = features.frequency_domain['1X_amplitude'] || 0;
                findings.push('Se detecta dominancia clara del componente 1X');
                findings.push(`Componente 1X: ${amp1x.toFixed(3)}`);
                findings.push('Patrón típico de desbalance de masa');
                break;

            case FaultType.MISALIGNMENT:
                const amp2x = features.frequency_domain['2X_amplitude'] || 0;
                findings.push('Se detectan armónicos pares amplificados');
                findings.push(`Componente 2X: ${amp2x.toFixed(3)}`);
                findings.push('Indicativo de problemas de alineación');
                break;

            case FaultType.CAVITATION:
                findings.push(`RMS muy elevado: ${features.time_domain.rms.toFixed(3)} g`);
                findings.push('Espectro disperso en banda ancha');
                findings.push('Señala formación/colapso de burbujas');
                break;

            case FaultType.HEALTHY:
                findings.push('Parámetros dentro de rangos normales');
                findings.push('RMS bajo y espectro limpio');
                findings.push('Equipo operando correctamente');
                break;
        }

        return findings;
    }
}
