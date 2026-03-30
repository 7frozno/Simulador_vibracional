"""
Archivo de configuración del simulador
"""

# Configuración de señal
SAMPLING_RATE = 10000  # Hz
DURATION = 1.0  # segundos
RPM = 1500  # Revoluciones por minuto
AMPLITUDE_BASE = 1.0  # g (unidades de aceleración)

# Configuración de análisis
FFT_MAX_FREQUENCY = 5000  # Hz
NUM_FFT_POINTS = 2048

# Configuración de filtros
BANDPASS_LOW = 50  # Hz
BANDPASS_HIGH = 5000  # Hz
FILTER_ORDER = 4

# Configuración de UI
PLOT_STYLE = "seaborn-v0_8-darkgrid"
FIGURE_DPI = 100
FIGURE_SIZE = (12, 6)

# Configuración de diagnóstico
CONFIDENCE_THRESHOLD = 0.4
SEVERITY_LEVELS = {
    'NORMAL': (0, 1),
    'LEVE': (1, 3),
    'MODERADA': (3, 5),
    'SEVERA': (5, 7),
    'CRÍTICA': (7, float('inf'))
}

# Colores para visualización
COLORS = {
    'healthy': '#2ecc71',      # Verde
    'light': '#f39c12',        # Naranja
    'moderate': '#e74c3c',     # Rojo claro
    'severe': '#c0392b',       # Rojo oscuro
    'critical': '#8b0000'      # Rojo muy oscuro
}

# Equipos soportados
EQUIPMENT_TYPES = {
    'bomba': {
        'rpm_typical': 1500,
        'description': 'Bomba centrífuga'
    },
    'compresor': {
        'rpm_typical': 3600,
        'description': 'Compresor rotativo'
    },
    'ventilador': {
        'rpm_typical': 1200,
        'description': 'Ventilador industrial'
    },
    'motor': {
        'rpm_typical': 1800,
        'description': 'Motor eléctrico'
    }
}

# Parámetros típicos de alarma
ALARM_THRESHOLDS = {
    'rms': {
        'warning': 0.5,    # g
        'alarm': 1.0,      # g
        'fault': 2.0       # g
    },
    'kurtosis': {
        'warning': 4,
        'alarm': 6,
        'fault': 10
    },
    'crest_factor': {
        'warning': 4,
        'alarm': 6,
        'fault': 8
    }
}
