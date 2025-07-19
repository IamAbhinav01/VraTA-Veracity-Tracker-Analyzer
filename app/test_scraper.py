import sys
import os
sys.path.append(os.path.abspath("."))
from app.rag_retriever import retrieve_facts

query = "Did Joe Biden win the 2020 election?"
facts = retrieve_facts(query)

print("🔍 Top Matching Facts:\n")
print(facts)
