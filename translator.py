import requests
import time

def translate_titles(titles, api_key):
    url = "https://rapid-translate-multi-traduction.p.rapidapi.com/t"
    headers = {
        "x-rapidapi-key": api_key,
        "x-rapidapi-host": "rapid-translate-multi-traduction.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    translated = []
    for idx, title in enumerate(titles):
        payload = {
            "from": "es",
            "to": "en",
            "q": title
        }
        try:
            r = requests.post(url, headers=headers, json=payload, timeout=10)
            data = r.json()
            translated.append(data[0] if isinstance(data, list) else "[Translation failed]")
        except Exception as e:
            print(f"⚠️ Translation {idx+1} failed: {e}")
            translated.append("[Translation failed]")
        time.sleep(1.5)
    return translated
