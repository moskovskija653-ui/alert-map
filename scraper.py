import requests

FIREBASE_URL = "https://alertrussiamap-default-rtdb.europe-west1.firebasedatabase.app/alerts.json"
SOURCE_URL = "https://share.google/qGPdi7mz21mxRiEu3"

def run():
    try:
        response = requests.get(SOURCE_URL, timeout=15)
        content = response.text.lower()
        
        region_map = {
            "москов": "Moscow", "туль": "Tula", "липец": "Lipetsk", 
            "рязан": "Ryazan", "белгород": "Belgorod", "воронеж": "Voronezh", 
            "курск": "Kursk", "брянск": "Bryansk", "калуж": "Kaluga",
            "краснодар": "Krasnodar", "ростов": "Rostov", "крым": "Crimea"
        }
        
        danger_words = ["зафиксирован", "опасность", "бпла", "тревога", "пво", "атака", "ракет", "обстрел", "внимание", "сирена"]
        cancel_words = ["отбой", "отменена", "миновала", "спокойно"]

        new_statuses = {}

        for text_key, map_key in region_map.items():
            if text_key in content:
                # Ищем ПОСЛЕДНЕЕ (самое свежее) упоминание региона в тексте
                pos = content.rfind(text_key) 
                chunk = content[pos : pos+300]
                
                has_danger = any(dw in chunk for dw in danger_words)
                has_cancel = any(cw in chunk for cw in cancel_words)

                if has_danger and not has_cancel:
                    new_statuses[map_key] = "danger"
                elif has_cancel:
                    new_statuses[map_key] = "safe"

        if new_statuses:
            requests.patch(FIREBASE_URL, json=new_statuses, timeout=15)
            print(f"✅ Обновлено в Firebase: {new_statuses}")
        else:
            print("ℹ️ Активных угроз в свежих сообщениях не найдено.")

    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    run()
