import requests

# ВАЖНО: Ссылка для записи (должна совпадать с базой)
FIREBASE_URL = "https://alertrussiamap-default-rtdb.europe-west1.firebasedatabase.app/alerts.json"

def run():
    try:
        # Тестовые данные для проверки связи
        test_data = {
            "Tula": "danger",
            "Crimea": "danger",
            "Moscow": "danger",
            "Belgorod": "danger",
            "Kursk": "danger"
        }
        
        print("Отправка данных в Firebase...")
        response = requests.patch(FIREBASE_URL, json=test_data, timeout=15)
        
        if response.status_code == 200:
            print(f"✅ УСПЕХ: Данные записаны! Статус: {response.status_code}")
            print(f"Ответ базы: {response.text}")
        else:
            print(f"❌ ОШИБКА: Код {response.status_code}, Ответ: {response.text}")

    except Exception as e:
        print(f"❌ ОШИБКА СКРИПТА: {e}")

if __name__ == "__main__":
    run()
