import os
from dotenv import load_dotenv
from astrapy import DataAPIClient
from sentence_transformers import SentenceTransformer, util

# Load environment variables
load_dotenv("config/.env")

# 🔐 Env vars
ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_COLLECTION = os.getenv("ASTRA_DB_COLLECTION")

# ✅ Initialize client
client = DataAPIClient(ASTRA_DB_APPLICATION_TOKEN)
db = client.get_database_by_api_endpoint(ASTRA_DB_API_ENDPOINT)
if ASTRA_DB_COLLECTION not in db.list_collections():
    db.create_collection(ASTRA_DB_COLLECTION)
collection = db.get_collection(ASTRA_DB_COLLECTION)

# ✅ Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# 🔹 Create embedding
def embed_text(text: str) -> list:
    return model.encode(text).tolist()

# 🔹 Add fact to Astra DB
def add_fact(text: str, source="manual", url=None, date=None, category="general"):
    doc = {
        "text": text,
        "embedding": embed_text(text),
        "source": source,
        "url": url,
        "date": date,
        "category": category
    }
    collection.insert_one(doc)

# 🔹 Retrieve top-k relevant facts
def retrieve_facts(query: str, k: int = 3) -> list:
    query_vector = model.encode(query)
    documents = collection.find()

    scored_docs = []
    for doc in documents:
        if "embedding" in doc:
            try:
                score = util.cos_sim(query_vector, doc["embedding"])[0][0].item()
                scored_docs.append({
                    "score": score,
                    "text": doc["text"],
                    "url": doc.get("url", "URL not available"),
                    "source": doc.get("source", "Unknown"),
                    "date": doc.get("date", "Date not provided"),
                    "category": doc.get("category", "General")
                })
            except:
                continue

    top_docs = sorted(scored_docs, key=lambda x: x["score"], reverse=True)[:k]
    return top_docs