from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

app = FastAPI(title="Advanced AI Copywriting Engine")

# --- CROSS-ORIGIN RESOURCE SHARING (CORS) LAYER ---
# This permits your Streamlit frontend browser window to securely query the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins, or narrow it down to ["http://localhost:8501"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_NAME = "google/flan-t5-base"
print("Initializing localized language model transformer weights...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
print("System Engine Ready.")

class AdvancedGenerationRequest(BaseModel):
    product_name: str
    category: str
    keywords: str
    tone: str
    platform: str
    creativity_bias: float = 0.7

@app.post("/generate")
def run_generation_pipeline(data: AdvancedGenerationRequest):
    try:
        system_prompt = (
            f"Task: Write a highly engaging marketing product listing description for an online retail catalog.\n"
            f"Product: {data.product_name}\n"
            f"Industry Category: {data.category}\n"
            f"Optimized Target Channel: {data.platform}\n"
            f"Brand Tone: {data.tone}\n"
            f"Crucial Search Keywords: {data.keywords}\n\n"
            f"Format Output Exactly as follows:\n"
            f"Description: [Write a engaging 3-sentence promotional overview narrative]\n"
            f"Bullet Points:\n"
            f"- [Feature bullet 1]\n"
            f"- [Feature bullet 2]\n"
            f"- [Feature bullet 3]"
        )

        inputs = tokenizer(system_prompt, return_tensors="pt", max_length=512, truncation=True)

        outputs = model.generate(
            **inputs,
            max_length=300,
            temperature=data.creativity_bias,
            do_sample=True,
            num_beams=2,
            no_repeat_ngram_size=3,
            early_stopping=True
        )

        raw_result = tokenizer.decode(outputs[0], skip_special_tokens=True)

        description_part = "Failed to parse narrative copy snippet."
        bullet_part = []

        if "Description:" in raw_result:
            parts = raw_result.split("Bullet Points:")
            description_part = parts[0].replace("Description:", "").strip()
            if len(parts) > 1:
                bullet_part = [b.strip("- ") for b in parts[1].split("\n") if b.strip()]
        else:
            description_part = raw_result

        return {
            "narrative": description_part,
            "bullets": bullet_part if bullet_part else ["High-durability construction material.", "Optimized for day-to-day lifestyle usage.", "Eco-friendly component layout build."]
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


