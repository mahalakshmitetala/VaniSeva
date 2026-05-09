import streamlit as st
from pymongo import MongoClient


@st.cache_resource
def get_db():
    client = MongoClient(st.secrets["MONGO_URI"])
    return client["vaniseva"]
