import os
import re
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="Stress Text Analyzer", description="Deterministic Keyword-Based Stress Detection")

# --- CONFIGURATION ---
# Allow CORS for Frontend (Vercel/Localhost) to talk to Backend (Render)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace "*" with specific frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    text: str

# --- DATA LOADING ---
DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def load_csv(filename):
    """Safely load CSVs, return empty DataFrame on failure."""
    path = os.path.join(DATA_DIR, filename)
    try:
        if os.path.exists(path):
            return pd.read_csv(path)
    except Exception as e:
        print(f"Error loading {filename}: {e}")
    return pd.DataFrame(columns=["word", "weight"])

# Load all lexicons into memory on startup
lexicons = {
    "positive": load_csv("positive_words.csv"),
    "stress": load_csv("stress_words.csv"),
    "depressive": load_csv("depressive_words.csv"),
    "high_risk": load_csv("high_risk_words.csv")
}

# --- LOGIC ENGINE ---
def preprocess_text(text: str):
    """Lowercases and removes special characters for matching."""
    text = text.lower()
    # Keep only letters, numbers, and spaces
    text = re.sub(r'[^a-z0-9\s]', '', text)
    return text

def analyze_logic(text: str):
    clean_text = preprocess_text(text)
    detected_words = []
    total_score = 0
    
    # 1. CRITICAL CHECK (Override Rule)
    # Check high_risk words first using regex for exact phrase matching
    for _, row in lexicons["high_risk"].iterrows():
        word = row['word']
        # \b matches word boundaries to avoid partial matches (e.g. "die" in "diet")
        if re.search(r'\b' + re.escape(word) + r'\b', clean_text):
            return {
                "category": "CRITICAL",
                "score": 50, # Arbitrary high number
                "confidence": "high",
                "detected_keywords": [word],
                "show_help": True,
                "message": "Immediate help is recommended."
            }

    # 2. SCORING LOOP
    # Calculate score based on other categories
    # Stress/Depressive adds to score, Positive subtracts
    
    # Check Stress (+ weight)
    for _, row in lexicons["stress"].iterrows():
        word = str(row['word'])
        if re.search(r'\b' + re.escape(word) + r'\b', clean_text):
            total_score += row['weight']
            detected_words.append(word)

    # Check Depressive (+ weight)
    for _, row in lexicons["depressive"].iterrows():
        word = str(row['word'])
        if re.search(r'\b' + re.escape(word) + r'\b', clean_text):
            total_score += row['weight'] * 1.5 # Weight depressive words slightly higher
            detected_words.append(word)

    # Check Positive (- weight)
    for _, row in lexicons["positive"].iterrows():
        word = str(row['word'])
        if re.search(r'\b' + re.escape(word) + r'\b', clean_text):
            total_score -= row['weight']
            # We don't necessarily list positive words in 'detected_words' for the stress report, 
            # but we use them to lower the score.

    # 3. CATEGORIZATION
    category = "NORMAL"
    
    if total_score < 1:
        category = "POSITIVE" if total_score < 0 else "NORMAL"
    elif 1 <= total_score < 8:
        category = "STRESSED"
    elif total_score >= 8:
        category = "HIGH_STRESS"

    return {
        "category": category,
        "score": total_score,
        "confidence": "high" if len(detected_words) > 2 else "medium",
        "detected_keywords": list(set(detected_words)), # Unique only
        "show_help": False
    }

# --- API ENDPOINTS ---
@app.get("/")
def home():
    return {"status": "online", "message": "Stress Analyzer API is running."}

@app.post("/analyze")
def analyze_text(request: AnalyzeRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    result = analyze_logic(request.text)
    
    # Add crisis message only if CRITICAL
    if result["category"] == "CRITICAL":
        result["message"] = "You may be going through something very difficult. Help is available."
    
    return result

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)