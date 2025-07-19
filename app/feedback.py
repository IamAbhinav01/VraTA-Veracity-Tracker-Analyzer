from astrapy import DataAPIClient
import os
from dotenv import load_dotenv
load_dotenv("config/.env")

client = DataAPIClient(os.getenv("ASTRA_DB_APPLICATION_TOKEN"))
db = client.get_database_by_api_endpoint(os.getenv("ASTRA_DB_API_ENDPOINT"))
collection = db.get_collection("user_feedback")

def submit_feedback(statement, verdict, user_verdict, reason):
    doc = {
        "statement": statement,
        "system_verdict": verdict,
        "user_verdict": user_verdict,
        "reason": reason
    }
    collection.insert_one(doc)
