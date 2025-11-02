#!/usr/bin/env python3
"""
Quick Start Script
One-click start for Web server and visualization system
"""

import sys
import os
import subprocess
import argparse
from pathlib import Path

def check_dependencies():
    """检查依赖是否installed"""
    try:
        import numpy
        import matplotlib
        import flask
        import flask_cors
        return True
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("\nPlease run the following command to install依赖:")
        print("  pip install -r requirements.txt")
        return False

def start_web_server(port=5000):
    """Start Web server"""
    print(f"🚀 Start Web server (端口: {port})...")
    print(f"   访问: http://localhost:{port}")
    print("\n按 Ctrl+C 停止服务器\n")
    
    server_path = Path(__file__).parent / 'server' / 'app.py'
    
    try:
        subprocess.run(
            [sys.executable, str(server_path)],
            env={**os.environ, 'FLASK_ENV': 'development'}
        )
    except KeyboardInterrupt:
        print("\n\n👋 服务器已停止")

def run_example(example_number):
    """Run Examples"""
    examples = {
        1: 'example_1_basic_evacuation.py',
        2: 'example_2_fire_emergency.py'
    }
    
    if example_number not in examples:
        print(f"❌ 示例 {example_number} does not exist")
        print(f"可用示例: {list(examples.keys())}")
        return
    
    example_path = Path(__file__).parent / 'examples' / examples[example_number]
    
    if not example_path.exists():
        print(f"❌ 示例文件does not exist: {example_path}")
        return
    
    print(f"🎬 Run Examples {example_number}...")
    subprocess.run([sys.executable, str(example_path)])

def show_menu():
    """显示交互式菜单"""
    print("="*60)
    print("行人运动模拟系统 - 快速启动")
    print("="*60)
    print("\n请选择:")
    print("1. Start Web Editor")
    print("2. Run Examples1 - 基础疏散")
    print("3. Run Examples2 - Fire应急")
    print("4. Initialize project")
    print("5. 查看帮助")
    print("0. 退出")
    print("\n" + "="*60)
    
    choice = input("\n请输入选项 (0-5): ").strip()
    
    if choice == '1':
        start_web_server()
    elif choice == '2':
        run_example(1)
    elif choice == '3':
        run_example(2)
    elif choice == '4':
        init_path = Path(__file__).parent / 'init_project.py'
        subprocess.run([sys.executable, str(init_path)])
    elif choice == '5':
        show_help()
    elif choice == '0':
        print("👋 再见!")
        sys.exit(0)
    else:
        print("❌ 无效选项")
        show_menu()

def show_help():
    """显示帮助信息"""
    print("\n" + "="*60)
    print("帮助信息")
    print("="*60)
    print("\n命令行用法:")
    print("  python start.py                  # 显示交互式菜单")
    print("  python start.py --web            # Start Web server")
    print("  python start.py --example 1      # Run Examples1")
    print("  python start.py --port 8080      # 指定端口")
    print("\n更多信息:")
    print("  - 查看 README.md 了解详细文档")
    print("  - 查看 examples/ 目录中的示例代码")
    print("  - 查看 unity_integration/ 目录了解Unity集成")
    print("="*60 + "\n")

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='行人运动模拟系统启动器')
    parser.add_argument('--web', action='store_true', help='Start Web server')
    parser.add_argument('--example', type=int, help='运行指定示例 (1或2)')
    parser.add_argument('--port', type=int, default=5000, help='Web服务器端口')
    parser.add_argument('--init', action='store_true', help='Initialize project')
    
    args = parser.parse_args()
    
    # 检查依赖
    if not check_dependencies():
        sys.exit(1)
    
    # 根据参数执行
    if args.init:
        init_path = Path(__file__).parent / 'init_project.py'
        subprocess.run([sys.executable, str(init_path)])
    elif args.web:
        start_web_server(args.port)
    elif args.example:
        run_example(args.example)
    else:
        # 显示交互式菜单
        show_menu()

if __name__ == '__main__':
    main()
