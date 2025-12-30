# 🧠 Text-Based Stress Analyzer

A lightweight, production-ready tool designed to analyze stress levels in user-provided text. Unlike traditional "black-box" AI, this tool uses a transparent, **weighted-keyword architecture** for high interpretability and reliability.

## 🚀 Features
- **Deterministic Scoring:** Uses curated CSV lexicons for Stress, Depression, and Positivity.
- **Safety-First (Critical Override):** Immediate detection of high-risk phrases with automated crisis resource routing (Helplines for India & Global).
- **Lightweight Stack:** No GPU required, no heavy Transformers, and zero database overhead.
- **Responsive UI:** Built with Bootstrap 5 and real-time JavaScript.

## 🛠️ Tech Stack
- **Backend:** Python 3.10+, FastAPI, Pandas (Data handling), Uvicorn.
- **Frontend:** HTML5, Bootstrap 5 (CDN), Vanilla JavaScript.
- **Deployment:** Optimized for Render (Backend) and Vercel/Netlify (Frontend).

## 📊 Logic Engine
The analyzer processes text through four layers:
1. **Normalization:** Lowercasing and symbol removal.
2. **Critical Check:** Scans for high-risk phrases (Overrides all other scores).
3. **Weighted Accumulation:** Calculates a net score by balancing stress/depressive weights against positive modifiers.
4. **Classification:** Categorizes results into `POSITIVE`, `NORMAL`, `STRESSED`, `HIGH_STRESS`, or `CRITICAL`.

## 📦 Installation & Setup
1. **Clone the repo:**
   ```bash
   git clone [https://github.com/yourusername/stress-text-analyzer.git](https://github.com/yourusername/stress-text-analyzer.git)
