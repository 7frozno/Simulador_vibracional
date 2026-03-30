@echo off
REM Instalador automatico para Simulador de Análisis Vibracional
REM Para Windows

echo.
echo ============================================================================
echo  SIMULADOR DE ANALISIS VIBRACIONAL - Instalador automatico
echo ============================================================================
echo.

echo Verificando Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python no encontrado. Descargalo de https://www.python.org/downloads/
    echo Asegurate de marcar "Add Python to PATH" durante la instalacion
    pause
    exit /b 1
)

echo OK: Python detectado

echo.
echo Actualizando pip...
python -m pip install --upgrade pip

echo.
echo Instalando dependencias (esto puede tomar 2-3 minutos)...
pip install -r requirements.txt

if errorlevel 1 (
    echo ERROR: Fallo la instalacion
    echo Intenta ejecutar: pip install --upgrade -r requirements.txt
    pause
    exit /b 1
)

echo.
echo ============================================================================
echo  INSTALACION COMPLETADA CON EXITO
echo ============================================================================
echo.
echo Para ejecutar la aplicacion:
echo   streamlit run app.py
echo.
echo Esta abrira la interfaz en: http://localhost:8501
echo.
echo Para ejecutar ejemplos:
echo   python examples\sample_analysis.py
echo.
echo Para validar la instalacion:
echo   python tests.py
echo.
echo ============================================================================
echo.
pause
