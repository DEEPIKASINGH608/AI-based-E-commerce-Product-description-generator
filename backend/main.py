from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
import torch

app = FastAPI(title="AI E-Commerce Description Generator Backend")

# Initialize Hugging Face model and tokenizer (Completely Free & Downloads Locally)
MODEL_NAME = "google/flan-t5-base"
print("Loading AI Model... Please wait (this takes a moment on first run)...")
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME)
print("Model loaded successfully!")

# Define the structure of incoming requests
class DescriptionRequest(BaseModel):
    product_name: str
    category: str
    keywords: str
    tone: str
    platform: str  # e.g., Amazon, Shopify, Instagram

@app.get("/")
def home():
    return {"message": "AI Generator Backend is running smoothly!"}

@app.post("/generate")
def generate_description(data: DescriptionRequest):
    try:
        # Engineering advanced prompts based on features chosen by user
        prompt = (
            f"Write a professional, high-converting e-commerce product description for a website catalog.\n"
            f"Product Name: {data.product_name}\n"
            f"Category: {data.category}\n"
            f"Target Platform: {data.platform}\n"
            f"Tone of Voice: {data.tone}\n"
            f"Essential Keywords to Include: {data.keywords}\n\n"
            f"Output a compelling product description followed by 3 optimized bullet points for features."
        )

        # Tokenize prompt inputs
        inputs = tokenizer(prompt, return_tensors="pt", max_length=512, truncation=True)

        # Generate text using specific parameters to prevent repetition and increase quality
        outputs = model.generate(
            **inputs,
            max_length=250,
            num_beams=4,
            early_stopping=True,
            no_repeat_ngram_size=3
        )

        # Decode text back to human language
        generated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

        return {
            "product": data.product_name,
            "description": generated_text
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


    