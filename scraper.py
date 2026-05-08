import requests

# Твои ссылки
FIREBASE_URL = "https://alertrussiamap-default-rtdb.europe-west1.firebasedatabase.app/alerts.json"
SOURCE_URL = "https://share.google/qGPdi7mz21mxRiEu3"

def run():
    try:
        response = requests.get(SOURCE_URL, timeout=15)
        content = response.text.lower()
        
        # Словарь: корень русского слова -> ключ в базе данных
        region_map = {
            "адыг": "Adygeya", "алтай": "Altay", "амурск": "Amur", "архангель": "Arkhangel'sk", "астрахан": "Astrakhan'",
            "башкорто": "Bashkortostan", "белгород": "Belgorod", "брянск": "Bryansk", "бурят": "Buryat", "чечен": "Chechnya",
            "челябин": "Chelyabinsk", "чук": "Chukot", "чуваш": "Chuvash", "даг": "Dagestan", "ингуш": "Ingush",
            "иркут": "Irkutsk", "иванов": "Ivanovo", "еврей": "Yevrey", "кабардин": "Kabardin-Balkar", "калинин": "Kaliningrad",
            "калмык": "Kalmyk", "калуж": "Kaluga", "камчат": "Kamchatka", "карача": "Karachay-Cherkess", "карел": "Karelia",
            "кемеров": "Kemerovo", "хабар": "Khabarovsk", "хакас": "Khakass", "ханты": "Khanty-Mansiy", "киров": "Kirov",
            "коми": "Komi", "костром": "Kostroma", "краснодар": "Krasnodar", "краснояр": "Krasnoyarsk", "курган": "Kurgan",
            "курск": "Kursk", "ленин": "Leningrad", "липецк": "Lipetsk", "магадан": "Magadan", "марий": "Mariiy-El",
            "мордов": "Mordovia", "москов": "Moscow", "мурман": "Murmansk", "ненец": "Nenets", "нижегород": "Nizhegorod",
            "осет": "North Ossetia", "новгород": "Novgorod", "новосибир": "Novosibirsk", "омск": "Omsk", "оренбург": "Orenburg",
            "орел": "Orel", "орлов": "Orel", "пенз": "Penza", "перм": "Perm'", "примор": "Primor'ye", "псков": "Pskov",
            "ростов": "Rostov", "рязан": "Ryazan", "саха": "Sakha", "сахалин": "Sakhalin", "самар": "Samara",
            "сарат": "Saratov", "смолен": "Smolensk", "ставро": "Stavropol'", "свердлов": "Sverdlovsk", "тамбов": "Tambov",
            "татар": "Tatarstan", "томск": "Tomsk", "туль": "Tula", "тыва": "Tuva", "твер": "Tver'",
            "тюмен": "Tyumen'", "удмурт": "Udmurt", "ульянов": "Ul'yanovsk", "владимир": "Vladimir", "волгоград": "Volgograd",
            "волог": "Vologda", "воронеж": "Voronezh", "ямало": "Yamal-Nenets", "ярослав": "Yaroslavl'", "забайка": "Zabaykal'ye",
            "крым": "Crimea", "севастополь": "Crimea"
        }
        
        danger_words = ["зафиксирован", "опасность", "бпла", "тревога", "пво", "атака", "ракет"]
        cancel_words = ["отбой", "отменена", "миновала", "нету угрозы"]

        new_statuses = {}

        for text_key, map_key in region_map.items():
            if text_key in content:
                pos = content.find(text_key)
                # Берем контекст вокруг слова
                chunk = content[max(0, pos-50) : pos+200]
                
                if any(cw in chunk for cw in cancel_words):
                    new_statuses[map_key] = "safe"
                elif any(dw in chunk for dw in danger_words):
                    new_statuses[map_key] = "danger"
                else:
                    new_statuses[map_key] = "safe"

        if new_statuses:
            # Обновляем Firebase (PATCH не стирает другие данные)
            requests.patch(FIREBASE_URL, json=new_statuses)
            print(f" Firebase updated: {new_statuses}")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    run()
