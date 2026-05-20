#!/bin/bash
echo "======================================"
echo "  AkreditasiRS Pro v3.0 - Starting..."
echo "======================================"
cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
  echo "[INFO] Membuat virtual environment..."
  python3 -m venv venv
fi

source venv/bin/activate
pip install -r requirements.txt -q

echo "[INFO] Aplikasi berjalan di http://localhost:8000"
echo "[INFO] Login: admin / Admin123!"
echo "[INFO] Tekan Ctrl+C untuk menghentikan."
python app.py
