import google.generativeai as genai 
import streamlit as st
import os
import pandas as pd
import json
import re
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
    st.subheader("Analysera egenskaper och krav")

    prompts = {
        "Vanliga önskade egenskaper": "Analysera jobbeskrivningarna och lista de vanligaste egenskaperna som arbetsgivarna söker, skriv ut detta snyggt i kolumner, ta bort 'Frekvens' men ha kvar sammanfattning.",
        "Sammanfattning av krav": "Sammanfatta vilka krav som oftast förekommer i dessa jobbannonser, skriv ut detta snyggt i kolumner.",
        "Visualisera det": """Analysera jobbeskrivningarna och returnera en chart med top 10 baserat på önskade egenskaper:
        Format:
        {
            "chart": {
                "x": [...],
                "y": [...]
            }
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

        if st.button("Analysera"):
            with st.spinner("Rikard tänker, ett ögonblick"):
                response = Gemini(full_prompt)
                st.success("Rikard har tänkt klart")

            if prompt_choice == "Visualisera det":
                try:
                    # Extrahera JSON från response
                    match = re.search(r"\{.*\}", response, re.DOTALL)
                    if not match:
                        st.error("Kunde inte hitta JSON i Gemini-svaret.")
                        st.code(response)
                        return

                    json_text = match.group(0)
                    data = json.loads(json_text)
                    x = data["chart"]["x"]
                    y = data["chart"]["y"]

                    df_chart = pd.DataFrame({
                        'Egenskap': x,
                        'Antal nämningar': y
                    })

                    st.write("### Top 10 personliga egenskaper som efterfrågas")
                    show_bar_chart(df_chart, x="Antal nämningar", y="Egenskap")
                    
                except Exception as e:
                    st.error("Fel vid tolkning av JSON.")
                    st.code(response)
                    st.exception(e)

            else:
                st.write(response)
