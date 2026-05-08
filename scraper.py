import requests
import re

FIREBASE_URL = "https://alertrussiamap-default-rtdb.europe-west1.firebasedatabase.app/alerts.json"
# Мы меняем ссылку на экспортную, которую Google отдает как текст
SOURCE_URL = "https://docs.google.com/document/d/1vC1jKclmF8iXzG7Wsh5I_m60f9VvW_Z0vC5mF8mI_Q/export?format=txt"

def run():
    try:
        # Пытаемся забрать документ как чистый текст
        response = requests.get(SOURCE_URL, timeout=15)
        response.encoding = 'utf-8'
        content = response.text.lower()
        
        print(f"DEBUG: Получено текста: {len(content)} символов")
        # Выводим кусочек текста для проверки в логах
        print(f"DEBUG: Текст из дока: {content[:300]}")

        region_map = {
            "москов": "Moscow", "туль": "Tula", "липец": "Lipetsk", 
            "рязан": "Ryazan", "белгород": "Belgorod", "воронеж": "Voronezh", 
            "курск": "Kursk", "брянск": "Bryansk", "калуж": "Kaluga"
        }
        
        danger_words = ["зафиксирован", "опасность", "бпла", "тревога", "пво", "атака", "ракет", "обстрел", "внимание"]
        cancel_words = ["отбой", "отменена", "миновала"]

        new_statuses = {}

        for text_key, map_key in region_map.items():
            if text_key in content:
                # Ищем последнее упоминание
                pos = content.rfind(text_key)
                chunk = content[pos : pos+400]
                
                if any(dw in chunk for dw in danger_words):
                    new_statuses[map_key] = "danger"
                elif any(cw in chunk for cw in cancel_words):
                    new_statuses[map_key] = "safe"

        if new_statuses:
            requests.patch(FIREBASE_URL, json=new_statuses, timeout=15)
            print(f"✅ УСПЕХ! Обновлено в базе: {new_statuses}")
        else:
            print("ℹ️ Совпадений не найдено. Проверь текст в DEBUG выше.")

    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    run()
