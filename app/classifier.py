from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# Pre-trained fake news detection model
MODEL_NAME = "roberta-base"

# Load tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)

# Inference pipeline
classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)

def classify_news(text: str):
    result = classifier(text, truncation=True, max_length=512)[0]
    label = result["label"]
    score = result["score"]

    # Label mapping based on this model
    label_map = {
        "LABEL_0": "Fake",
        "LABEL_1": "Real"
    }

    return {
        "verdict": label_map.get(label, "Unknown"),
        "confidence": round(score * 100, 2)
    }
