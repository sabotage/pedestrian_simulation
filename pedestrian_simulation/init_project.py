"""
Project Initialization Script
Automatically create necessary directory structure and check dependencies
"""
import os
import sys
from pathlib import Path
import subprocess

def create_directory_structure():
    """Create project directory structure"""
    
    base_dir = Path(__file__).parent
    
    directories = [
        'core',
        'server/templates',
        'server/static',
        'visualization',
        'unity_integration',
        'examples',
        'scenarios',
        'exports',
        'data',
        'logs'
    ]
    
    print("Creating directory structure...")
    for directory in directories:
        dir_path = base_dir / directory
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"  ✓ {directory}/")
    
    print("\nDirectory structure created!")

def check_dependencies():
    """Check Python dependencies"""
    
    print("\nCheck Python dependencies...")
    
    required_packages = {
        'numpy': 'numpy',
        'matplotlib': 'matplotlib',
        'flask': 'flask',
        'flask_cors': 'flask-cors',
        'scipy': 'scipy',
    }
    
    missing_packages = []
    
    for import_name, install_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"  ✓ {install_name}")
        except ImportError:
            print(f"  ✗ {install_name} (not installed)")
            missing_packages.append(install_name)
    
    if missing_packages:
        print(f"\nMissing dependencies:")
        for pkg in missing_packages:
            print(f"  - {pkg}")
        
        print("\nPlease run the following command to install:")
        print(f"  pip install {' '.join(missing_packages)}")
        return False
    else:
        print("\nAll dependencies installed!")
        return True

def check_ffmpeg():
    """Check FFmpeg (for video export)"""
    
    print("\nChecking FFmpeg...")
    
    try:
        result = subprocess.run(
            ['ffmpeg', '-version'],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("  ✓ FFmpeg installed")
            return True
    except FileNotFoundError:
        pass
    
    print("  ℹ️  FFmpeg not installed (optional, for exporting video animations)")
    print("     Installation:")
    print("     - Ubuntu/Debian: sudo apt-get install ffmpeg")
    print("     - macOS: brew install ffmpeg")
    print("     - Windows: Download from https://ffmpeg.org")
    
    return False

def create_example_config():
    """Create example configuration file"""
    
    print("\nCreating example configuration...")
    
    config_path = Path(__file__).parent / 'scenarios' / 'example_scenario.json'
    
    example_config = {
        "name": "示例场景",
        "width": 40,
        "height": 40,
        "obstacles": [
            {
                "vertices": [[0, 0], [40, 0], [40, 40], [0, 40]]
            }
        ],
        "exits": [
            {
                "position": [20, 0],
                "width": 3.0
            }
        ],
        "pedestrian_spawn": {
            "count": 50,
            "areas": [
                {
                    "x_min": 5,
                    "x_max": 35,
                    "y_min": 5,
                    "y_max": 35
                }
            ]
        }
    }
    
    import json
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(example_config, f, indent=2, ensure_ascii=False)
    
    print(f"  ✓ 示例场景配置已创建: {config_path}")

def print_next_steps():
    """打印后续Step"""
    
    print("\n" + "="*60)
    print("Initialization Complete!")
    print("="*60)
    
    print("\nQuick Start:")
    print("\n1. 使用Web编辑器:")
    print("   cd server")
    print("   python app.py")
    print("   然后访问: http://localhost:5000")
    
    print("\n2. Run Examples:")
    print("   python examples/example_1_basic_evacuation.py")
    
    print("\n3. 查看完整文档:")
    print("   查看 README.md 文件")
    
    print("\n" + "="*60)

def main():
    """主函数"""
    
    print("="*60)
    print("行人运动模拟系统 - 初始化")
    print("="*60)
    
    # Create directories
    create_directory_structure()
    
    # Check dependencies
    deps_ok = check_dependencies()
    
    # Check FFmpeg
    check_ffmpeg()
    
    # Create example configuration
    create_example_config()
    
    # 打印后续Step
    print_next_steps()
    
    if not deps_ok:
        print("\n⚠️  请先安装缺失的依赖包!")
        sys.exit(1)

if __name__ == '__main__':
    main()
