@echo off
title Akreditasi RS
color 0A
echo.
echo  ==========================================
echo   Akreditasi RS --  Starting...
echo  ==========================================
echo.

cd /d "%~dp0"

REM Check Python
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python tidak ditemukan. Install Python 3.10+ terlebih dahulu.
    pause
    exit /b 1
)

REM Create venv if missing
if not exist "venv\Scripts\activate.bat" (
    echo [INFO] Membuat virtual environment...
    python -m venv venv
)

REM Activate
call venv\Scripts\activate.bat

REM Install deps
echo [INFO] Memeriksa dependensi...
pip install -r requirements.txt -q

REM Init DB and start
echo [INFO] Menginisialisasi database...
echo [INFO] Aplikasi berjalan di http://localhost:8000
echo [INFO] Login: admin / Admin123!
echo [INFO] Tekan Ctrl+C untuk menghentikan.
echo.

python app.py

pause
