import requests
import json

# Твой URL из скрипта (обязательно с .json на конце)
FIREBASE_URL = "https://alertrussiamap-default-rtdb.europe-west1.firebasedatabase.app/alerts.json"
# Ссылка на мониторинг
SOURCE_URL = "https://share.google/qGPdi7mz21mxRiEu3"

def run():
    try:
        # 1. Проверяем источник
        response = requests.get(SOURCE_URL, timeout=15)
        content = response.text.lower()

        # 2. Формируем данные для Firebase
        # Можно добавить логику для других регионов здесь
        new_status = {
            "Crimea": "danger" if "крым" in content and ("бпла" in content or "тревога" in content) else "safe",
            "Mos": "safe",
            "Belgorod": "safe"
        }

        # 3. Отправляем в Firebase через PATCH (чтобы обновить только эти поля)
        res = requests.patch(FIREBASE_URL, json=new_status)
        
        if res.status_code == 200:
            print("Firebase успешно обновлен!")
        else:
            print(f"Ошибка Firebase: {res.status_code}")

    except Exception as e:
        print(f"Ошибка скрипта: {e}")

if __name__ == "__main__":
    run()
