@echo off
echo Starting AI Mock Interview Coach...
start "API Server" cmd /k "venv\Scripts\activate.bat && python api_server.py"
timeout /t 3 /nobreak >nul
cd Frontend
start "Frontend" cmd /k "python -m http.server 5500"
