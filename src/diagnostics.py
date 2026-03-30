"""
Motor de diagnóstico basado en características vibratorias
Identifica tipos de falla automáticamente
"""

from typing import Dict, Tuple
import numpy as np
from .signal_analyzer import SignalAnalyzer
from .fault_simulator import FaultType


class DiagnosticEngine:
    """Motor de diagnóstico automático de fallas"""
    
    def __init__(self, sampling_rate: float = 10000, rpm: float = 1500):
        """
        Inicializa el motor de diagnóstico
        
        Args:
            sampling_rate: Frecuencia de muestreo
            rpm: Revoluciones por minuto del equipo
        """
        self.analyzer = SignalAnalyzer(sampling_rate)
        self.rpm = rpm
        self.f0 = rpm / 60.0  # Frecuencia fundamental
        
    def diagnose(self, signal: np.ndarray) -> Dict:
        """
        Realiza diagnóstico completo de la señal
        
        Args:
            signal: Señal vibracional a analizar
            
        Returns:
            Diccionario con diagnóstico detallado
        """
        # Obtener todas las características
        all_features = self.analyzer.get_all_features(signal, self.rpm)
        
        # Calcular scores de diagnóstico
        scores = self._calculate_fault_scores(all_features)
        
        # Identificar falla principal
        primary_fault = max(scores, key=scores.get)
        confidence = scores[primary_fault]
        
        # Análisis de otras fallas
        secondary_faults = {k: v for k, v in scores.items() 
                           if k != primary_fault and v > 0.3}
        
        return {
            'primary_fault': primary_fault,
            'confidence': confidence,
            'all_scores': scores,
            'secondary_faults': secondary_faults,
            'features': all_features,
            'recommendations': self._get_recommendations(primary_fault),
            'severity_level': self._assess_severity(all_features),
            'analysis': self._generate_analysis(all_features, primary_fault)
        }
    
    def _calculate_fault_scores(self, features: Dict) -> Dict[str, float]:
        """
        Calcula scores de probabilidad para cada tipo de falla
        
        Args:
            features: Características de la señal
            
        Returns:
            Diccionario con scores para cada falla
        """
        time_feat = features['time_domain']
        freq_feat = features['frequency_domain']
        
        scores = {
            FaultType.HEALTHY: self._score_healthy(time_feat, freq_feat),
            FaultType.BEARING: self._score_bearing(time_feat, freq_feat),
            FaultType.CAVITATION: self._score_cavitation(time_feat, freq_feat),
            FaultType.MISALIGNMENT: self._score_misalignment(time_feat, freq_feat),
            FaultType.UNBALANCE: self._score_unbalance(time_feat, freq_feat),
            FaultType.COMBINED: self._score_combined(time_feat, freq_feat),
        }
        
        # Normalizar scores a 0-1
        total = sum(scores.values())
        if total > 0:
            scores = {k: v/total for k, v in scores.items()}
        
        return scores
    
    def _score_healthy(self, time_feat: Dict, freq_feat: Dict) -> float:
        """Calcula score de equipo sano"""
        score = 1.0
        
        # RMS bajo (< 0.3 g)
        if time_feat['rms'] > 0.5:
            score *= 0.5
        elif time_feat['rms'] > 0.3:
            score *= 0.8
        
        # Kurtosis cercana a 3
        kurtosis = time_feat['kurtosis']
        if abs(kurtosis - 3.0) > 3.0:
            score *= 0.3
        elif abs(kurtosis - 3.0) > 1.5:
            score *= 0.6
        
        # Factor de cresta moderado
        cf = time_feat['crest_factor']
        if cf > 5:
            score *= 0.4
        elif cf > 4:
            score *= 0.7
        
        # Energía baja en banda alta
        total_energy = (freq_feat['low_freq_energy'] + 
                       freq_feat['mid_freq_energy'] + 
                       freq_feat['high_freq_energy'])
        if total_energy > 0:
            ratio_hf = freq_feat['high_freq_energy'] / total_energy
            if ratio_hf > 0.3:
                score *= 0.6
        
        return max(0, score)
    
    def _score_bearing(self, time_feat: Dict, freq_feat: Dict) -> float:
        """Calcula score de falla de rodamiento"""
        score = 0.0
        
        # Kurtosis muy elevada es indicador fuerte
        kurtosis = time_feat['kurtosis']
        if kurtosis > 8:
            score += 0.8
        elif kurtosis > 6:
            score += 0.6
        elif kurtosis > 4:
            score += 0.3
        
        # Factor de cresta elevado
        cf = time_feat['crest_factor']
        if cf > 8:
            score += 0.7
        elif cf > 6:
            score += 0.5
        elif cf > 4:
            score += 0.2
        
        # Energía en banda alta (1-5 kHz)
        total_energy = (freq_feat['low_freq_energy'] + 
                       freq_feat['mid_freq_energy'] + 
                       freq_feat['high_freq_energy'])
        if total_energy > 0:
            ratio_hf = freq_feat['high_freq_energy'] / total_energy
            if ratio_hf > 0.4:
                score += 0.6
        
        # RMS elevado
        if time_feat['rms'] > 1.0:
            score += 0.4
        
        return min(1.0, score)
    
    def _score_cavitation(self, time_feat: Dict, freq_feat: Dict) -> float:
        """Calcula score de cavitación"""
        score = 0.0
        
        # RMS muy elevado
        rms = time_feat['rms']
        if rms > 2.0:
            score += 0.7
        elif rms > 1.0:
            score += 0.5
        
        # Ancho de banda elevado
        bw = freq_feat['bandwidth']
        if bw > 3000:
            score += 0.7
        elif bw > 1500:
            score += 0.4
        
        # Energía distribuida en bandas altas
        total_energy = (freq_feat['low_freq_energy'] + 
                       freq_feat['mid_freq_energy'] + 
                       freq_feat['high_freq_energy'])
        if total_energy > 0:
            ratio_hf = freq_feat['high_freq_energy'] / total_energy
            if ratio_hf > 0.3:
                score += 0.6
        
        # Kurtosis moderada (menos que rodamiento)
        kurtosis = time_feat['kurtosis']
        if kurtosis > 4:
            score += 0.3
        
        # Asimetría (skewness) indicador adicional
        skew = abs(time_feat['skewness'])
        if skew > 2:
            score += 0.2
        
        return min(1.0, score)
    
    def _score_misalignment(self, time_feat: Dict, freq_feat: Dict) -> float:
        """Calcula score de desalineamiento"""
        score = 0.0
        
        # Relación 2X/1X > 1
        ratio_2x_1x = freq_feat['2X_amplitude'] / (freq_feat['1X_amplitude'] + 1e-10)
        if ratio_2x_1x > 1.5:
            score += 0.8
        elif ratio_2x_1x > 1.0:
            score += 0.6
        elif ratio_2x_1x > 0.8:
            score += 0.3
        
        # Amplitudes de 4X y 6X significativas
        if freq_feat['4X_amplitude'] > 0.3:
            score += 0.5
        elif freq_feat['4X_amplitude'] > 0.1:
            score += 0.2
        
        if freq_feat['6X_amplitude'] > 0.2:
            score += 0.4
        elif freq_feat['6X_amplitude'] > 0.1:
            score += 0.2
        
        # RMS moderado
        rms = time_feat['rms']
        if 0.3 < rms < 1.5:
            score += 0.3
        
        # Kurtosis cercana a 3-5
        kurtosis = time_feat['kurtosis']
        if 3 < kurtosis < 6:
            score += 0.3
        
        return min(1.0, score)
    
    def _score_unbalance(self, time_feat: Dict, freq_feat: Dict) -> float:
        """Calcula score de desbalance"""
        score = 0.0
        
        # 1X dominante (> 50% de la energía armónica)
        x1_amp = freq_feat['1X_amplitude']
        x2_amp = freq_feat['2X_amplitude']
        
        if x1_amp > 0.5:
            score += 0.7
        elif x1_amp > 0.3:
            score += 0.5
        
        # 2X muy baja comparada con 1X
        ratio_1x_2x = x1_amp / (x2_amp + 1e-10)
        if ratio_1x_2x > 5:
            score += 0.8
        elif ratio_1x_2x > 3:
            score += 0.6
        elif ratio_1x_2x > 2:
            score += 0.3
        
        # Factor de cresta moderado
        cf = time_feat['crest_factor']
        if cf < 5:
            score += 0.5
        elif cf < 7:
            score += 0.3
        
        # Kurtosis cercana a 3
        kurtosis = time_feat['kurtosis']
        if abs(kurtosis - 3.0) < 1.5:
            score += 0.5
        elif abs(kurtosis - 3.0) < 3:
            score += 0.3
        
        return min(1.0, score)
    
    def _score_combined(self, time_feat: Dict, freq_feat: Dict) -> float:
        """Calcula score de falla combinada"""
        score = 0.0
        
        # RMS muy elevado (múltiples defectos requieren amplitud alta)
        rms = time_feat['rms']
        if rms > 1.5:
            score += 0.7
        elif rms > 0.8:
            score += 0.5
        elif rms > 0.4:
            score += 0.2
        
        # Kurtosis elevada (combina impactos + periódico)
        kurtosis = time_feat['kurtosis']
        if kurtosis > 7:
            score += 0.8
        elif kurtosis > 5:
            score += 0.6
        elif kurtosis > 3.5:
            score += 0.3
        
        # Factor de cresta alto
        cf = time_feat['crest_factor']
        if cf > 7:
            score += 0.7
        elif cf > 5:
            score += 0.5
        elif cf > 3:
            score += 0.2
        
        # Múltiples componentes significativas
        x1 = freq_feat['1X_amplitude']
        x2 = freq_feat['2X_amplitude']
        x3 = freq_feat['3X_amplitude']
        x4 = freq_feat['4X_amplitude']
        
        num_components = sum([1 for amp in [x1, x2, x3, x4] if amp > 0.15])
        if num_components >= 3:
            score += 0.6
        elif num_components >= 2:
            score += 0.3
        
        # Energía distribuida en múltiples bandas
        total_energy = (freq_feat['low_freq_energy'] + 
                       freq_feat['mid_freq_energy'] + 
                       freq_feat['high_freq_energy'])
        if total_energy > 0:
            low_ratio = freq_feat['low_freq_energy'] / total_energy
            mid_ratio = freq_feat['mid_freq_energy'] / total_energy
            high_ratio = freq_feat['high_freq_energy'] / total_energy
            
            # Falla combinada tiene energía distribuida
            if 0.2 < low_ratio < 0.8 and 0.2 < mid_ratio < 0.8:
                score += 0.4
        
        return min(1.0, score)
    
    def _assess_severity(self, features: Dict) -> str:
        """
        Evalúa la severidad global de la condición
        
        Args:
            features: Características de la señal
            
        Returns:
            Nivel de severidad
        """
        time_feat = features['time_domain']
        rms = time_feat['rms']
        kurtosis = time_feat['kurtosis']
        cf = time_feat['crest_factor']
        
        # Sistema de puntuación
        severity_score = 0
        
        # RMS
        if rms > 2.0:
            severity_score += 3
        elif rms > 1.0:
            severity_score += 2
        elif rms > 0.5:
            severity_score += 1
        
        # Kurtosis
        if kurtosis > 10:
            severity_score += 3
        elif kurtosis > 6:
            severity_score += 2
        elif kurtosis > 4:
            severity_score += 1
        
        # Factor de cresta
        if cf > 8:
            severity_score += 3
        elif cf > 6:
            severity_score += 2
        elif cf > 4:
            severity_score += 1
        
        if severity_score >= 7:
            return "CRÍTICA"
        elif severity_score >= 5:
            return "SEVERA"
        elif severity_score >= 3:
            return "MODERADA"
        elif severity_score >= 1:
            return "LEVE"
        else:
            return "NORMAL"
    
    def _get_recommendations(self, fault_type: FaultType) -> list:
        """
        Obtiene recomendaciones de mantenimiento
        
        Args:
            fault_type: Tipo de falla detectada
            
        Returns:
            Lista de recomendaciones
        """
        recommendations = {
            FaultType.HEALTHY: [
                "Equipo operando correctamente",
                "Continuar con monitoreo rutinario",
                "Aplicar mantenimiento preventivo según cronograma"
            ],
            FaultType.BEARING: [
               "URGENTE: Planificar reemplazo de rodamiento",
                "Reducir velocidad de operación si es posible",
                "Monitoreo continuo para detectar progresión",
                "Preparar piezas de repuesto"
            ],
            FaultType.CAVITATION: [
                "Revisar condiciones de succión",
                "Verificar NPSH disponible",
                "Inspeccionar impelente por erosión",
                "Considerar cambio de punto de operación"
            ],
            FaultType.MISALIGNMENT: [
                "Alinear ejes acoplados inmediatamente",
                "Verificar alineamiento angular y radial",
                "Usar equipos de alineamiento láser",
                "Inspeccionar flexibles / acoplamientos"
            ],
            FaultType.UNBALANCE: [
                "Ejecutar balanceo dinámico",
                "Verificar fijación de componentes",
                "Revisar rotor por corrosión u obstrucción",
                "Confirmar balanceo de vendededor si es reciente"
            ]
        }
        
        return recommendations.get(fault_type, ["Realizar análisis adicional"])
    
    def _generate_analysis(self, features: Dict, fault_type: FaultType) -> str:
        """
        Genera análisis textual detallado
        
        Args:
            features: Características de la señal
            fault_type: Tipo de falla principal
            
        Returns:
            Análisis detallado en texto
        """
        time_feat = features['time_domain']
        freq_feat = features['frequency_domain']
        
        analysis = f"Análisis de Diagnóstico\n"
        analysis += f"{'='*50}\n\n"
        
        analysis += f"Parámetros Clave:\n"
        analysis += f"  • RMS: {time_feat['rms']:.4f} g\n"
        analysis += f"  • Pico: {time_feat['peak']:.4f} g\n"
        analysis += f"  • Kurtosis: {time_feat['kurtosis']:.2f}\n"
        analysis += f"  • Factor de Cresta: {time_feat['crest_factor']:.2f}\n"
        analysis += f"  • Asimetría: {time_feat['skewness']:.2f}\n\n"
        
        analysis += f"Componentes Armónicos:\n"
        for n in range(1, 7):
            amp = freq_feat.get(f'{n}X_amplitude', 0)
            analysis += f"  • {n}X: {amp:.4f}\n"
        
        return analysis
