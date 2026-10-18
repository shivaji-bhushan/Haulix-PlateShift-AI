@echo off
title PlateShift Live Server Launcher
echo ========================================================
echo   Starting Haulix PlateShift AI Operations Dashboard
echo ========================================================

REM Start Flask in background
start "PlateShift Flask Engine" cmd /k "venv\Scripts\python app.py"

REM Wait 3 seconds for Flask to bind port 5000
timeout /t 3 /nobreak >nul

REM Start Cloudflare Tunnel
echo Starting Public Cloudflare HTTPS Tunnel...
cloudflared.exe tunnel --protocol http2 --url http://127.0.0.1:5000
pause
