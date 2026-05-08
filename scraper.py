import requests

FIREBASE_URL = "https://alertrussiamap-default-rtdb.europe-west1.firebasedatabase.app/alerts.json"
SOURCE_URL = "https://share.google/qGPdi7mz21mxRiEu3"

def run():
    try:
        response = requests.get(SOURCE_URL, timeout=15)
        content = response.text.lower()
        
        # Основные регионы и их ключи (добавь сюда те, что чаще всего в сводках)
        region_map = {
            "тульск": "Tula",
            "рязанск": "Ryazan",
            "крым": "Crimea",
            "севастополь": "Crimea",
            "белгород": "Belgorod",
            "воронеж": "Voronezh",
            "курск": "Kursk",
            "брянск": "Bryansk",
            "ростов": "Rostov",
            "краснодар": "Krasnodar",
            "липецк": "Lipetsk",
            "калуж": "Kaluga",
            "московск": "Moscow"
        }
        
        danger_words = ["опасность", "бпла", "тревога", "ракет", "атака"]
        cancel_words = ["отбой", "миновала", "отменена", "нету угрозы"]

        new_statuses = {}

        # Проверяем каждый регион из списка
        for text_key, map_key in region_map.items():
            if text_key in content:
                # Берем кусок текста вокруг упоминания региона (150 символов), чтобы найти "отбой"
                start_idx = content.find(text_key)
                context = content[start_idx : start_idx + 150]
                
                if any(cw in context for cw in cancel_words):
                    new_statuses[map_key] = "safe"
                elif any(dw in context for dw in danger_words):
                    new_statuses[map_key] = "danger"
                else:
                    new_statuses[map_key] = "safe"

        if new_statuses:
            requests.patch(FIREBASE_URL, json=new_statuses)
            print(f"Обновлено в Firebase: {new_statuses}")

    except Exception as e:
        print(f"Ошибка парсера: {e}")

if __name__ == "__main__":
    run()
