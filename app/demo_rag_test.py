import sys
import os
sys.path.append(os.path.abspath("."))
from app.rag_retriever import retrieve_facts

query = "Was NASA preparing for alien contact by hiring theologians?"

facts = retrieve_facts(query)
print("\n🔍 Retrieved Facts:\n")
print(facts)
