import sys
import os
sys.path.append(os.path.abspath("."))
from app.rag_retriever import add_fact

facts = [
    {
        "text": "The US 2020 election was won by Joe Biden against Donald Trump.",
        "source": "CNN",
        "url": "https://cnn.com/article1",
        "date": "2020-11-04",
        "category": "politics"
    },
    {
        "text": "NASA did not hire 24 theologians to prepare for alien contact.",
        "source": "Reuters",
        "url": "https://reuters.com/fact-check-nasa",
        "date": "2022-03-14",
        "category": "science"
    }
]

for fact in facts:
    add_fact(**fact)

print("✅ Metadata-based facts inserted successfully.")
