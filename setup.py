"""
Script de instalación y configuración inicial
"""

import subprocess
import sys
from pathlib import Path


def check_python_version():
    """Verifica que la versión de Python sea compatible"""
    if sys.version_info < (3, 8):
        print("❌ Se requiere Python 3.8 o superior")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor} detectado")


def install_requirements():
    """Instala las dependencias"""
    print("\n📦 Instalando dependencias...")
    
    requirements_file = Path(__file__).parent / "requirements.txt"
    
    try:
        subprocess.check_call([
            sys.executable, "-m", "pip", "install", 
            "-r", str(requirements_file)
        ])
        print("✓ Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError:
        print("❌ Error al instalar dependencias")
        return False


def verify_installation():
    """Verifica que todos los módulos estén disponibles"""
    print("\n🔍 Verificando instalación...")
    
    required_packages = [
        'numpy',
        'scipy',
        'matplotlib',
        'plotly',
        'streamlit',
        'pandas',
        'sklearn'
    ]
    
    failed = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {package}")
        except ImportError:
            print(f"  ❌ {package} - NO ENCONTRADO")
            failed.append(package)
    
    if failed:
        print(f"\n⚠️ Paquetes no encontrados: {', '.join(failed)}")
        print("Intenta ejecutar: pip install -r requirements.txt")
        return False
    
    print("\n✓ Todos los paquetes requeridos están instalados")
    return True


def setup_project_structure():
    """Verifica que la estructura del proyecto sea correcta"""
    print("\n📁 Verificando estructura del proyecto...")
    
    base_path = Path(__file__).parent
    required_dirs = ['src', 'examples', 'data']
    required_files = [
        'src/__init__.py',
        'src/signal_generator.py',
        'src/signal_analyzer.py',
        'src/fault_simulator.py',
        'src/diagnostics.py',
        'src/utils.py',
        'app.py',
        'config.py',
        'requirements.txt'
    ]
    
    # Verificar directorios
    all_ok = True
    for dir_name in required_dirs:
        dir_path = base_path / dir_name
        if dir_path.exists():
            print(f"  ✓ Directorio {dir_name}")
        else:
            print(f"  ❌ Directorio {dir_name} - NO ENCONTRADO")
            dir_path.mkdir(parents=True, exist_ok=True)
            all_ok = False
    
    # Verificar archivos
    for file_name in required_files:
        file_path = base_path / file_name
        if file_path.exists():
            print(f"  ✓ Archivo {file_name}")
        else:
            print(f"  ⚠️ Archivo {file_name} - NO ENCONTRADO")
            all_ok = False
    
    if all_ok:
        print("\n✓ Estructura del proyecto correcta")
    
    return all_ok


def main():
    """Ejecuta la configuración inicial"""
    
    print("\n" + "="*60)
    print("🔧 CONFIGURACIÓN INICIAL - SIMULADOR VIBRACIONAL")
    print("="*60 + "\n")
    
    # Verificar Python
    check_python_version()
    
    # Verificar estructura
    setup_project_structure()
    
    # Instalar requisitos
    if not install_requirements():
        print("\n❌ Instalación fallida")
        sys.exit(1)
    
    # Verificar instalación
    if not verify_installation():
        print("\n⚠️ Algunos paquetes tienen problemas")
        print("Solución: Ejecuta: pip install --upgrade -r requirements.txt")
    else:
        print("\n" + "="*60)
        print("✅ INSTALACIÓN COMPLETADA EXITOSAMENTE")
        print("="*60)
        print("\n🚀 Próximos pasos:")
        print("   1. Ejecuta: streamlit run app.py")
        print("   2. O ejecuta: python examples/sample_analysis.py")
        print("\n📖 Para más información, lee: QUICK_START.md")
        print()


if __name__ == "__main__":
    main()
