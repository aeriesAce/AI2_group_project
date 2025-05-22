from Dashboard.charts import pydeck_chart
from Dashboard.ui import dashboard
import json

import streamlit as st
from Dashboard.llm import Gemini

def Gemi():
    st.title("Behöver du hjälp? fråga våran ChatBot Erika")
    prompt = st.text_area("Fråga:", height=100)
    if st.button("Fråga Erika"):

        if prompt.strip():
            with st.spinner("Erika svara strax..."):
                svar = Gemini(prompt)
                st.write(svar)
    else:
        st.warning("Hmm, nu blev det konstigt! försök igen.")
Gemi()


#with open("Dashboard/swedish_regions.geojson", encoding="utf-8") as f:
 #   regions_geojson = json.load(f)
dashboard()