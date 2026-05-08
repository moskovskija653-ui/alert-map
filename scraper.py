import requests

# Твой URL (проверь, чтобы в конце был /alerts.json)
FIREBASE_URL = "https://alertrussiamap-default-rtdb.europe-west1.firebasedatabase.app/alerts.json"

def run():
    try:
        # ПРИНУДИТЕЛЬНЫЙ ТЕСТ: Красим эти регионы прямо сейчас
        test_data = {
            "Tula": "danger",
            "Crimea": "danger",
            "Moscow": "danger",
            "Belgorod": "danger",
            "Kursk": "danger"
        }
        
        # Отправляем в базу
        response = requests.patch(FIREBASE_URL, json=test_data)
        
        if response.status_code == 200:
            print(f"✅ ТЕСТ УСПЕШЕН: Данные в Firebase обновлены!")
            print(f"Отправлено: {test_data}")
        else:
            print(f"❌ ОШИБКА FIREBASE: Код {response.status_code}")
            print(f"Ответ сервера: {response.text}")

    except Exception as e:
        print(f"❌ КРИТИЧЕСКАЯ ОШИБКА: {e}")

if __name__ == "__main__":
    run()
