#!/bin/bash
# Instalador automatico para Simulador de Análisis Vibracional
# Para Linux/Mac

echo ""
echo "============================================================================"
echo "  SIMULADOR DE ANALISIS VIBRACIONAL - Instalador automatico"
echo "============================================================================"
echo ""

# Verificar Python
echo "Verificando Python..."
if ! command -v python3 &> /dev/null
then
    echo "ERROR: Python 3 no encontrado"
    echo "Descargalo desde https://www.python.org/downloads/"
    exit 1
fi

python3 --version

# Actualizar pip
echo ""
echo "Actualizando pip..."
python3 -m pip install --upgrade pip

# Instalar dependencias
echo ""
echo "Instalando dependencias (esto puede tomar 2-3 minutos)..."
pip3 install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "ERROR: Fallo la instalacion"
    echo "Intenta: pip3 install --upgrade -r requirements.txt"
    exit 1
fi

echo ""
echo "============================================================================"
echo "  INSTALACION COMPLETADA CON EXITO"
echo "============================================================================"
echo ""
echo "Para ejecutar la aplicacion:"
echo "  streamlit run app.py"
echo ""
echo "Esta abrira la interfaz en: http://localhost:8501"
echo ""
echo "Para ejecutar ejemplos:"
echo "  python3 examples/sample_analysis.py"
echo ""
echo "Para validar la instalacion:"
echo "  python3 tests.py"
echo ""
echo "============================================================================"
echo ""
