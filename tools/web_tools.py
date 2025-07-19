# tools/web_tools.py

import feedparser
import logging
from langchain.tools import DuckDuckGoSearchRun, YahooFinanceNewsTool

async def tell_news(context, query):
    url = f"https://news.google.com/rss/search?q={query.replace(' ', '+')}"
    feed = feedparser.parse(url)
    if not feed.entries:
        return f"No news found for '{query}'."
    return "\n\n".join([f"{i+1}. {entry.title}\n{entry.link}" for i, entry in enumerate(feed.entries[:3])])

async def search(context, query):
    try:
        return DuckDuckGoSearchRun().run(tool_input=query)
    except Exception as e:
        logging.error(f"Search error: {e}")
        return f"No search result for {query}."

async def get_news(context, query):
    try:
        return YahooFinanceNewsTool().run(tool_input=query)
    except Exception as e:
        logging.error(f"Finance error: {e}")
        return f"No finance news for {query}."
