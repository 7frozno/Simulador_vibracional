# 🔌 Integración de Sensores Reales - Guía de Implementación

## 📌 Propósito

Este documento proporciona guías completas y código listo para adaptar el simulador
a un **sistema real de recolección de datos** desde sensores de vibración en:

- Bombas
- Compresores  
- Ventiladores
- Otros equipos rotativos

**Estado**: Documentación para proyecto futuro  
**Fecha creación**: Febrero 2026  
**Versión**: Planificación v1.0

---

## 🎯 Arquitectura General

```
SENSORES FÍSICOS
      ↓
INTERFAZ HARDWARE (Clase SensorInterface)
      ↓
RECOLECTOR EN TIEMPO REAL (RealtimeDataCollector)
      ↓
PROCESAMIENTO (Analyzer + Engine)
      ↓
ALMACENAMIENTO (Base de Datos / JSON)
      ↓
VISUALIZACIÓN (Streamlit Dashboard)
      ↓
ALERTAS (Email/SMS/API)
```

---

## 1️⃣ PASO 1: Clase Base para Sensores

Crear archivo: `src/sensor_interface.py`

```python
"""
Interfaz base para sensores de vibración
Define contrato que deben cumplir todos los sensores
"""

from abc import ABC, abstractmethod
from typing import Optional, Dict
import numpy as np


class SensorInterface(ABC):
    """Clase base para todas las interfaces de sensor"""
    
    def __init__(self, device_id: str, sampling_rate: int = 10000):
        """
        Args:
            device_id: Identificador único del dispositivo
            sampling_rate: Frecuencia de muestreo (Hz)
        """
        self.device_id = device_id
        self.sampling_rate = sampling_rate
        self.connected = False
        self.last_error = None
    
    @abstractmethod
    def connect(self) -> bool:
        """Conecta al sensor. Retorna True si éxito"""
        pass
    
    @abstractmethod
    def disconnect(self) -> bool:
        """Desconecta del sensor"""
        pass
    
    @abstractmethod
    def read(self) -> Optional[float]:
        """
        Lee un valor del sensor
        Retorna: valor en g (aceleración gravitacional)
        """
        pass
    
    @abstractmethod
    def read_batch(self, n_samples: int) -> Optional[np.ndarray]:
        """
        Lee n muestras del sensor
        Retorna: array de n valores en g
        """
        pass
    
    def is_connected(self) -> bool:
        """Verifica si sensor está conectado"""
        return self.connected
    
    def get_last_error(self) -> str:
        """Retorna último error reportado"""
        return self.last_error or "No error"


# ============================================================================
# IMPLEMENTACIONES ESPECÍFICAS POR TIPO DE SENSOR
# ============================================================================

class AccelerometerUSB(SensorInterface):
    """
    Sensor acelerómetro conectado por USB
    Ejemplo: Brüel & Kjær, GEOBOX, Dytran, etc.
    """
    
    def __init__(self, device_id: str, com_port: str, sampling_rate: int = 10000):
        super().__init__(device_id, sampling_rate)
        self.com_port = com_port
        self.serial_conn = None
    
    def connect(self) -> bool:
        """Conecta por puerto serial"""
        try:
            import serial
            self.serial_conn = serial.Serial(
                port=self.com_port,
                baudrate=115200,
                timeout=1
            )
            self.connected = True
            return True
        except Exception as e:
            self.last_error = str(e)
            return False
    
    def disconnect(self) -> bool:
        """Desconecta puerto serial"""
        if self.serial_conn:
            self.serial_conn.close()
            self.connected = False
        return True
    
    def read(self) -> Optional[float]:
        """Lee un dato de aceleración"""
        try:
            if self.serial_conn.in_waiting > 0:
                line = self.serial_conn.readline().decode('utf-8').strip()
                return float(line)
        except Exception as e:
            self.last_error = str(e)
        return None
    
    def read_batch(self, n_samples: int) -> Optional[np.ndarray]:
        """Lee n muestras"""
        try:
            samples = []
            for _ in range(n_samples):
                value = self.read()
                if value is not None:
                    samples.append(value)
            return np.array(samples)
        except Exception as e:
            self.last_error = str(e)
        return None


class AccelerometerWiFi(SensorInterface):
    """
    Sensor inalámbrico WiFi
    Ejemplo: Acelerómetro con módulo ESP32
    """
    
    def __init__(self, device_id: str, ip_address: str, port: int = 5000):
        super().__init__(device_id)
        self.ip_address = ip_address
        self.port = port
        self.socket = None
    
    def connect(self) -> bool:
        """Conecta por WiFi"""
        try:
            import socket as sock
            self.socket = sock.socket(sock.AF_INET, sock.SOCK_STREAM)
            self.socket.connect((self.ip_address, self.port))
            self.socket.settimeout(2)
            self.connected = True
            return True
        except Exception as e:
            self.last_error = str(e)
            return False
    
    def disconnect(self) -> bool:
        """Desconecta WiFi"""
        if self.socket:
            self.socket.close()
            self.connected = False
        return True
    
    def read(self) -> Optional[float]:
        """Lee un valor por WiFi"""
        try:
            data = self.socket.recv(1024).decode('utf-8')
            return float(data.strip())
        except Exception as e:
            self.last_error = str(e)
        return None
    
    def read_batch(self, n_samples: int) -> Optional[np.ndarray]:
        """Lee lote de datos"""
        try:
            samples = []
            for _ in range(n_samples):
                value = self.read()
                if value is not None:
                    samples.append(value)
            return np.array(samples) if samples else None
        except Exception as e:
            self.last_error = str(e)
        return None


class AccelerometerDAQ(SensorInterface):
    """
    Tarjeta de adquisición (DAQ) - National Instruments, etc.
    """
    
    def __init__(self, device_id: str, channel: str, sampling_rate: int = 10000):
        super().__init__(device_id, sampling_rate)
        self.channel = channel  # e.g., "Dev1/ai0"
        self.task = None
    
    def connect(self) -> bool:
        """Conecta DAQ"""
        try:
            import nidaqmx
            self.task = nidaqmx.Task()
            self.task.ai_channels.add_ai_voltage_chan(self.channel)
            self.task.timing.cfg_samp_clk_timing(
                self.sampling_rate,
                sample_mode=nidaqmx.constants.AcquisitionType.CONTINUOUS
            )
            self.task.start()
            self.connected = True
            return True
        except Exception as e:
            self.last_error = str(e)
            return False
    
    def disconnect(self) -> bool:
        """Desconecta DAQ"""
        if self.task:
            self.task.close()
            self.connected = False
        return True
    
    def read(self) -> Optional[float]:
        """Lee un valor"""
        try:
            return float(self.task.read())
        except Exception as e:
            self.last_error = str(e)
        return None
    
    def read_batch(self, n_samples: int) -> Optional[np.ndarray]:
        """Lee n muestras a velocidad fs"""
        try:
            samples = self.task.read(number_of_samples_per_channel=n_samples)
            return np.array(samples)
        except Exception as e:
            self.last_error = str(e)
        return None
```

---

## 2️⃣ PASO 2: Recolector en Tiempo Real

Crear archivo: `src/realtime_collector.py`

```python
"""
Recolector de datos en tiempo real desde sensores
Procesa datos mientras se recolectan
"""

import numpy as np
from threading import Thread, Event
from collections import deque
from datetime import datetime
from src.sensor_interface import SensorInterface
from src.signal_analyzer import SignalAnalyzer
from src.diagnostics import DiagnosticEngine
from typing import Callable, Optional, Dict


class RealtimeDataCollector:
    """Recolecta y analiza datos en tiempo real"""
    
    def __init__(self, sensor: SensorInterface, rpm: float = 1500, 
                 window_size: int = 10000, callback: Optional[Callable] = None):
        """
        Args:
            sensor: Instancia de SensorInterface
            rpm: RPM del equipo
            window_size: Número de muestras para análisis
            callback: Función llamada cuando hay nuevo análisis
        """
        self.sensor = sensor
        self.rpm = rpm
        self.window_size = window_size
        self.callback = callback
        
        self.analyzer = SignalAnalyzer(sensor.sampling_rate)
        self.engine = DiagnosticEngine(sensor.sampling_rate, rpm)
        
        self.buffer = deque(maxlen=window_size)
        self.running = False
        self.thread = None
        self.stop_event = Event()
        
        self.measurements_count = 0
        self.last_diagnosis = None
    
    def start(self) -> bool:
        """Inicia recolección en thread separado"""
        if not self.sensor.connect():
            print(f"❌ No se pudo conectar sensor {self.sensor.device_id}")
            return False
        
        self.running = True
        self.stop_event.clear()
        self.thread = Thread(target=self._collect_loop, daemon=False)
        self.thread.start()
        
        print(f"✅ Recolección iniciada: {self.sensor.device_id}")
        return True
    
    def stop(self):
        """Detiene recolección"""
        self.running = False
        self.stop_event.set()
        
        if self.thread:
            self.thread.join(timeout=5)
        
        self.sensor.disconnect()
        print(f"⏹️ Recolección detenida: {self.sensor.device_id}")
    
    def _collect_loop(self):
        """Loop principal de recolección"""
        while self.running and not self.stop_event.is_set():
            # Leer datos
            sample = self.sensor.read()
            
            if sample is not None:
                self.buffer.append(sample)
                
                # Cuando buffer está lleno, analizar
                if len(self.buffer) == self.window_size:
                    signal = np.array(self.buffer)
                    self._analyze_signal(signal)
                    
                    self.measurements_count += 1
    
    def _analyze_signal(self, signal: np.ndarray):
        """Analiza una ventana de datos"""
        try:
            # Análisis de características
            features = self.analyzer.get_all_features(signal, self.rpm)
            
            # Diagnóstico
            diagnosis = self.engine.diagnose(signal)
            
            # Guardar último resultado
            self.last_diagnosis = {
                'timestamp': datetime.now().isoformat(),
                'fault': diagnosis['primary_fault'].value,
                'severity': diagnosis['severity_level'],
                'confidence': diagnosis['confidence'],
                'features': features,
                'diagnosis': diagnosis
            }
            
            # Callback si definido
            if self.callback:
                self.callback(self.last_diagnosis)
        
        except Exception as e:
            print(f"❌ Error en análisis: {e}")
    
    def get_latest_diagnosis(self) -> Optional[Dict]:
        """Retorna último diagnóstico"""
        return self.last_diagnosis
    
    def is_running(self) -> bool:
        """Verifica si está corriendo"""
        return self.running
    
    def get_status(self) -> Dict:
        """Retorna estado actual"""
        return {
            'device_id': self.sensor.device_id,
            'running': self.running,
            'connected': self.sensor.is_connected(),
            'measurements': self.measurements_count,
            'buffer_size': len(self.buffer),
            'last_diagnosis': self.last_diagnosis
        }
```

---

## 3️⃣ PASO 3: Almacenamiento en Base de Datos

Crear archivo: `src/data_storage.py`

```python
"""
Almacenamiento de mediciones en base de datos
"""

import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional


class MeasurementDatabase:
    """Almacena mediciones en SQLite"""
    
    def __init__(self, db_path: str = 'vibraciones.db'):
        self.db_path = db_path
        self.db = sqlite3.connect(db_path, check_same_thread=False)
        self.create_tables()
    
    def create_tables(self):
        """Crea tablas necesarias"""
        
        # Tabla de mediciones
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS measurements (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                fault_type TEXT,
                severity TEXT,
                confidence REAL,
                rms REAL,
                peak REAL,
                kurtosis REAL,
                crest_factor REAL,
                features_json TEXT
            )
        ''')
        
        # Tabla de dispositivos
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS devices (
                device_id TEXT PRIMARY KEY,
                device_type TEXT,
                rpm INTEGER,
                sampling_rate INTEGER,
                location TEXT,
                added_date TEXT
            )
        ''')
        
        # Tabla de alertas
        self.db.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                severity TEXT NOT NULL,
                fault_type TEXT,
                message TEXT,
                acknowledged INTEGER DEFAULT 0
            )
        ''')
        
        self.db.commit()
    
    def register_device(self, device_id: str, device_type: str, 
                       rpm: int, sampling_rate: int, location: str = ""):
        """Registra un nuevo dispositivo"""
        self.db.execute('''
            INSERT OR REPLACE INTO devices 
            (device_id, device_type, rpm, sampling_rate, location, added_date)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (device_id, device_type, rpm, sampling_rate, location, 
              datetime.now().isoformat()))
        self.db.commit()
    
    def save_measurement(self, device_id: str, diagnosis: Dict, 
                        features: Dict):
        """Guarda una medición"""
        time_feat = features['time_domain']
        freq_feat = features['frequency_domain']
        
        self.db.execute('''
            INSERT INTO measurements
            (device_id, timestamp, fault_type, severity, confidence,
             rms, peak, kurtosis, crest_factor, features_json)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            device_id,
            datetime.now().isoformat(),
            diagnosis['primary_fault'].value,
            diagnosis['severity_level'],
            diagnosis['confidence'],
            time_feat['rms'],
            time_feat['peak'],
            time_feat['kurtosis'],
            time_feat['crest_factor'],
            json.dumps(features)
        ))
        self.db.commit()
    
    def save_alert(self, device_id: str, severity: str, 
                   fault_type: str, message: str):
        """Registra una alerta"""
        self.db.execute('''
            INSERT INTO alerts
            (device_id, timestamp, severity, fault_type, message)
            VALUES (?, ?, ?, ?, ?)
        ''', (device_id, datetime.now().isoformat(), severity, fault_type, message))
        self.db.commit()
    
    def get_trend(self, device_id: str, hours: int = 24) -> List[Dict]:
        """Obtiene tendencia de últimas N horas"""
        query = '''
            SELECT timestamp, fault_type, severity, rms, kurtosis, confidence
            FROM measurements
            WHERE device_id = ? 
            AND timestamp > datetime('now', '-' || ? || ' hours')
            ORDER BY timestamp DESC
        '''
        rows = self.db.execute(query, (device_id, hours)).fetchall()
        
        return [{
            'timestamp': row[0],
            'fault_type': row[1],
            'severity': row[2],
            'rms': row[3],
            'kurtosis': row[4],
            'confidence': row[5]
        } for row in rows]
    
    def get_devices(self) -> List[Dict]:
        """Lista todos los dispositivos registrados"""
        rows = self.db.execute('SELECT * FROM devices').fetchall()
        return rows
    
    def get_unacknowledged_alerts(self) -> List[Dict]:
        """Obtiene alertas sin reconocer"""
        query = 'SELECT * FROM alerts WHERE acknowledged = 0'
        rows = self.db.execute(query).fetchall()
        return rows
    
    def acknowledge_alert(self, alert_id: int):
        """Marca alerta como reconocida"""
        self.db.execute(
            'UPDATE alerts SET acknowledged = 1 WHERE id = ?',
            (alert_id,)
        )
        self.db.commit()
    
    def close(self):
        """Cierra la base de datos"""
        self.db.close()
```

---

## 4️⃣ PASO 4: Sistema de Alertas

Crear archivo: `src/alert_system.py`

```python
"""
Sistema de alertas - notificaciones por email, SMS, etc.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import List


class AlertManager:
    """Gestiona alertas y notificaciones"""
    
    def __init__(self, email_config: dict = None):
        self.email_config = email_config or {}
        self.alert_thresholds = {
            'LEVE': ['email'],
            'MODERADA': ['email'],
            'SEVERA': ['email', 'sms'],
            'CRÍTICA': ['email', 'sms', 'phone']
        }
    
    def send_alert(self, device_id: str, severity: str, 
                   fault_type: str, diagnosis: dict):
        """Envía alerta según severidad"""
        
        message = self._format_alert_message(
            device_id, severity, fault_type, diagnosis
        )
        
        if severity in self.alert_thresholds:
            channels = self.alert_thresholds[severity]
            
            if 'email' in channels:
                self.send_email_alert(message)
            
            if 'sms' in channels:
                self.send_sms_alert(message)
            
            if 'phone' in channels:
                self.send_phone_call_alert(device_id)
    
    def send_email_alert(self, message: str):
        """Envía alerta por email"""
        try:
            server = smtplib.SMTP(
                self.email_config.get('smtp_server', 'smtp.gmail.com'),
                self.email_config.get('smtp_port', 587)
            )
            server.starttls()
            server.login(
                self.email_config.get('email', ''),
                self.email_config.get('password', '')
            )
            
            msg = MIMEMultipart()
            msg['From'] = self.email_config.get('email', '')
            msg['To'] = ', '.join(self.email_config.get('recipients', []))
            msg['Subject'] = '🚨 ALERTA VIBRACIONAL'
            
            msg.attach(MIMEText(message, 'plain'))
            
            server.send_message(msg)
            server.quit()
            
            print("✅ Email de alerta enviado")
        except Exception as e:
            print(f"❌ Error enviando email: {e}")
    
    def send_sms_alert(self, message: str):
        """Envía alerta por SMS (requiere Twilio u otro servicio)"""
        try:
            from twilio.rest import Client
            
            account_sid = self.email_config.get('twilio_sid', '')
            auth_token = self.email_config.get('twilio_token', '')
            
            client = Client(account_sid, auth_token)
            
            message = client.messages.create(
                body=message[:160],  # SMS max 160 chars
                from_=self.email_config.get('twilio_phone', ''),
                to=self.email_config.get('recipient_phone', '')
            )
            
            print(f"✅ SMS enviado: {message.sid}")
        except Exception as e:
            print(f"❌ Error enviando SMS: {e}")
    
    def send_phone_call_alert(self, device_id: str):
        """Inicia llamada de alerta (solo para críticas)"""
        print(f"☎️ LLAMADA CRÍTICA para {device_id}")
        # Implementar con vonage, twilio, etc.
    
    def _format_alert_message(self, device_id: str, severity: str,
                              fault_type: str, diagnosis: dict) -> str:
        """Formatea mensaje de alerta"""
        return f"""
ALERTA VIBRACIONAL 🚨

Dispositivo: {device_id}
Severidad: {severity}
Falla Detectada: {fault_type}
Confianza: {diagnosis['confidence']:.1%}

Recomendaciones:
{chr(10).join(['• ' + rec for rec in diagnosis['recommendations'][:3]])}

Acción requerida: Revisar inmediatamente
"""
```

---

## 5️⃣ PASO 5: Dashboard Múltiples Dispositivos

Crear archivo: `app_multidevice.py`

```python
"""
Dashboard para monitoreo de múltiples dispositivos
"""

import streamlit as st
import pandas as pd
from src.data_storage import MeasurementDatabase

st.set_page_config(page_title="Monitor Multi-Equipo", layout="wide")

st.title("🏭 Sistema de Monitoreo Vibracional")
st.subtitle("Múltiples Bombas y Compresores")

# Base de datos
db = MeasurementDatabase('vibraciones.db')

# Tabs principales
tab_overview, tab_devices, tab_history, tab_alerts = st.tabs([
    "📊 Resumen",
    "🔧 Dispositivos",
    "📈 Historial",
    "⚠️ Alertas"
])

# ===== TAB 1: RESUMEN =====
with tab_overview:
    st.header("Estado Actual de Equipos")
    
    devices = db.get_devices()
    
    if devices:
        cols = st.columns(min(3, len(devices)))
        
        for idx, device in enumerate(devices):
            with cols[idx % 3]:
                device_id, device_type, rpm, fs, location = device[:5]
                
                st.subheader(device_id)
                st.write(f"Tipo: {device_type}")
                st.write(f"Ubicación: {location}")
                st.write(f"RPM: {rpm}")
                
                # Último diagnóstico
                trend = db.get_trend(device_id, hours=1)
                if trend:
                    latest = trend[0]
                    st.metric(
                        "Estado",
                        latest['severity'],
                        latest['fault_type']
                    )
    else:
        st.info("📢 No hay dispositivos registrados")

# ===== TAB 2: DISPOSITIVOS =====
with tab_devices:
    st.header("Gestión de Dispositivos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Registrar Nuevo Dispositivo")
        
        device_id = st.text_input("ID del Dispositivo")
        device_type = st.selectbox("Tipo", ["Bomba", "Compresor", "Ventilador"])
        rpm = st.number_input("RPM", value=1500)
        sampling_rate = st.number_input("Frecuencia Muestreo", value=10000)
        location = st.text_input("Ubicación")
        
        if st.button("✅ Registrar"):
            db.register_device(
                device_id, device_type, rpm, sampling_rate, location
            )
            st.success(f"✅ {device_id} registrado")
    
    with col2:
        st.subheader("Dispositivos Activos")
        
        devices = db.get_devices()
        if devices:
            df = pd.DataFrame(
                devices,
                columns=['Device ID', 'Tipo', 'RPM', 'fs', 'Ubicación', 'Añadido']
            )
            st.dataframe(df, use_container_width=True)

# ===== TAB 3: HISTORIAL =====
with tab_history:
    st.header("Historial de Mediciones")
    
    devices = [d[0] for d in db.get_devices()]
    
    if devices:
        selected_device = st.selectbox("Selecciona dispositivo", devices)
        hours = st.slider("Últimas X horas", 1, 168, 24)
        
        trend = db.get_trend(selected_device, hours=hours)
        
        if trend:
            df = pd.DataFrame(trend)
            
            st.subheader(f"Datos de {selected_device}")
            st.dataframe(df, use_container_width=True)
            
            # Gráficos
            col1, col2 = st.columns(2)
            
            with col1:
                st.line_chart(
                    df.set_index('timestamp')['rms'],
                    title="RMS en el Tiempo"
                )
            
            with col2:
                st.line_chart(
                    df.set_index('timestamp')['kurtosis'],
                    title="Kurtosis en el Tiempo"
                )
        else:
            st.info("No hay datos disponibles")

# ===== TAB 4: ALERTAS =====
with tab_alerts:
    st.header("Alertas Generadas")
    
    alerts = db.get_unacknowledged_alerts()
    
    if alerts:
        for alert in alerts[:10]:  # Últimas 10
            alert_id, device_id, timestamp, severity, fault, message, ack = alert
            
            color_map = {
                'LEVE': '🟡',
                'MODERADA': '🟠',
                'SEVERA': '🔴',
                'CRÍTICA': '⚫'
            }
            
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.write(
                    f"{color_map.get(severity, '❓')} "
                    f"**{device_id}** - {severity} - {fault}"
                )
                st.caption(f"⏰ {timestamp}")
            
            with col2:
                if st.button("✅ Reconocer", key=alert_id):
                    db.acknowledge_alert(alert_id)
                    st.rerun()
    else:
        st.success("✅ No hay alertas pendientes")

db.close()
```

---

## 📋 Configuración Recomendada para Producción

### `config_sensores.py`

```python
"""
Configuración para sistema de sensores en producción
"""

# DISPOSITIVOS
DEVICES = {
    'BOMBA_001': {
        'type': 'bomba',
        'rpm': 1500,
        'location': 'Planta A - Succión',
        'sensor_type': 'USB',  # USB, WiFi, DAQ
        'sensor_config': {
            'com_port': 'COM3',
            'baudrate': 115200
        }
    },
    'COMPRESOR_001': {
        'type': 'compresor',
        'rpm': 3600,
        'location': 'Sala de Aire - L1',
        'sensor_type': 'WiFi',
        'sensor_config': {
            'ip_address': '192.168.1.100',
            'port': 5000
        }
    }
}

# ANÁLISIS
ANALYSIS_CONFIG = {
    'sampling_rate': 10000,  # Hz
    'window_size': 10000,    # muestras
    'analysis_interval': 60  # segundos entre análisis
}

# ALERTAS
ALERT_CONFIG = {
    'email_enabled': True,
    'smtp_server': 'smtp.gmail.com',
    'smtp_port': 587,
    'email': 'alerts@empresa.com',
    'password': 'tu_password_aqui',
    'recipients': ['admin@empresa.com', 'mantenimiento@empresa.com'],
    
    'sms_enabled': True,
    'twilio_sid': 'tu_sid',
    'twilio_token': 'tu_token',
    'twilio_phone': '+1234567890',
    'recipient_phone': '+0987654321'
}

# SEVERIDAD DE ALERTAS
ALERT_THRESHOLDS = {
    'rms': {
        'warning': 0.5,     # Amarillo
        'alarm': 1.0,       # Naranja
        'critical': 2.0     # Rojo
    },
    'kurtosis': {
        'warning': 4,
        'alarm': 6,
        'critical': 10
    },
    'crest_factor': {
        'warning': 4,
        'alarm': 6,
        'critical': 8
    }
}

# ALMACENAMIENTO
DATABASE = {
    'path': 'vibraciones.db',
    'retain_days': 365  # Guardar 1 año
}
```

---

## 🚀 Flujo de Implementación Completo

```python
"""
Script principal para sistema completo de monitoreo
"""

from src.sensor_interface import AccelerometerUSB, AccelerometerWiFi
from src.realtime_collector import RealtimeDataCollector
from src.data_storage import MeasurementDatabase
from src.alert_system import AlertManager
from config_sensores import DEVICES, ALERT_CONFIG
import time


def setup_sensors():
    """Configura todos los sensores"""
    collectors = {}
    
    for device_id, config in DEVICES.items():
        
        # Crear sensor
        if config['sensor_type'] == 'USB':
            sensor = AccelerometerUSB(
                device_id,
                config['sensor_config']['com_port'],
                sampling_rate=10000
            )
        elif config['sensor_type'] == 'WiFi':
            sensor = AccelerometerWiFi(
                device_id,
                config['sensor_config']['ip_address'],
                config['sensor_config']['port']
            )
        
        # Crear recolector
        db = MeasurementDatabase()
        alert_mgr = AlertManager(ALERT_CONFIG)
        
        def on_analysis(result):
            # Guardar medición
            db.save_measurement(device_id, result['diagnosis'], result['features'])
            
            # Alerta si necesario
            if result['diagnosis']['severity_level'] in ['SEVERA', 'CRÍTICA']:
                alert_mgr.send_alert(
                    device_id,
                    result['diagnosis']['severity_level'],
                    result['diagnosis']['primary_fault'].value,
                    result['diagnosis']
                )
        
        collector = RealtimeDataCollector(
            sensor,
            rpm=config['rpm'],
            callback=on_analysis
        )
        
        if collector.start():
            collectors[device_id] = collector
            print(f"✅ {device_id} iniciado")
    
    return collectors


def main():
    """Ejecuta monitoreo continuo"""
    collectors = setup_sensors()
    
    try:
        # Monitoreo continuo
        while True:
            for device_id, collector in collectors.items():
                status = collector.get_status()
                diagnosis = status['last_diagnosis']
                
                if diagnosis:
                    print(f"{device_id}: {diagnosis['severity']}")
            
            time.sleep(30)  # Actulizar cada 30s
    
    except KeyboardInterrupt:
        print("\n⏹️ Deteniendo...")
        for collector in collectors.values():
            collector.stop()


if __name__ == '__main__':
    main()
```

---

## 📝 Checklist para Implementación

- [ ] Sensor hardware seleccionado y obtornillado
- [ ] Clase `SensorInterface` personalizada para tu sensor
- [ ] `RealtimeDataCollector` configurado
- [ ] `MeasurementDatabase` con esquema apropiado
- [ ] `AlertManager` con configuración de email/SMS
- [ ] `app_multidevice.py` desplegado
- [ ] Pruebas con datos reales
- [ ] Configuración de alertas validada
- [ ] Backup automático de base de datos
- [ ] Documentación de operación

---

## 🔗 Recursos Útiles

- **Sensores USB**: Brüel & Kjær, GEOBOX, Dytran
- **Sensores WiFi**: Arduino + ESP32, ThingSpeak
- **DAQ**: National Instruments DAQmx, ADLINK
- **Alertas**: Twilio (SMS), SendGrid (Email)
- **Base Datos**: SQLite (local), PostgreSQL (servidor)

---

**Documento completo guardado para futuro proyecto de sensores 🎯**
