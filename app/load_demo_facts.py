import sys
import os
sys.path.append(os.path.abspath("."))
from app.rag_retriever import add_fact

demo_facts = [
    "NASA did not hire 24 theologians to prepare for alien contact.",
    "Joe Biden won the US 2020 election, not Donald Trump.",
    "The Indian government did not impose a six-month nationwide internet ban.",
    "Fake news spreads faster during election seasons in India.",
    "PIB is the government agency for verifying official fake news in India."
]

for fact in demo_facts:
    add_fact(fact)

print("✅ Demo facts embedded successfully.")

