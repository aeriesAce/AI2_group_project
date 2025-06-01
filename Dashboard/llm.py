import google.generativeai as genai 
import streamlit as st
import os
import pandas as pd
import json
import plotly.express as px
from Dashboard.charts import show_bar_chart
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("API_KEY"))
model = genai.GenerativeModel("gemini-2.0-flash")

def Gemini(prompt: str) -> str:

    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Fel {e}"


def call_Gemeni(df):
    st.subheader("Analysera annonser")

    prompts = {
        "Vanliga önskade egenskaper": "Analysera jobbeskrivningarna och lista de vanligaste egenskaperna som arbetsgivarna söker.",
        "Sammanfattning av krav": "Sammanfatta vilka krav som oftast förekommer i dessa jobbannonser.",
        "Gör en graf över det": """Analysera jobbeskrivningarna och returnera ett JSON-objekt med två listor:
        - "x": en lista med top tio egenskaperna arbetsgivare söker
        - "y": hur många yrken de vanligaste egenskaperna nämns

        Format:
        {
        "chart": {
            "x": [...],
            "y": [...],
        }
        }
        Returnera endast JSON utan förklaring."""
        }

    prompt_choice = st.selectbox("Välj analys:", list(prompts.keys()))
    selected_prompt = prompts[prompt_choice]

    # Ta beskrivningar från redan filtrerade df
    job_descriptions = df["job_description"].dropna().tolist()

    if len(job_descriptions) == 0:
        st.warning("Inga jobbeskrivningar tillgängliga för analys.")
    else:
        prompt_text = "\n\n".join(job_descriptions[:50])  # Begränsa för att inte krascha modellen
        full_prompt = f"{selected_prompt}\n\n{prompt_text}"

        if st.button("Sammanfatta"):
            with st.spinner("Rikard tänker, ett ögonblick"):
                response = Gemini(full_prompt)
                st.success("Rikard har tänkt klart")
                st.write(response)
            gemini_chart(df, prompts)


def gemini_chart(df, prompts):
    # fetches the non NAN job_descriptions to a list
    job_descriptions = df["job_description"].dropna().tolist()
    sample = "\n\n".join(job_descriptions[:50])

    # builds the prompt from the Gemeni function with job_description sample
    prompt = prompts["Gör en graf över det"] + sample
    response = Gemini(prompt)

    # cleans the data response and removes leading and trailing whitespaces
    raw = response.strip()

    # removes the markdown block
    if raw.startswith("```json"):
        raw = raw[7:-3].strip()

    # parses JSON and generate the chart
    try:
        chart_data = json.loads(raw)["chart"]
        df_chart = pd.DataFrame({
            "Egenskap": chart_data["x"],
            "Förekomst": chart_data["y"]
        })
        st.subheader(f"Top 10 mest efterfrågade personliga egenskaperna")
        show_bar_chart(df_chart, x="Egenskap", y="Förekomst")
    except:
        st.error("Kunde inte tolka JSON från Gemini.")
