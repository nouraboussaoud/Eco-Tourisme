@echo off
REM Installation script for Eco-Tourism Backend
REM Run this to install all dependencies properly

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║   ECO-TOURISM BACKEND - DEPENDENCY INSTALLATION           ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

REM Check Python version
python --version
if errorlevel 1 (
    echo ❌ ERROR: Python not found!
    echo Install Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH"
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo ✅ Virtual environment created
) else (
    echo ✅ Virtual environment already exists
)

echo.
echo Activating virtual environment...
call venv\Scripts\activate.bat

echo ✅ Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip
echo ✅ Pip upgraded
echo.

REM Install requirements
echo Installing dependencies from requirements.txt...
pip install -r requirements.txt

if errorlevel 1 (
    echo ⚠️  Some packages failed to install
    echo Trying to install them individually...
    echo.
    
    pip install fastapi>=0.104.1
    pip install uvicorn>=0.24.0
    pip install pydantic>=2.5.0
    pip install python-dotenv>=1.0.0
    pip install requests>=2.31.0
    pip install google-generativeai>=0.3.0
    pip install python-multipart>=0.0.6
    
    echo ⚠️  Some packages may have failed
    echo Try: pip install spacy
    echo      python -m spacy download en_core_web_sm
) else (
    echo ✅ All dependencies installed successfully
)

echo.
echo ╔════════════════════════════════════════════════════════════╗
echo ║   INSTALLATION COMPLETE                                    ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo You can now run: python main.py
echo.
pause
