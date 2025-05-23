import google.generativeai as genai 
from dotenv import load_dotenv
from Dashboard.charts import pydeck_chart
from Dashboard.ui import dashboard
import json

import streamlit as st
import os 

load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

def Gemini(prompt: str) -> str:

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Fel {e}"



def ask_gemini():
    st.title("Behöver du hjälp? fråga våran ChatBot Erika")
    prompt = st.text_area("Fråga:", height=100)
    if st.button("Fråga Erika"):

        if prompt.strip():
            with st.spinner("Erika svara strax..."):
                svar = Gemini(prompt)
                st.write(svar)
    else:
        st.warning("Hmm, nu blev det konstigt! försök igen.")
