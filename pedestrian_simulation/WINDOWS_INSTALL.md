# Windows 安装指南 🪟

## 📥 安装步骤

### 方式一：手动创建（推荐）

#### 步骤1: 创建项目目录
```cmd
# 打开命令提示符 (Win + R, 输入 cmd)
mkdir C:\ymq\projects\pedestrian_simulation
cd C:\ymq\projects\pedestrian_simulation
```

#### 步骤2: 下载项目文件
1. 从Claude下载 `pedestrian_simulation.tar.gz`
2. 使用7-Zip或WinRAR解压到 `C:\ymq\projects\pedestrian_simulation`

或者，直接复制已解压的 `pedestrian_simulation` 文件夹到 `C:\ymq\projects\`

#### 步骤3: 安装Python（如果还没安装）
1. 访问 https://www.python.org/downloads/
2. 下载 Python 3.8 或更高版本
3. 安装时**勾选** "Add Python to PATH"
4. 验证安装:
```cmd
python --version
pip --version
```

#### 步骤4: 安装依赖
```cmd
cd C:\ymq\projects\pedestrian_simulation
pip install -r requirements.txt
```

如果遇到网络问题，使用国内镜像：
```cmd
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 步骤5: 初始化项目
```cmd
python init_project.py
```

#### 步骤6: 运行测试
```cmd
python test_system.py
```

---

### 方式二：使用PowerShell脚本（自动化）

创建文件 `install.ps1`:

```powershell
# Windows PowerShell 安装脚本
Write-Host "开始安装行人运动模拟系统..." -ForegroundColor Green

# 检查Python
Write-Host "`n检查Python..." -ForegroundColor Yellow
try {
    $pythonVersion = python --version
    Write-Host "✓ Python已安装: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "✗ 未找到Python，请先安装Python 3.8+" -ForegroundColor Red
    Write-Host "下载地址: https://www.python.org/downloads/" -ForegroundColor Cyan
    exit 1
}

# 创建目录
Write-Host "`n创建项目目录..." -ForegroundColor Yellow
$projectPath = "C:\ymq\projects\pedestrian_simulation"

if (!(Test-Path $projectPath)) {
    New-Item -ItemType Directory -Path $projectPath -Force | Out-Null
    Write-Host "✓ 目录已创建: $projectPath" -ForegroundColor Green
} else {
    Write-Host "✓ 目录已存在: $projectPath" -ForegroundColor Green
}

# 切换到项目目录
Set-Location $projectPath

# 安装依赖
Write-Host "`n安装Python依赖..." -ForegroundColor Yellow
pip install -r requirements.txt

if ($LASTEXITCODE -eq 0) {
    Write-Host "✓ 依赖安装成功" -ForegroundColor Green
} else {
    Write-Host "✗ 依赖安装失败" -ForegroundColor Red
    exit 1
}

# 初始化项目
Write-Host "`n初始化项目..." -ForegroundColor Yellow
python init_project.py

# 运行测试
Write-Host "`n运行系统测试..." -ForegroundColor Yellow
python test_system.py

Write-Host "`n✓ 安装完成!" -ForegroundColor Green
Write-Host "`n快速开始:" -ForegroundColor Cyan
Write-Host "  python start.py --web     # 启动Web编辑器" -ForegroundColor White
Write-Host "  python start.py --example 1   # 运行示例" -ForegroundColor White
```

运行脚本：
```powershell
# 以管理员身份运行PowerShell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\install.ps1
```

---

## 🚀 快速启动

### 启动Web编辑器
```cmd
cd C:\ymq\projects\pedestrian_simulation
python start.py --web
```
然后打开浏览器访问: http://localhost:5000

### 运行示例
```cmd
# 基础疏散场景
python start.py --example 1

# 火灾应急场景
python start.py --example 2
```

### Python编程
```cmd
# 创建你的脚本
notepad my_simulation.py
```

```python
from core.pedestrian_model import SimulationEnvironment
import numpy as np

env = SimulationEnvironment(width=50, height=50)
# ... 你的代码
```

---

## 🔧 Windows特定配置

### 1. 防火墙设置
如果Web服务器无法访问：
```
控制面板 → Windows Defender 防火墙 → 允许应用通过防火墙
→ 勾选 Python
```

### 2. 路径问题
Windows使用反斜杠 `\`，代码中已自动处理：
```python
from pathlib import Path
path = Path("C:/ymq/projects/pedestrian_simulation")  # 这样也可以
```

### 3. 编码问题
如果遇到中文乱码，在Python文件开头添加：
```python
# -*- coding: utf-8 -*-
```

### 4. 虚拟环境（推荐）
```cmd
cd C:\ymq\projects\pedestrian_simulation

# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 退出虚拟环境
deactivate
```

---

## 📊 可选：安装FFmpeg（用于视频导出）

### 方式一：使用Chocolatey
```powershell
# 安装Chocolatey（如果没有）
Set-ExecutionPolicy Bypass -Scope Process -Force
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072
iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))

# 安装FFmpeg
choco install ffmpeg
```

### 方式二：手动安装
1. 访问 https://www.gyan.dev/ffmpeg/builds/
2. 下载 "ffmpeg-release-essentials.zip"
3. 解压到 `C:\ffmpeg`
4. 添加到PATH:
   - 右键"此电脑" → 属性 → 高级系统设置 → 环境变量
   - 在"系统变量"中找到"Path"，点击编辑
   - 添加 `C:\ffmpeg\bin`
5. 验证: 打开新的CMD窗口，输入 `ffmpeg -version`

---

## 🎮 Unity集成（Windows）

### 1. 安装Unity Hub
下载：https://unity.com/download

### 2. 安装Unity Editor
推荐版本：Unity 2020.3 LTS 或更新

### 3. 导出数据
```cmd
cd C:\ymq\projects\pedestrian_simulation
python examples\example_2_fire_emergency.py
```
数据将保存在 `exports\fire_emergency.json`

### 4. 导入Unity
1. 创建新的Unity 3D项目
2. 将 `unity_integration\` 文件夹中的 `.cs` 脚本复制到Unity项目的 `Assets\Scripts\`
3. 将导出的JSON文件复制到 `Assets\Data\`
4. 按照 `UNITY_INTEGRATION_GUIDE.md` 配置场景

---

## 🐛 Windows常见问题

### Q1: "python不是内部或外部命令"
**解决**:
1. 重新安装Python，确保勾选"Add to PATH"
2. 或手动添加Python到环境变量：
   - 找到Python安装路径（如 `C:\Users\你的用户名\AppData\Local\Programs\Python\Python311`）
   - 添加到PATH环境变量

### Q2: pip安装速度慢
**解决**: 使用国内镜像
```cmd
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q3: 权限错误
**解决**: 以管理员身份运行CMD
- 右键CMD → "以管理员身份运行"

### Q4: 端口5000被占用
**解决**: 更改端口
```cmd
python start.py --web --port 8080
```

### Q5: numpy等安装失败
**解决**: 安装Visual C++ Build Tools
- 下载：https://visualstudio.microsoft.com/visual-cpp-build-tools/
- 或使用预编译版本：
```cmd
pip install numpy -i https://pypi.tuna.tsinghua.edu.cn/simple
```

---

## 📁 目录结构检查

确保你的目录结构如下：

```
C:\ymq\projects\pedestrian_simulation\
├── core\
│   ├── __init__.py
│   └── pedestrian_model.py
├── server\
│   ├── app.py
│   └── templates\
│       └── editor.html
├── visualization\
│   └── visualizer.py
├── unity_integration\
│   ├── SimulationDataLoader.cs
│   ├── SimulationUIController.cs
│   └── UNITY_INTEGRATION_GUIDE.md
├── examples\
│   ├── example_1_basic_evacuation.py
│   └── example_2_fire_emergency.py
├── scenarios\
├── exports\
├── data\
├── logs\
├── README.md
├── requirements.txt
├── start.py
├── init_project.py
└── test_system.py
```

---

## ✅ 验证安装

运行完整测试：
```cmd
cd C:\ymq\projects\pedestrian_simulation
python test_system.py
```

如果看到 "✅ 所有测试通过!"，说明安装成功！

---

## 🎯 下一步

1. **阅读文档**
   ```cmd
   # 在Windows资源管理器中打开
   explorer C:\ymq\projects\pedestrian_simulation
   # 阅读 README.md
   ```

2. **启动Web编辑器**
   ```cmd
   python start.py --web
   ```

3. **运行示例**
   ```cmd
   python start.py --example 1
   ```

4. **开始开发**
   ```python
   # 创建你的第一个脚本
   # my_first_simulation.py
   ```

---

## 📞 获取帮助

- 查看文档: `README.md`
- 快速参考: `QUICK_REFERENCE.md`
- 项目总览: `PROJECT_OVERVIEW.md`
- Unity集成: `unity_integration\UNITY_INTEGRATION_GUIDE.md`

---

## 🎉 安装完成

恭喜！你已经在Windows上成功设置了行人运动模拟系统。

**享受使用吧！** 🚀

---

*Windows安装指南 v1.0*  
*适用于 Windows 10/11*
