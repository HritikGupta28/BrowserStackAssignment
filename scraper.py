import time
import re
import os
import requests

from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_articles(driver, limit=5):
    """
    Scrape top `limit` Opinion articles from El País:
      - Accept cookie banner
      - Visit Opinion section
      - Capture title, first 5 paragraphs, cover image
    Returns list of dicts:
      [ { "title": str, "content": str, "img": str }, ... ]
    """
    driver.maximize_window()
    driver.get("https://elpais.com/")
    time.sleep(2)

    # Accept cookie banner if present
    try:
        driver.find_element(
            By.XPATH, '//*[@id="didomi-notice-agree-button"]/span'
        ).click()
    except:
        pass

    driver.get("https://elpais.com/opinion/")
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    cards = soup.select("article")[:limit]

    os.makedirs("images", exist_ok=True)
    data = []

    for card in cards:
        title_tag = card.find("h2")
        link_tag  = card.find("a")
        if not title_tag or not link_tag:
            continue

        title = title_tag.text.strip()
        href  = link_tag["href"]
        url   = href if href.startswith("http") else f"https://elpais.com{href}"

        # Visit the article page
        driver.get(url)
        time.sleep(2)
        detail = BeautifulSoup(driver.page_source, "html.parser")

        # Extract first 5 paragraphs
        paras   = detail.select("p")
        content = "\n".join(p.text for p in paras[:5]) if paras else "[No content]"

        # Extract cover image (not logo)
        img_tag = detail.select_one("figure img[src^='https']")
        img_url = urljoin(url, img_tag["src"]) if img_tag else None

        # Build safe filename
        safe_name = re.sub(r"[^\w\s-]", "", title).strip().replace(" ", "_")
        img_path  = "[No image found]"

        if img_url:
            img_path = os.path.join("images", f"{safe_name}.jpg")
            try:
                response = requests.get(img_url, timeout=10)
                response.raise_for_status()
                with open(img_path, "wb") as f:
                    f.write(response.content)
            except Exception:
                img_path = "[Image download failed]"

        data.append({
            "title":   title,
            "content": content,
            "img":     img_path
        })

    return data
