import time, re, os, requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_articles(chrome_path, limit=5):
    driver = webdriver.Chrome(service=Service(chrome_path))
    driver.maximize_window()

    driver.get("https://elpais.com/")
    time.sleep(2)
    try:
        driver.find_element(By.XPATH, '//*[@id="didomi-notice-agree-button"]/span').click()
    except: pass

    driver.get("https://elpais.com/opinion/")
    time.sleep(2)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    articles = soup.select("article")[:limit]

    results = []
    os.makedirs("images", exist_ok=True)

    for article in articles:
        title_tag = article.find("h2")
        link_tag = article.find("a")
        if not title_tag or not link_tag:
            continue

        title = title_tag.text.strip()
        href = link_tag.get("href", "#")
        url = href if href.startswith("http") else f"https://elpais.com{href}"

        driver.get(url)
        time.sleep(2)
        detail = BeautifulSoup(driver.page_source, "html.parser")
        paras = detail.select("p")
        content = "\n".join(p.text for p in paras[:5]) if paras else "[No content]"

        img_tag = detail.select_one("figure img[src^='https']")
        img_url = urljoin(url, img_tag["src"]) if img_tag else None
        safe_name = re.sub(r"[^\w\s-]", "", title).strip().replace(" ", "_")
        img_path = "[No image found]"

        if img_url:
            img_path = f"images/{safe_name}.jpg"
            try:
                with open(img_path, "wb") as f:
                    f.write(requests.get(img_url).content)
            except:
                img_path = "[Image failed]"

        results.append({"title": title, "content": content, "img": img_path})

    driver.quit()
    return results
