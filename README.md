# VaniSeva — Multilingual Citizen Complaint Department Identifier

*Vani* (వాణి) = Voice | *Seva* (సేవ) = Service

Helping citizens identify the correct government department for their complaint — in their own language, through voice or text.

**Live App:** [VaniSeva on Streamlit](https://locallanguagecomplaintclassifier-zhhueftxujvsrbqee6esbf.streamlit.app/)

---

## The Problem

Citizens in rural and multilingual regions often do not know which government department handles their complaint. This leads to misdirected visits, wasted time, and unresolved issues — especially for those unfamiliar with government structure or who cannot read English.

---

## What VaniSeva Does

A citizen enters their complaint in any supported Indian language — by typing in native script, typing in Romanized form, or speaking via voice input. VaniSeva translates it, classifies it using a trained ML model, and tells them exactly which government department handles it. It also generates a formatted complaint letter in English that they can download and submit.

---

## Features

- Multilingual input — English, Hindi, Telugu, Tamil, Kannada, and Malayalam
- Voice input — speak your complaint directly in your language
- Romanized text support — type Telugu or Hindi in English letters
- Auto-translation to English before classification
- ML-based department prediction with confidence score
- Voice output — result is read aloud in the user's language after classification
- User authentication — register and login with secure password hashing
- Complaint history — every classification is saved per user
- PDF complaint letter — auto-generated, formatted, and downloadable in English

---

## Tech Stack

| Layer | Technology |
|---|---|
| Application | Streamlit |
| ML Model | Scikit-learn (TF-IDF + Classifier) |
| Translation | Deep Translator (Google Translate API) |
| Voice Input | Web Speech API |
| Voice Output | gTTS (Google Text-to-Speech) |
| PDF Generation | fpdf2 |
| Authentication | Custom — hashlib SHA-256, JSON storage |
| Language | Python 3 |

---

## Project Structure

```
VaniSeva/
├── app.py                      # Main application
├── auth.py                     # Login and registration logic
├── pdf_generator.py            # Complaint letter PDF generator
├── requirements.txt
├── DejaVuSans.ttf              # Unicode font for PDF rendering
├── .streamlit/
│   └── config.toml             # Theme configuration
└── models/
    ├── complaint_model.pkl     # Trained classification model
    └── tfidf_vectorizer.pkl    # TF-IDF vectorizer
```

---

## How to Run Locally

```bash
git clone https://github.com/mahalakshmitetala/VaniSeva.git
cd VaniSeva
pip install -r requirements.txt
streamlit run app.py
```

---

## Use Case

A villager in Andhra Pradesh notices a broken road but does not know whether to approach the municipality, NHAI, or Panchayat. They open VaniSeva, speak their complaint in Telugu, and instantly learn which department to approach — with a downloadable complaint letter ready to submit.

---

## Future Scope

- Direct complaint submission to department portals via API integration
- Government official dashboard for complaint tracking and analytics
- Support for more regional languages and dialects
- SMS-based interface for users without smartphones

---

## Author

**Tetala Mahalakshmi**
B.Tech 3rd Year | Andhra Pradesh, India
[GitHub](https://github.com/mahalakshmitetala)
