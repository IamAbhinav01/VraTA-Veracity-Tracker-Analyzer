import sys
import os
sys.path.append(os.path.abspath("."))
import requests
from bs4 import BeautifulSoup
from app.rag_retriever import add_fact

def scrape_pib_factchecks():
    print("🔍 Scraping PIB fact-check press releases...")

    url = "https://pib.gov.in/AllRelease.aspx?MenuId=3"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0 Safari/537.36"
    }
    response = requests.get(url, headers=headers, timeout=10)

    if response.status_code != 200:
        print("❌ Failed to fetch PIB press releases.")
        return

    soup = BeautifulSoup(response.content, "html.parser")
    links = soup.select("a")  # Get all links

    count = 0
    for link in links:
        text = link.get_text(strip=True)
        if any(kw in text.lower() for kw in ["fake", "false", "fact", "misleading", "rumor", "claim"]):
            if len(text.split()) > 5:
                add_fact(text)
                print(f"✅ Embedded: {text}")
                count += 1

    print(f"\n🎯 Total embedded: {count} PIB fact-checks\n")

if __name__ == "__main__":
    scrape_pib_factchecks()
