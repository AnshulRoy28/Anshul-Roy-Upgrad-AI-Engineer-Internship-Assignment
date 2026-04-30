@echo off
REM AI Mock Interview Coach - Unified Server Launcher
REM This script starts the Flask server that serves both API and frontend

echo 🚀 Starting AI Mock Interview Coach...

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed. Please install Python 3.8 or higher.
    pause
    exit /b 1
)

REM Check if virtual environment exists
if not exist "venv\" (
    echo 📦 Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
echo 🔧 Activating virtual environment...
call venv\Scripts\activate.bat

REM Install dependencies
if not exist "venv\.installed" (
    echo 📥 Installing dependencies...
    pip install -r requirements.txt
    echo. > venv\.installed
)

REM Check for .env file
if not exist ".env" (
    echo ⚠️  No .env file found. Creating from .env.example...
    if exist ".env.example" (
        copy .env.example .env
        echo 📝 Please edit .env and add your GOOGLE_API_KEY
        pause
        exit /b 1
    )
)

REM Start the unified server
echo 🌐 Starting unified server...
python run_server.py

REM Deactivate virtual environment on exit
call venv\Scripts\deactivate.bat
