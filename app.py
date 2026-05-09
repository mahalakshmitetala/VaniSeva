import streamlit as st
import joblib
import numpy as np
from datetime import datetime
from deep_translator import GoogleTranslator
import streamlit.components.v1 as components
from gtts import gTTS
import base64
import tempfile

from auth import show_auth_page, is_logged_in, logout
from pdf_generator import generate_pdf
from db import get_db

# ------------------------------------------------------------------ #
#  PAGE CONFIG
# ------------------------------------------------------------------ #

st.set_page_config(page_title="VaniSeva", layout="centered")

st.markdown("""
<style>
    [data-testid="stStatusWidget"] { display: none !important; }
    section[data-testid="stSidebar"] { display: none; }

    .field-label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.07em;
        text-transform: uppercase;
        margin-bottom: 4px;
        color: #9aa6b2;
    }
    .stTextArea textarea {
        background-color: #ffffff !important;
        color: #111827 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
    }
    .stTextArea textarea::placeholder {
        color: #9ca3af !important;
    }
    .stSelectbox > div > div {
        background-color: #ffffff !important;
        color: #111827 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
    }
    .stSelectbox svg {
        fill: #111827 !important;
    }
    .stButton > button {
        background-color: #ffffff !important;
        color: #111827 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        font-size: 14px !important;
        padding: 10px !important;
    }
    .stButton > button:hover {
        border-color: #2563eb !important;
        color: #2563eb !important;
        background-color: #ffffff !important;
    }
    .stDownloadButton > button {
        background-color: #ffffff !important;
        color: #111827 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 8px !important;
        width: 100% !important;
        font-size: 14px !important;
    }
    .stDownloadButton > button:hover {
        border-color: #2563eb !important;
        color: #2563eb !important;
    }
    .result-card {
        border: 1px solid #1e293b;
        padding: 20px 24px;
        border-radius: 12px;
        background: #0f172a;
        margin-top: 16px;
        margin-bottom: 16px;
    }
    .result-label {
        font-size: 11px;
        font-weight: 600;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #9aa6b2;
        margin-bottom: 6px;
    }
    .result-dept {
        font-size: 24px;
        font-weight: 700;
        color: #f1f5f9;
        margin-bottom: 6px;
    }
    .result-desc {
        color: #94a3b8;
        font-size: 13px;
        margin-bottom: 14px;
    }
    .result-conf {
        color: #3b82f6;
        font-size: 12px;
        font-weight: 500;
    }
    hr { border-color: #1e293b; margin: 20px 0; }
    .stExpander { border: 1px solid #1e293b; border-radius: 8px; }
</style>
""", unsafe_allow_html=True)


# ------------------------------------------------------------------ #
#  AUTH GATE
# ------------------------------------------------------------------ #

if not is_logged_in():
    show_auth_page()
    st.stop()

username = st.session_state["username"]
fullname = st.session_state["fullname"]


# ------------------------------------------------------------------ #
#  MODEL
# ------------------------------------------------------------------ #

@st.cache_resource
def load_model():
    model      = joblib.load("models/complaint_model.pkl")
    vectorizer = joblib.load("models/tfidf_vectorizer.pkl")
    return model, vectorizer


# ------------------------------------------------------------------ #
#  HELPERS
# ------------------------------------------------------------------ #

def translate(text):
    try:
        return GoogleTranslator(source="auto", target="en").translate(text)
    except Exception:
        return text


def speak_result(text, lang_code):
    try:
        tts = gTTS(text=text, lang=lang_code)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
            tts.save(f.name)
            audio_bytes = open(f.name, "rb").read()
        b64 = base64.b64encode(audio_bytes).decode()
        st.markdown(
            f'<audio autoplay>'
            f'<source src="data:audio/mp3;base64,{b64}" type="audio/mp3">'
            f'</audio>',
            unsafe_allow_html=True,
        )
    except Exception:
        pass


# ------------------------------------------------------------------ #
#  MONGODB COMPLAINT FUNCTIONS
# ------------------------------------------------------------------ #

def save_complaint(username, complaint_text, department, confidence):
    col = get_db()["complaints"]
    col.insert_one({
        "username":   username,
        "complaint":  complaint_text,
        "department": department,
        "confidence": f"{confidence:.1f}%",
        "date":       datetime.now().strftime("%d-%m-%Y %H:%M"),
    })


def load_history(username):
    col  = get_db()["complaints"]
    rows = list(col.find({"username": username}, {"_id": 0}).sort("date", -1))
    return rows


# ------------------------------------------------------------------ #
#  DEPARTMENT INFO
# ------------------------------------------------------------------ #

DEPT_INFO = {
    "PWD":                   "Public Works Department - Roads, Bridges, Government Buildings",
    "Municipality":          "Municipality - Drainage, Street Lights, Sanitation",
    "Water Board":           "Water Board - Drinking Water Supply and Pipeline Issues",
    "Electricity":           "Electricity Department - Power Cuts and Meter Issues",
    "Police":                "Police Department - Law and Order, Safety Complaints",
    "Revenue":               "Revenue Department - Land Records, Patta, Survey Issues",
    "Agriculture":           "Agriculture Department - Crop, Seeds, Fertilizer Issues",
    "Health":                "Health Department - Hospitals, Medicines, Medical Services",
    "Education":             "Education Department - Schools, Teachers, Mid-day Meal Issues",
    "Panchayat":             "Gram Panchayat - Village-level Civic Issues",
    "Sanitation":            "Sanitation Department - Waste Collection and Cleanliness",
    "Public Infrastructure": "Public Infrastructure - General Civic Infrastructure",
}


def get_dept_description(dept):
    for key, val in DEPT_INFO.items():
        if key.lower() in dept.lower():
            return val
    return dept


# ------------------------------------------------------------------ #
#  SESSION INIT
# ------------------------------------------------------------------ #

if "complaint" not in st.session_state:
    st.session_state.complaint = ""
if "result" not in st.session_state:
    st.session_state.result = None


# ------------------------------------------------------------------ #
#  HEADER
# ------------------------------------------------------------------ #

col_title, col_logout = st.columns([5, 1])

with col_title:
    st.markdown(f"""
    <div style='padding: 8px 0 20px 0;'>
        <div style='font-size:22px; font-weight:700;'>VaniSeva</div>
        <div style='color:#9aa6b2; font-size:13px; margin-top:2px;'>Welcome, {fullname}</div>
    </div>
    """, unsafe_allow_html=True)

with col_logout:
    if st.button("Logout"):
        logout()
        st.rerun()

st.markdown("<hr>", unsafe_allow_html=True)


# ------------------------------------------------------------------ #
#  TABS
# ------------------------------------------------------------------ #

tab_classify, tab_history = st.tabs(["Classify Complaint", "My History"])


# ================================================================== #
#  TAB 1 — CLASSIFY
# ================================================================== #

with tab_classify:

    st.markdown("<p class='field-label'>Language</p>", unsafe_allow_html=True)
    language = st.selectbox(
        "",
        ["English", "Hindi", "Telugu", "Tamil", "Kannada", "Malayalam"],
        label_visibility="collapsed",
    )

    lang_map = {
        "English":   ("en-IN", "en"),
        "Hindi":     ("hi-IN", "hi"),
        "Telugu":    ("te-IN", "te"),
        "Tamil":     ("ta-IN", "ta"),
        "Kannada":   ("kn-IN", "kn"),
        "Malayalam": ("ml-IN", "ml"),
    }
    speech_lang, tts_lang = lang_map[language]

    st.markdown("<p class='field-label' style='margin-top:12px;'>Your Complaint</p>", unsafe_allow_html=True)
    complaint = st.text_area(
        "",
        value=st.session_state.complaint,
        height=120,
        placeholder="Type your complaint here, or use voice input below...",
        label_visibility="collapsed",
    )
    st.session_state.complaint = complaint

    st.markdown("""
    <p class='field-label' style='margin-top:12px;'>Voice Input</p>
    <p style='color:#475569; font-size:12px; margin-bottom:8px;'>
        Click Start, speak your complaint, then copy the recognised text into the box above.
    </p>
    """, unsafe_allow_html=True)

    components.html(f"""
    <style>
        #voiceBtn {{
            width: 100%;
            padding: 10px;
            border-radius: 8px;
            background: #ffffff;
            color: #111827;
            border: 1px solid #d1d5db;
            font-size: 14px;
            cursor: pointer;
            font-family: sans-serif;
        }}
        #voiceBtn:hover {{ border-color: #2563eb; color: #2563eb; }}
        #voiceOutput {{
            color: #374151;
            margin-top: 10px;
            min-height: 18px;
            font-size: 13px;
            font-family: sans-serif;
        }}
        #copyBtn {{
            display: none;
            margin-top: 8px;
            padding: 5px 14px;
            border-radius: 6px;
            background: #ffffff;
            color: #111827;
            border: 1px solid #d1d5db;
            cursor: pointer;
            font-size: 12px;
            font-family: sans-serif;
        }}
        #copyBtn:hover {{ border-color: #2563eb; color: #2563eb; }}
    </style>
    <button id="voiceBtn" onclick="startRecognition()">Start Speaking</button>
    <p id="voiceOutput"></p>
    <button id="copyBtn" onclick="copyText()">Copy Text</button>
    <script>
        let recognized = "";
        function startRecognition() {{
            recognized = "";
            document.getElementById("voiceOutput").innerText = "Listening...";
            document.getElementById("copyBtn").style.display = "none";
            const r = new webkitSpeechRecognition();
            r.lang = "{speech_lang}";
            r.interimResults = false;
            r.onresult = function(e) {{
                recognized = e.results[0][0].transcript;
                document.getElementById("voiceOutput").innerText = recognized;
                const btn = document.getElementById("copyBtn");
                btn.style.display = "inline-block";
                btn.innerText = "Copy Text";
            }};
            r.onerror = function() {{
                document.getElementById("voiceOutput").innerText = "Could not recognise speech. Please try again.";
            }};
            r.start();
        }}
        function copyText() {{
            navigator.clipboard.writeText(recognized);
            document.getElementById("copyBtn").innerText = "Copied";
        }}
    </script>
    """, height=150, scrolling=False)

    col1, col2 = st.columns(2)
    with col1:
        do_classify = st.button("Classify", use_container_width=True)
    with col2:
        do_clear = st.button("Clear", use_container_width=True)

    if do_clear:
        st.session_state.complaint = ""
        st.session_state.result    = None
        st.rerun()

    if do_classify:
        text = st.session_state.complaint.strip()
        if not text:
            st.warning("Please enter a complaint before classifying.")
        else:
            with st.spinner("Classifying..."):
                translated        = translate(text)
                model, vectorizer = load_model()
                vec               = vectorizer.transform([translated])
                pred              = model.predict(vec)[0]
                conf              = float(np.max(model.predict_proba(vec))) * 100

            st.session_state.result = {
                "department": pred,
                "confidence": conf,
                "original":   text,
                "translated": translated,
                "tts_lang":   tts_lang,
            }
            save_complaint(username, translated, pred, conf)

    if st.session_state.result:
        r         = st.session_state.result
        dept_desc = get_dept_description(r["department"])

        st.markdown(f"""
        <div class="result-card">
            <div class="result-label">Identified Department</div>
            <div class="result-dept">{r['department']}</div>
            <div class="result-desc">{dept_desc}</div>
            <div class="result-conf">Confidence: {r['confidence']:.1f}%</div>
        </div>
        """, unsafe_allow_html=True)

        if r["tts_lang"] == "te":
            speak_text = f"Mee complaint {r['department']} department ki chendutundi."
        elif r["tts_lang"] == "hi":
            speak_text = f"Aapki shikayat {r['department']} vibhag se sambandhit hai."
        else:
            speak_text = f"Your complaint belongs to the {r['department']} department."

        speak_result(speak_text, r["tts_lang"])

        pdf_bytes = generate_pdf(
            fullname=fullname,
            complaint_text=r["translated"],
            department=r["department"],
            dept_description=dept_desc,
        )
        st.download_button(
            label="Download Complaint Letter (PDF)",
            data=pdf_bytes,
            file_name=f"VaniSeva_{r['department'].replace(' ', '_')}_Complaint.pdf",
            mime="application/pdf",
            use_container_width=True,
        )


# ================================================================== #
#  TAB 2 — HISTORY
# ================================================================== #

with tab_history:
    st.markdown(
        "<p style='color:#64748b; font-size:13px; margin-bottom:16px;'>"
        "Your past complaints and the departments identified for each."
        "</p>",
        unsafe_allow_html=True,
    )

    history = load_history(username)

    if not history:
        st.info("You have not classified any complaints yet.")
    else:
        for row in history:
            label = f"{row.get('date', '')}  —  {row.get('department', '')}"
            with st.expander(label):
                st.markdown(f"**Complaint:** {row.get('complaint', '')}")
                st.markdown(f"**Department:** {row.get('department', '')}")
                st.markdown(f"**Confidence:** {row.get('confidence', '')}")
