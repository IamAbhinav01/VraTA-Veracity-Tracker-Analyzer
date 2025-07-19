from fastapi import FastAPI
from pydantic import BaseModel
from app.explainer import generate_explanation
from app.classifier import classify_news
from app.rag_retriever import retrieve_facts

app = FastAPI()

class NewsInput(BaseModel):
    text: str

@app.get("/")
def root():
    return {"message": "Welcome to VraTA.AI - Fake News Detector"}

@app.post("/evaluate")
def evaluate_news(item: NewsInput):
    result = classify_news(item.text)
    context = retrieve_facts(item.text)
    explanation = generate_explanation(item.text, result["verdict"])
    
    return {
        "text": item.text,
        "verdict": result["verdict"],
        "confidence": result["confidence"],
        "explanation": explanation,
        "retrieved_context": context
    }
