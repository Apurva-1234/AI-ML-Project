#Twitter Sentiment Analysis System

A modern, full-stack application for real-time sentiment analysis of tweets using state-of-the-art Natural Language Processing (NLP).

![Design Preview](https://img.shields.io/badge/Aesthetics-Premium-blueviolet)
![Tech Stack](https://img.shields.io/badge/Stack-FastAPI%20%7C%20Transformers%20%7C%20VanillaJS-success)

##Overview

This project provides a comprehensive solution for analyzing public sentiment on Twitter. It leverages the `twitter-roberta-base-sentiment` model to classify text into Positive, Neutral, or Negative categories with high confidence.

##Key Features
- Real-time Prediction**: Instant sentiment analysis of any tweet text.
- Dynamic Dashboard**: Interactive visualizations of sentiment trends and statistics.
- Robust API**: Built with FastAPI for high performance and automatic documentation.
- Modern UI**: A sleek, responsive frontend designed with glassmorphism and smooth animations.
- Rate Limiting & Logging**: Production-ready features to ensure stability and traceability.

---

##Tech Stack

- Backend: Python, FastAPI, Hugging Face Transformers (RoBERTa), PyTorch.
- Frontend: HTML5, CSS3 (Custom Design System), Vanilla JavaScript.
- ML Training: Jupyter Notebooks, Scikit-learn (for EDA and baseline models).
- Deployment: Docker, Docker Compose.

---

## 📁 Project Structure

```text
├── backend/            # FastAPI Application
│   ├── app.py          # Main entry point
│   ├── sentiment.py    # ML Inference logic
│   ├── rate_limit.py   # Middleware for rate limiting
│   └── ...
├── frontend/           # Modern UI Components
│   ├── index.html      # Landing page
│   ├── dashboard.html  # Stats & Analytics
│   └── ...
├── ml/                 # Machine Learning Research
│   ├── train.py        # Model training scripts
│   └── evaluate.py     # Evaluation metrics
├── model/              # Serialized model artifacts
└── Dockerfile          # Containerization config
```

---

##Getting Started

### Prerequisites
- Python 3.9+
- Node.js (optional, for local frontend serving)
- Docker (recommended)

#Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd Twiteer_Sentiment
   ```

2. Setup Backend**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python -m uvicorn app:app --reload
   ```

3. **Open Frontend**:
   Simply open `frontend/index.html` in your browser or serve it using a local server.

### Running with Docker

```bash
docker-compose up --build
```

---

## Documentation

Once the backend is running, you can access the interactive API docs at:
- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

---

## Design System

The application uses a custom-built CSS design system featuring:
- **Gradient Backgrounds**: Deep purples and blues for a modern feel.
- **Glassmorphism**: Translucent cards with subtle blur effects.
- **Micro-animations**: Hover states and transition effects for an engaging UX.

---

## License

Distributed under the MIT License. See `LICENSE` for more information.

---


