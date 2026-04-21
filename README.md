# 🥦 NutriQuest: Contextual Bio-Feedback Engine

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Google Cloud Run](https://img.shields.io/badge/Deployed_on-Google_Cloud_Run-4285F4.svg?logo=googlecloud)](https://cloud.google.com/run)
[![Status](https://img.shields.io/badge/Status-Live-success.svg)]()

**NutriQuest** is a gamified, multi-factor heuristic scoring engine that transforms nutritional choices into an interactive journey. Instead of a generic calorie counter, NutriQuest evaluates a user's food cravings against their current physiological and cognitive state to provide highly optimized, scientifically-backed alternatives.

## 🎯 The Vision
We believe health apps shouldn't feel like clinical dashboards. NutriQuest introduces **Brock the Broccoli**, an interactive mascot that acts as a real-time bio-feedback mirror. As users input their cognitive load and metabolic state, Brock's emotional state changes, guiding users toward healthier choices through empathy and gamification.

## ✨ Core Features
* **Contextual Heuristic Engine:** An algorithmic backend that simultaneously evaluates circadian rhythm, stress levels, and metabolic state against macronutrient profiles.
* **Interactive Mascot (Brock):** Real-time UI updates that map user state to emotional feedback without backend latency.
* **Stateless Architecture:** Built strictly for infinite scalability on Google Cloud Run. The API requires no persistent database, handling state entirely via payload.
* **Dynamic Visual Generation:** Integrates with stateless AI image endpoints (`pollinations.ai`) to instantly render mouth-watering previews of healthy alternatives.
* **Accessible & Gamified UX:** Features a multi-step horizontal journey, ARIA-compliant screen-reader tags, and zero-dependency CSS particle physics (Confetti/Vignettes) for reward loops.

## 🛠️ Tech Stack
* **Backend:** Python, FastAPI, Uvicorn, Pydantic (Strict Type Hinting).
* **Frontend:** Vanilla HTML5, CSS3 (Glassmorphism & Keyframes), Vanilla JavaScript (ES6+). *Zero heavy frontend frameworks.*
* **Testing:** Python `unittest` framework.
* **Deployment & Ops:** Docker, Google Cloud Build, Google Cloud Run.

## 🚀 Local Quickstart

### 1. Clone the Repository
```bash
git clone [https://github.com/JakkiRajasekharRamana/AMD-Hackathon.git](https://github.com/JakkiRajasekharRamana/AMD-Hackathon.git)
cd AMD-Hackathon
