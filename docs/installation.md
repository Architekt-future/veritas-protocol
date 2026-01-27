# 📦 Installation Guide

This guide will help you install and set up Veritas Protocol on your system.

---

## 📋 Prerequisites

### System Requirements

- **Python:** 3.9 or higher
- **OS:** Linux, macOS, or Windows
- **RAM:** Minimum 512MB (recommended 1GB+)
- **Disk Space:** ~150MB for installation

### Optional

- **Git:** For cloning the repository
- **Virtual environment:** Recommended for isolation

---

## 🚀 Quick Install (Recommended)

### 1. Clone Repository

```bash
git clone https://github.com/Architekt-future/veritas-protocol.git
cd veritas-protocol
```

### 2. Create Virtual Environment (Recommended)

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**Windows:**
```cmd
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify Installation

```bash
python cli.py --help
```

If you see the help message, installation is successful! ✅

---

## 🐳 Docker Installation (Alternative)

### Pull Image (Coming Soon)

```bash
docker pull architektfuture/veritas-protocol:latest
```

### Or Build Locally

```bash
cd veritas-protocol
docker build -t veritas-protocol .
docker run -p 5000:5000 veritas-protocol
```

---

## 📦 Manual Installation

### 1. Download ZIP

If you don't have Git:

1. Go to [GitHub Repository](https://github.com/Architekt-future/veritas-protocol)
2. Click "Code" → "Download ZIP"
3. Extract the archive
4. Open terminal in extracted folder

### 2. Install Python

**Check if Python is installed:**
```bash
python --version
# or
python3 --version
```

**If not installed:**

- **Linux (Ubuntu/Debian):**
  ```bash
  sudo apt update
  sudo apt install python3 python3-pip python3-venv
  ```

- **macOS:**
  ```bash
  brew install python3
  ```

- **Windows:**
  Download from [python.org](https://www.python.org/downloads/)

### 3. Install Dependencies Manually

```bash
pip install requests beautifulsoup4 lxml pandas numpy flask flask-cors pyyaml colorama rich
```

---

## 🧪 Test Your Installation

### Run Quick Test

```bash
# Test 1: Simple text analysis
python cli.py --text "If the data equals zero, then result indicates an error"

# Test 2: Check help
python cli.py --help

# Test 3: Run web interface
python web/app.py
# Open http://localhost:5000 in browser
```

### Expected Output (Test 1)

```
╔═══════════════════════════════════════════════════════════════╗
║           VERITAS PROTOCOL - АНАЛІЗ НОВИНИ                    ║
╚═══════════════════════════════════════════════════════════════╝

📰 ДЖЕРЕЛО: Manual_Input
🔍 Індекс ентропії: 0.125
📈 Репутація джерела: 0.55
🏷️  Статус: SUCCESS
💬 Вердикт: Високоякісний логічний сигнал
```

---

## ⚙️ Configuration

### Default Configuration

Veritas works out-of-the-box with default settings.

### Custom Configuration (Optional)

Create `config.yaml` in project root:

```yaml
veritas:
  thresholds:
    critical: 0.7
    warning: 0.4
    trusted: 0.2
  
  slashing:
    penalty_multiplier: 0.35
    reward_bonus: 0.05

web:
  host: "0.0.0.0"
  port: 5000

database:
  path: "veritas_analysis.db"
```

See [Configuration Guide](configuration.md) for full options.

---

## 🔧 Troubleshooting

### Common Issues

#### Issue: `ModuleNotFoundError`

**Solution:**
```bash
pip install -r requirements.txt
```

#### Issue: `Permission denied` on Linux/macOS

**Solution:**
```bash
chmod +x cli.py
# or
python3 cli.py --help
```

#### Issue: Port 5000 already in use

**Solution:**
Edit `config.yaml`:
```yaml
web:
  port: 8080  # Change to different port
```

Or run directly:
```bash
python web/app.py --port 8080
```

#### Issue: `sqlite3.OperationalError`

**Solution:**
```bash
# Delete old database
rm veritas_analysis.db
# Restart app - will create new database
python cli.py --help
```

---

## 🚀 Next Steps

After successful installation:

1. **Read the [Quick Start Guide](../README.md#quick-start)**
2. **Try example commands:**
   ```bash
   python cli.py --text "Your text here"
   python cli.py --url https://news-site.com/article
   ```
3. **Explore [Configuration Options](configuration.md)**
4. **Check out [API Reference](api.md)**

---

## 💻 Development Installation

For contributors and developers:

### 1. Install Development Dependencies

```bash
pip install -r requirements-dev.txt
```

### 2. Install Pre-commit Hooks

```bash
pre-commit install
```

### 3. Run Tests

```bash
pytest tests/
```

### 4. Run Linters

```bash
black .
flake8 .
mypy veritas_core.py
```

See [Contributing Guide](../CONTRIBUTING.md) for more details.

---

## 🌍 Platform-Specific Notes

### Linux

Works perfectly on Ubuntu 20.04+, Debian 11+, Fedora, Arch.

### macOS

Tested on macOS 11+ (Big Sur and newer).

**Note:** On Apple Silicon (M1/M2), use:
```bash
arch -arm64 python3 -m pip install -r requirements.txt
```

### Windows

Works on Windows 10/11.

**Note:** If you encounter encoding issues:
```bash
set PYTHONIOENCODING=utf-8
python cli.py --text "Your text"
```

---

## 📞 Need Help?

- 📖 **Documentation:** [docs/](.)
- 🐛 **Issues:** [GitHub Issues](https://github.com/Architekt-future/veritas-protocol/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/Architekt-future/veritas-protocol/discussions)

---

**Installation complete! Ready to detect manipulation! 🚀**
