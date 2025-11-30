@echo off
echo Установка зависимостей...
pip install -r requirements.txt

echo.
echo Запуск скачивания модели Llama 3 8B q4_k_m...
python download_llama.py

echo.
pause
