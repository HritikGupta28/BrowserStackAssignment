import os
import json

from dotenv import load_dotenv
from selenium import webdriver

from scraper import scrape_articles
from translator import translate_titles
from analyzer import find_repeated_words

# ─── Load env and BrowserStack config ────────────────────────────────
load_dotenv()
API_KEY       = os.getenv("RAPIDAPI_KEY")
BS_USERNAME   = os.getenv("BROWSERSTACK_USERNAME")
BS_ACCESS_KEY = os.getenv("BROWSERSTACK_ACCESS_KEY")
BS_REMOTE_URL = f"https://{BS_USERNAME}:{BS_ACCESS_KEY}@hub-cloud.browserstack.com/wd/hub"

# ─── BrowserStack executor helpers ─────────────────────────────────
def bs_name(driver, name):
    driver.execute_script(
        "browserstack_executor: " +
        json.dumps({"action": "setSessionName", "arguments": {"name": name}})
    )

def bs_status(driver, status, reason=""):
    driver.execute_script(
        "browserstack_executor: " +
        json.dumps({"action": "setSessionStatus", "arguments": {"status": status, "reason": reason}})
    )

def main():
    opts   = webdriver.ChromeOptions()
    driver = webdriver.Remote(command_executor=BS_REMOTE_URL, options=opts)
    bs_name(driver, "El País Opinion Test")

    try:
        # SCRAPE
        scraped = scrape_articles(driver)
        if not scraped:
            raise AssertionError("No articles scraped")

        # Print Spanish title + content
        print("\n🗞 Spanish Articles:")
        for art in scraped:
            print(f"Title: {art['title']}")
            print(f"Content: {art['content']}\n")

        # TRANSLATE
        titles_es = [a["title"] for a in scraped]
        titles_en = translate_titles(titles_es, API_KEY)
        if len(titles_en) != len(titles_es) or any("[Translation failed]" in t for t in titles_en):
            raise AssertionError("Translation failure detected")

        # ANALYZE
        repeats = find_repeated_words(titles_en)

        # Print English titles
        print("🌍 Translated Titles:")
        for t in titles_en:
            print(f"- {t}")

        # Print image paths
        print("\n🖼 Image Paths:")
        for a in scraped:
            print(f"- {a['img']}")

        # Print repeated words
        print("\n🔁 Repeated Words:")
        for w, c in repeats.items():
            print(f"{w}: {c}")

        bs_status(driver, "passed", "All steps succeeded")

    except AssertionError as ae:
        msg = f"CHECKPOINT FAILED: {ae}"
        print(msg)
        bs_status(driver, "failed", msg)

    except Exception as e:
        msg = f"ERROR: {e}"
        print(msg)
        bs_status(driver, "failed", msg)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()
