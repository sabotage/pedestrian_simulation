# 🚀 Windows 快速安装 - C:\ymq\projects\

## 📥 安装到 C:\ymq\projects\

### 方法一：直接复制（最简单）

1. **下载项目**
   - 从Claude下载整个 `pedestrian_simulation` 文件夹

2. **复制到目标位置**
   ```
   将 pedestrian_simulation 文件夹复制到:
   C:\ymq\projects\
   
   最终路径应该是:
   C:\ymq\projects\pedestrian_simulation\
   ```

3. **打开命令提示符**
   - 按 `Win + R`
   - 输入 `cmd` 回车
   
4. **进入项目目录**
   ```cmd
   cd C:\ymq\projects\pedestrian_simulation
   ```

5. **一键安装**
   ```cmd
   install.bat
   ```
   
   或使用PowerShell（更好的体验）：
   ```powershell
   # 右键点击 install.ps1 → "使用PowerShell运行"
   ```

### 方法二：使用PowerShell（推荐）

1. **打开PowerShell**
   - 按 `Win + X`
   - 选择 "Windows PowerShell (管理员)"

2. **创建目录并进入**
   ```powershell
   # 创建父目录（如果不存在）
   New-Item -ItemType Directory -Path "C:\ymq\projects" -Force
   
   # 进入目录
   cd C:\ymq\projects
   ```

3. **复制项目文件夹到此处**
   ```
   将下载的 pedestrian_simulation 文件夹放到这里
   ```

4. **运行安装脚本**
   ```powershell
   cd pedestrian_simulation
   
   # 设置执行策略（首次需要）
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   
   # 运行安装
   .\install.ps1
   ```

---

## ✅ 验证安装

安装完成后，测试一下：

```cmd
cd C:\ymq\projects\pedestrian_simulation
python test_system.py
```

如果看到 "✅ 所有测试通过!"，说明安装成功！

---

## 🎯 快速启动

### 启动Web编辑器
```cmd
cd C:\ymq\projects\pedestrian_simulation
python start.py --web
```
打开浏览器访问: http://localhost:5000

### 运行示例
```cmd
# 基础疏散示例
python start.py --example 1

# 火灾应急示例
python start.py --example 2
```

### 交互式菜单
```cmd
python start.py
```
然后按照菜单提示操作

---

## 📁 目录结构确认

确保你的目录结构如下：

```
C:\ymq\projects\pedestrian_simulation\
├── core\
├── server\
├── visualization\
├── unity_integration\
├── examples\
├── README.md
├── install.bat        ← Windows批处理安装
├── install.ps1        ← PowerShell安装
└── requirements.txt
```

---

## 🔧 前置要求

### 1. Python 3.8+

检查是否已安装：
```cmd
python --version
```

如果未安装：
1. 访问 https://www.python.org/downloads/
2. 下载Python 3.8或更高版本
3. 安装时**勾选** "Add Python to PATH"

### 2. Git（可选）

如果想通过Git克隆：
```cmd
cd C:\ymq\projects
git clone [项目地址]
```

---

## 🐛 常见问题

### Q: 找不到 python 命令
**A:** Python未添加到PATH
- 重新安装Python，确保勾选 "Add Python to PATH"
- 或手动添加到系统环境变量

### Q: pip 安装很慢
**A:** 使用国内镜像
```cmd
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q: 权限错误
**A:** 以管理员身份运行
- 右键 `cmd` 或 `PowerShell` → "以管理员身份运行"

### Q: install.ps1 无法运行
**A:** PowerShell执行策略限制
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

### Q: 端口5000被占用
**A:** 更改端口
```cmd
python start.py --web --port 8080
```

---

## 📚 文档位置

安装完成后，所有文档都在项目目录中：

```
C:\ymq\projects\pedestrian_simulation\
├── README.md                    ← 主文档，从这里开始
├── QUICK_REFERENCE.md           ← 命令速查表
├── PROJECT_OVERVIEW.md          ← 技术细节
├── WINDOWS_INSTALL.md           ← Windows详细安装
└── unity_integration\
    └── UNITY_INTEGRATION_GUIDE.md  ← Unity VR集成
```

---

## 🎓 下一步

1. **查看主文档**
   ```cmd
   cd C:\ymq\projects\pedestrian_simulation
   start README.md
   ```

2. **尝试Web编辑器**
   ```cmd
   python start.py --web
   ```

3. **运行一个示例**
   ```cmd
   python examples\example_1_basic_evacuation.py
   ```

4. **学习API**
   - 查看 `examples\` 目录中的示例代码
   - 阅读 `PROJECT_OVERVIEW.md` 了解架构

---

## 🎉 完成！

你现在已经在 `C:\ymq\projects\pedestrian_simulation` 安装好了完整的系统！

**开始探索吧！** 🚀

---

## 💡 提示

- 创建桌面快捷方式：
  ```
  右键 start.py → 发送到 → 桌面快捷方式
  ```

- 添加到开始菜单：
  ```
  创建 start.bat 文件:
  @echo off
  cd C:\ymq\projects\pedestrian_simulation
  python start.py
  pause
  ```

- 使用虚拟环境（推荐）：
  ```cmd
  cd C:\ymq\projects\pedestrian_simulation
  python -m venv venv
  venv\Scripts\activate
  pip install -r requirements.txt
  ```

---

**祝使用愉快！** 如有问题请查看 `README.md` 或 `WINDOWS_INSTALL.md`
