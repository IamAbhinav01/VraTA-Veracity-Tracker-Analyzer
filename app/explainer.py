import os
import json
from dotenv import load_dotenv
from langchain_nvidia import ChatNVIDIA
from app.rag_retriever import retrieve_facts
from tools.web_tools import search, tell_news  

# Load environment variables
load_dotenv("config/.env")
if os.getenv("LANGSMITH_TRACING", "false").lower() == "true":
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_ENDPOINT"] = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
    os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
    os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGSMITH_PROJECT", "default")
nvidia_api_key = os.getenv("NVIDIA_API_KEY")

# Initialize NVIDIA Mixtral
llm = ChatNVIDIA(
    model="mistralai/mixtral-8x7b-instruct-v0.1",
    api_key=nvidia_api_key,
    temperature=0.6
)

# 🔍 Main function
async def generate_explanation(statement: str, verdict=None):
    # 📦 Retrieve from Astra DB (RAG)
    facts = retrieve_facts(statement)

    rag_context = "\n\n".join([
        f"{fact['text']} (🔗 {fact.get('url') or 'URL not available'})"
        for fact in facts
    ])

    # 🌐 Live Search + News
    live_search = await search(None, statement)
    live_news = await tell_news(None, statement)

    # 🧠 Final prompt context
    full_context = f"""
📚 Facts from DB:
{rag_context}

🌐 Web Search Results:
{live_search}

🗞️ Latest News:
{live_news}
"""

    prompt = f"""
Statement: "{statement}"

Use the following context (DB + live search + news) to decide if it's Real or Fake.

Context:
{full_context}

Respond strictly in JSON format:
{{
  "verdict": "Real or Fake",
  "confidence": "0 to 100",
  "explanation": "Short justification"
}}
"""

    # 🧠 LLM Response
    raw_response = llm.invoke(prompt)

    # 🧪 Parse JSON safely
    try:
        response = json.loads(raw_response.content)
    except Exception as e:
        return {
            "verdict": "Unknown",
            "confidence": 0.0,
            "explanation": f"Error parsing LLM output: {e}",
            "retrieved_context": full_context
        }

    # ✅ Safely cast confidence
    try:
        confidence = float(response.get("confidence", 0.0))
    except (ValueError, TypeError):
        confidence = 0.0

    return {
        "verdict": response.get("verdict", "Unknown"),
        "confidence": confidence,
        "explanation": response.get("explanation", "No explanation available."),
        "retrieved_context": full_context
    }
