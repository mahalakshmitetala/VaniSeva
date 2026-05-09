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
- 6 Indian languages supported
- Voice output of result in user's language
- Auto-generated downloadable complaint letter (PDF)
- User login with secure password hashing
- Complaint history saved per user via MongoDB Atlas
  
---
## Tech Stack
- Python
- Streamlit 
- Scikit-learn
- MongoDB Atlas
- Deep Translator
- gTTS
- fpdf2
- Web Speech API

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
## Future Scope

- Direct complaint submission to department portals via API integration
- Government official dashboard for complaint tracking and analytics
- Support for more regional languages and dialects
- SMS-based interface for users without smartphones

---

**Tetala Mahalakshmi**
