import sys
import os
sys.path.append(os.path.abspath("."))
from newspaper import Article, build
from app.rag_retriever import add_fact
import time

def scrape_and_embed_articles(source_url, max_articles=5):
    print(f"🔍 Scraping from: {source_url}")
    paper = build(source_url, memoize_articles=False)

    count = 0
    for article in paper.articles:
        if count >= max_articles:
            break
        try:
            article.download()
            article.parse()

            content = article.title.strip() + "\n\n" + article.text.strip()
            if len(content.split()) > 50:  # Only if it's a meaningful article
                add_fact(content)
                print(f"✅ Embedded: {article.title}")
                count += 1
                time.sleep(1)
        except Exception as e:
            print(f"⚠️ Skipped: {e}")
            continue

    print(f"\n🎯 Total embedded: {count} from {source_url}")

if __name__ == "__main__":
    sources = [
        "https://edition.cnn.com",
        "https://www.reuters.com/news/archive/factCheck"
    ]

    for src in sources:
        scrape_and_embed_articles(src, max_articles=3)
