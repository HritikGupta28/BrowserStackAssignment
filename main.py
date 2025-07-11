from scraper import scrape_articles
from translator import translate_titles
from analyzer import find_repeated_words
from dotenv import load_dotenv
import os

load_dotenv()
API_KEY = os.getenv("RAPIDAPI_KEY")
CHROME_PATH = os.getenv("CHROME_PATH", "chromedriver.exe")

articles = scrape_articles(CHROME_PATH)
titles_es = [item["title"] for item in articles]
titles_en = translate_titles(titles_es, API_KEY)
repeats = find_repeated_words(titles_en)

print("\n🗞 Spanish Titles:")
print("\n".join(f"- {t}" for t in titles_es))

print("\n🌍 Translated Titles:")
print("\n".join(f"- {t}" for t in titles_en))

print("\n🖼️ Image Paths:")
print("\n".join(f"- {item['img']}" for item in articles))

print("\n🔁 Repeated Words:")
for word, count in repeats.items():
    print(f"{word}: {count}")
