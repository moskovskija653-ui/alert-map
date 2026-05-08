import requests

# Твоя правильная ссылка
FIREBASE_URL = "https://alertrussiamap-default-rtdb.europe-west1.firebasedatabase.app/alerts.json"
SOURCE_URL = "https://share.google/qGPdi7mz21mxRiEu3"

def run():
    try:
        response = requests.get(SOURCE_URL, timeout=15)
        content = response.text.lower()
        
        region_map = {
            "туль": "Tula", "рязан": "Ryazan", "москов": "Moscow", "краснодар": "Krasnodar", "ростов": "Rostov",
            "крым": "Crimea", "севастополь": "Crimea", "белгород": "Belgorod", "воронеж": "Voronezh", "курск": "Kursk",
            "брянск": "Bryansk", "адыг": "Adygeya", "алтай": "Altay", "амурск": "Amur", "архангель": "Arkhangel'sk", 
            "астрахан": "Astrakhan'", "башкорто": "Bashkortostan", "бурят": "Buryat", "чечен": "Chechnya",
            "челябин": "Chelyabinsk", "даг": "Dagestan", "ингуш": "Ingush", "иркут": "Irkutsk", "иванов": "Ivanovo",
            "калин": "Kaliningrad", "калуж": "Kaluga", "карел": "Karelia", "кемеров": "Kemerovo", "хабар": "Khabarovsk",
            "киров": "Kirov", "коми": "Komi", "костром": "Kostroma", "краснояр": "Krasnoyarsk", "курган": "Kurgan",
            "ленин": "Leningrad", "липецк": "Lipetsk", "магадан": "Magadan", "мордов": "Mordovia", "мурман": "Murmansk",
            "нижегород": "Nizhegorod", "новгород": "Novgorod", "новосибир": "Novosibirsk", "омск": "Omsk", "оренбург": "Orenburg",
            "орел": "Orel", "пенз": "Penza", "перм": "Perm'", "примор": "Primor'ye", "псков": "Pskov", "самар": "Samara",
            "сарат": "Saratov", "смолен": "Smolensk", "ставро": "Stavropol'", "свердлов": "Sverdlovsk", "тамбов": "Tambov",
            "татар": "Tatarstan", "томск": "Tomsk", "твер": "Tver'", "тюмен": "Tyumen'", "удмурт": "Udmurt", 
            "ульянов": "Ul'yanovsk", "владимир": "Vladimir", "волгоград": "Volgograd", "волог": "Vologda", "ярослав": "Yaroslavl'"
        }
        
        danger_words = ["зафиксирован", "опасность", "бпла", "тревога", "пво", "атака", "ракет"]
        cancel_words = ["отбой", "отменена", "миновала"]

        new_statuses = {}

        for text_key, map_key in region_map.items():
            if text_key in content:
                pos = content.find(text_key)
                chunk = content[max(0, pos-50) : pos+200]
                
                if any(cw in chunk for cw in cancel_words):
                    new_statuses[map_key] = "safe"
                elif any(dw in chunk for dw in danger_words):
                    new_statuses[map_key] = "danger"

        if new_statuses:
            requests.patch(FIREBASE_URL, json=new_statuses, timeout=15)
            print(f"✅ Firebase updated: {new_statuses}")
        else:
            print("ℹ️ No alerts found in source.")

    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    run()
