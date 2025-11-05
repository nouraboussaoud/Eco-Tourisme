# Installation script for Eco-Tourism Backend (PowerShell)
# Run this to install all dependencies properly

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║   ECO-TOURISM BACKEND - DEPENDENCY INSTALLATION           ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check Python version
try {
    $pythonVersion = python --version 2>&1
    Write-Host "✅ Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ ERROR: Python not found!" -ForegroundColor Red
    Write-Host "Install Python from: https://www.python.org/downloads/" -ForegroundColor Yellow
    Write-Host "Make sure to check 'Add Python to PATH'" -ForegroundColor Yellow
    Read-Host "Press Enter to exit"
    exit 1
}

Write-Host ""

# Create virtual environment if it doesn't exist
if (-not (Test-Path "venv")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Cyan
    python -m venv venv
    Write-Host "✅ Virtual environment created" -ForegroundColor Green
} else {
    Write-Host "✅ Virtual environment already exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "Activating virtual environment..." -ForegroundColor Cyan
& "venv\Scripts\Activate.ps1"
Write-Host "✅ Virtual environment activated" -ForegroundColor Green
Write-Host ""

# Upgrade pip
Write-Host "Upgrading pip..." -ForegroundColor Cyan
python -m pip install --upgrade pip
Write-Host "✅ Pip upgraded" -ForegroundColor Green
Write-Host ""

# Install requirements
Write-Host "Installing dependencies from requirements.txt..." -ForegroundColor Cyan
pip install -r requirements.txt

if ($LASTEXITCODE -ne 0) {
    Write-Host "⚠️  Some packages failed to install" -ForegroundColor Yellow
    Write-Host "Trying to install them individually..." -ForegroundColor Yellow
    Write-Host ""
    
    pip install "fastapi>=0.104.1"
    pip install "uvicorn>=0.24.0"
    pip install "pydantic>=2.5.0"
    pip install "python-dotenv>=1.0.0"
    pip install "requests>=2.31.0"
    pip install "google-generativeai>=0.3.0"
    pip install "python-multipart>=0.0.6"
    
    Write-Host "⚠️  Installation completed with some warnings" -ForegroundColor Yellow
    Write-Host "Try running: pip install spacy" -ForegroundColor Yellow
    Write-Host "             python -m spacy download en_core_web_sm" -ForegroundColor Yellow
} else {
    Write-Host "✅ All dependencies installed successfully" -ForegroundColor Green
}

Write-Host ""
Write-Host "╔════════════════════════════════════════════════════════════╗" -ForegroundColor Green
Write-Host "║   INSTALLATION COMPLETE                                    ║" -ForegroundColor Green
Write-Host "╚════════════════════════════════════════════════════════════╝" -ForegroundColor Green
Write-Host ""
Write-Host "You can now run: python main.py" -ForegroundColor Green
Write-Host ""
