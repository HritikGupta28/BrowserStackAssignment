import time
import requests
import re
import os
from urllib.parse import urljoin
from collections import Counter
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

# === CONFIG ===
CHROME_PATH = r"D:\BrowserStackAssignment\webDrivers\chromedriver.exe"
ARTICLE_LIMIT = 5
API_KEY = "d24cf57d56mshff1f306c61c7af2p122afcjsnfe84202b3db3"
TRANSLATE_URL = "https://rapid-translate-multi-traduction.p.rapidapi.com/t"

# === INIT SELENIUM ===
service = Service(CHROME_PATH)
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

# === STEP 1: Accept Cookie Notice ===
driver.get("https://elpais.com/")
time.sleep(2)
try:
    cookie = driver.find_element(By.XPATH, '//*[@id="didomi-notice-agree-button"]/span')
    cookie.click()
    print("✅ Cookie accepted.")
except:
    print("ℹ️ Cookie consent not shown.")

# === STEP 2: Navigate to Opinion Section ===
driver.get("https://elpais.com/opinion/")
time.sleep(2)
soup = BeautifulSoup(driver.page_source, "html.parser")
articles = soup.select("article")[:ARTICLE_LIMIT]

# === STEP 3: Collect Article URLs and Titles ===
article_list = []
for article in articles:
    title_tag = article.find("h2")
    link_tag = article.find("a")
    if title_tag and link_tag:
        title = title_tag.text.strip()
        href = link_tag.get("href", "#")
        url = href if href.startswith("http") else f"https://elpais.com{href}"
        article_list.append({"title": title, "url": url})

# === STEP 4: Scrape Article Content & Cover Image ===
scraped = []
os.makedirs("images", exist_ok=True)

for idx, article in enumerate(article_list):
    driver.get(article["url"])
    time.sleep(2)
    detail_soup = BeautifulSoup(driver.page_source, "html.parser")

    paragraphs = detail_soup.select("p")
    content = "\n".join(p.text for p in paragraphs[:5]) if paragraphs else "[No content]"

    img_tag = detail_soup.select_one("figure img[src^='https']")
    img_url = urljoin(article["url"], img_tag["src"]) if img_tag else None

    safe_title = re.sub(r"[^\w\s-]", "", article["title"]).strip().replace(" ", "_")
    img_path = "[No image found]"

    if img_url and img_url.startswith("http"):
        img_path = os.path.join("images", f"{safe_title}.jpg")
        try:
            img_data = requests.get(img_url).content
            with open(img_path, "wb") as f:
                f.write(img_data)
        except:
            img_path = "[Image download failed]"

    scraped.append({
        "title": article["title"],
        "content": content,
        "img": img_path
    })
    print(f"✅ Scraped article {idx+1}: {article['title']}")

driver.quit()

# === STEP 5: Translate Titles via Rapid Translate API ===
def translate_titles(titles, api_key):
    translated = []
    url = "https://rapid-translate-multi-traduction.p.rapidapi.com/t"

    headers = {
        "x-rapidapi-key": "d24cf57d56mshff1f306c61c7af2p122afcjsnfe84202b3db3",
        "x-rapidapi-host": "rapid-translate-multi-traduction.p.rapidapi.com",
        "Content-Type": "application/json"
    }

    for idx, title in enumerate(titles):
        payload = {
            "from": "es",
            "to": "en",
            "q": title
        }

        try:
            response = requests.post(url, headers=headers, json=payload, timeout=10)
            data = response.json()
            if isinstance(data, list) and len(data) > 0:
                translated.append(data[0])
            else:
                translated.append("[Translation failed]")
        except Exception as e:
            print(f"⚠️ Translation error ({idx+1}): {e}")
            translated.append("[Translation failed]")

        time.sleep(1.5)  # Respect rate limits
    return translated
spanish_titles = [item["title"] for item in scraped]
translated_titles = translate_titles(spanish_titles, API_KEY)

# === STEP 6: Display Results ===
print("\n🗞 Spanish Titles:")
for title in spanish_titles:
    print(f"- {title}")

print("\n🌍 Translated Titles:")
for title in translated_titles:
    print(f"- {title}")

print("\n🖼️ Saved Images:")
for item in scraped:
    print(f"- {item['img']}")

# === STEP 7: Repeated Word Analysis ===
tokens = []
for title in translated_titles:
    tokens += re.findall(r"\b\w+\b", title.lower())

counts = Counter(tokens)
repeats = {word: count for word, count in counts.items() if count > 2}

print("\n🔁 Repeated Words in Translated Titles:")
for word, count in repeats.items():
    print(f"{word}: {count}")
