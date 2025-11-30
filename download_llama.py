#!/usr/bin/env python3
"""
Скрипт для скачивания модели Llama 3 8B (q4_k_m)
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from huggingface_hub import hf_hub_download, login, HfApi

def authenticate_huggingface():

    load_dotenv()
    print("gg",load_dotenv())
    # Сначала пробуем токен (рекомендуемый способ)
    token = os.getenv('HF_TOKEN') or os.getenv('HUGGINGFACE_TOKEN')
    if token:
        print("Токен найден")
    if token:

        try:
            login(token)
            print("Тоен прошел успешно")
            return True
        except Exception as e:
            print(f"Токен не смог: {e}")

    username = os.getenv('HF_USERNAME') or os.getenv('HUGGINGFACE_USERNAME')
    password = os.getenv('HF_PASSWORD') or os.getenv('HUGGINGFACE_PASSWORD')

    if username and password:
        try:
            api = HfApi()
            api.login(username=username, password=password)
            print("Успешная аутентификация по логину/паролю!")
            return True
        except Exception as e:
            print(f" Ошибка  по логину/паролю: {e}")
            return False
    else:
        return False
#https://huggingface.co/TheBloke/LLaMA-Pro-8B-Instruct-GGUF
def download_llama_model():

    models_dir = Path("neural_networks")
    models_dir.mkdir(exist_ok=True)

    print("Создаю папку neural_networks..." )
    print(f"Папка создана: {models_dir.absolute()}")

    repo_id = "TheBloke/LLaMA-Pro-8B-Instruct-GGUF"
    filename = "llama-pro-8b-instruct.Q4_K_M.gguf"

    print(f"Начинаю скачивание модели {filename} из {repo_id}...")

    authenticate_huggingface()

    try:
        model_path = hf_hub_download(
            repo_id=repo_id,
            filename=filename,
            local_dir=models_dir,
            local_dir_use_symlinks=False
        )


        print(f"Нейронка сохранена в: {model_path}")

        # Проверяем размер файла
        file_size = os.path.getsize(model_path) / (1024 * 1024 * 1024)  # GB
        print(".2f")
        return model_path

    except Exception as e:
        print(f" Ошибка при скачивании: {e}")
        return None

if __name__ == "__main__":
    print("Start")
    result = download_llama_model()
    if result:
        print("ура")
    else: print("не ура")

