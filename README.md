# 📰 El País Opinion Scraper

A modular Python automation tool that scrapes and analyzes the latest *Opinion* articles from [El País](https://elpais.com/opinion/). It extracts Spanish titles, content, and cover images, translates headlines to English via RapidAPI, and highlights repeated keywords—perfect for content QA and internationalization tasks.

---

## 🚀 Features

- ✅ Scrapes top 5 opinion articles using Selenium
- 🖼️ Downloads actual article cover images (excludes logos/icons)
- 🌐 Translates Spanish titles to English via Rapid Translate Multi Traduction API
- 🔁 Identifies frequently repeated words in translated headlines
- 🔒 Secured with `.env` for API keys and driver paths

## 🛠️ Setup Instructions

1. Clone the Repository
git clone https://github.com/HritikGupta28/BrowserStackAssignment.git
cd BrowserStackAssignment

2. Install Dependencies
bash
pip install -r requirements.txt

3. Create Your .env File
RAPIDAPI_KEY=your-rapidapi-key-here
CHROME_PATH=full/path/to/chromedriver.exe
✅ Important: Do NOT commit .env to Git. It contains sensitive keys.

4. Run the Script
bash
python main.py

📥 Output
  🖼 Cover images saved in images/
  🗞 Spanish and English article titles printed to the console
  🔁 Repeated keywords highlighted for analysis

🔐 Security Best Practices
  API keys and driver paths are loaded from a .env file using python-dotenv
  .env, images/, and temporary files are ignored via .gitignore
  No personal credentials or scraped media are committed to version control

🧪 Requirements
  Python 3.8+
  ChromeDriver (matching your local Chrome browser)
  Python packages:


🙋‍♂️ Contributions Welcome
This project is modular and extensible. You’re welcome to fork or open pull requests for:
Translating article body content
Exporting scraped data to JSON or CSV
Scraping other El País sections or domains
