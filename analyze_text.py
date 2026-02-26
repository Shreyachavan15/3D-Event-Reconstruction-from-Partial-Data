from transformers import pipeline
from datetime import datetime
import json

ner = pipeline(
    "ner",
    model="dslim/bert-base-NER",
    aggregation_strategy="simple"
)

summarizer = pipeline(
    "summarization",
    model="facebook/bart-large-cnn"
)

def analyze_text(text: str):
    ner_results = ner(text)

    entities = [
        {
            "text": ent["word"],
            "label": ent["entity_group"],
            "confidence": round(ent["score"], 2)
        }
        for ent in ner_results
    ]

    summary = summarizer(
        text,
        max_length=60,
        min_length=25,
        do_sample=False
    )[0]["summary_text"]

    return {
        "type": "text_event",
        "raw_text": text,
        "summary": summary,
        "entities": entities,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

if __name__ == "__main__":
    result = analyze_text("A boy was running in the park at 5 PM.")

    with open("text_output.json", "w", encoding="utf-8") as f:
        json.dump(result, f, indent=4)

    print("✅ Saved text_output.json")
