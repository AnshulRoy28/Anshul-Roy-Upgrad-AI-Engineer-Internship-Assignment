#!/bin/bash

# AI Mock Interview Coach - Unified Server Launcher
# This script starts the Flask server that serves both API and frontend

echo "🚀 Starting AI Mock Interview Coach..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
if [ ! -f "venv/.installed" ]; then
    echo "📥 Installing dependencies..."
    pip install -r requirements.txt
    touch venv/.installed
fi

# Check for .env file
if [ ! -f ".env" ]; then
    echo "⚠️  No .env file found. Creating from .env.example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env
        echo "📝 Please edit .env and add your GOOGLE_API_KEY"
        exit 1
    fi
fi

# Start the unified server
echo "🌐 Starting unified server..."
python run_server.py

# Deactivate virtual environment on exit
deactivate
