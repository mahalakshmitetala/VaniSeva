# VaniSeva — Multilingual Citizen Complaint Department Identifier

*Vani* (వాణి) = Voice | *Seva* (సేవ) = Service

Helping citizens identify the correct government department for their complaint — in their own language, through voice or text.

**Live App:** [vaniseva.streamlit.app](https://vaniseva.streamlit.app)

---

## The Problem

Citizens in rural and multilingual regions often do not know which government department handles their complaint. This leads to misdirected visits, wasted time, and unresolved issues — especially for those unfamiliar with government structure or who cannot communicate in English.

---

## What VaniSeva Does

A citizen enters their complaint in any supported Indian language — by typing in native script, Romanized form, or speaking via voice input. VaniSeva translates it, classifies it using a trained ML model, and tells them exactly which government department handles it. It also generates a formatted complaint letter in English that they can download and submit.

---

## Features

- Multilingual input — English, Hindi, Telugu, Tamil, Kannada, and Malayalam
- Voice input — speak your complaint directly in your language
- Romanized text support — type Telugu or Hindi in English letters
- Auto-translation to English before classification
- ML-based department prediction with confidence score
- Voice output — result is read aloud in the user's language after classification
- User authentication — register and login with secure SHA-256 password hashing
- Complaint history — every classification is saved per user to MongoDB Atlas
- PDF complaint letter — auto-generated formatted letter downloadable in English
- Cloud database — persistent storage via MongoDB Atlas across all sessions

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
| Authentication | Custom — SHA-256 hashing, MongoDB storage |
| Database | MongoDB Atlas (cloud, persistent) |
| Language | Python 3 |

---

## Project Structure

```
VaniSeva/
├── app.py                      # Main application
├── auth.py                     # Login and registration logic
├── db.py                       # MongoDB connection
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
