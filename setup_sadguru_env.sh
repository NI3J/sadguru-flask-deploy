#!/bin/bash

echo "🧘 Starting Sadguru Transcription Environment Setup..."

# 🌈 Auto-heal interrupted dpkg session
if sudo fuser /var/lib/dpkg/lock &>/dev/null || \
   sudo fuser /var/lib/dpkg/lock-frontend &>/dev/null; then
    echo "⚠️ DPKG is locked or was interrupted. Healing..."
    sudo rm -f /var/lib/dpkg/lock-frontend /var/lib/dpkg/lock
    sudo dpkg --configure -a
fi

# 🛠️ Function to check and install APT packages
install_if_missing() {
    if ! dpkg -s "$1" &>/dev/null; then
        echo "🔧 Installing $1..."
        sudo apt-get install -y "$1"
    else
        echo "✅ $1 is already installed."
    fi
}

# 🔃 Update repo and install system dependencies
sudo apt-get update

DEPENDENCIES=(
    python3.10
    python3.10-venv
    python3-pip
    ffmpeg
    pandoc
    curl
    git
    texlive
    texlive-xetex
    texlive-fonts-recommended
    texlive-latex-extra
)

for dep in "${DEPENDENCIES[@]}"; do
    install_if_missing "$dep"
done

# 🌿 Create and activate virtual environment
if [ ! -d "venv" ]; then
    python3.10 -m venv venv
    echo "🆕 Virtual environment created."
fi

source venv/bin/activate
echo "🌱 Virtual environment activated."

# 📦 Install Python packages
REQUIRED_PKGS=(
    autopep8==2.3.2
    black==25.1.0
    blinker==1.9.0
    certifi==2025.7.14
    charset-normalizer==3.4.2
    click==8.2.1
    Flask==3.1.1
    Flask-Mail==0.10.0
    gunicorn==23.0.0
    idna==3.10
    itsdangerous==2.2.0
    Jinja2==3.1.6
    MarkupSafe==3.0.2
    mypy_extensions==1.1.0
    mysql-connector-python==9.3.0
    packaging==25.0
    pathspec==0.12.1
    platformdirs==4.3.8
    pycodestyle==2.14.0
    python-dotenv==1.1.1
    requests==2.32.4
    tomli==2.2.1
    typing_extensions==4.14.1
    urllib3==2.5.0
    Werkzeug==3.1.3
    python-decouple
)

for pkg in "${REQUIRED_PKGS[@]}"; do
    pkg_name=$(echo "$pkg" | cut -d'=' -f1)
    if ! pip show "$pkg_name" &>/dev/null; then
        echo "📦 Installing $pkg..."
        pip install "$pkg"
    else
        echo "✅ $pkg_name already installed."
    fi
done

echo "🎉 Environment ready. You can now run your Sadguru app with: python3.10 app.py"
