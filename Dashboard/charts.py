import streamlit as st
import plotly_express as px
import duckdb
import numpy as np
import pandas as pd
import pydeck as pdk
import json

con = duckdb.connect('jobs.duckdb')

def jobs_per_type():                ### Vet inte riktigt varför denna är här om jag ska vara ärlig? men men
    # SQL-fråga för att få antalet jobb per job_type
    query = """
    SELECT job_type, COUNT(*) as count
    FROM marts.mart_anstallningsvillkor
    GROUP BY job_type;
    """

    # Utför SQL-frågan och hämta resultatet
    data = pd.read_sql(query, con)
    con.close()

    # Visa resultatet i Streamlit
    st.title("Jobbstatistik baserat på anställningsvillkor")
    st.bar_chart(data.set_index('job_type'))

# ------------------------------ TEST KPI FÖR MAP CHART -----------------------------------
# bro this is a query <3 / elvira

df = con.execute("""
    SELECT municipality, SUM(vacancies) AS vacancies
    FROM marts.mart_pedagogik
    GROUP BY municipality
""").fetchdf()


# ------------------------------------------- om vi vill ha kanske, vet inte? sparar den här, för då kan vi göra om den nedanför så vi kan ha alla occpupations ----------------------
def sun_chart(select_occ):
    df = con.execute("SELECT * FROM marts.mart_pedagogik").fetch_df()
    df = df[df["occupation_category"] == select_occ]
    top_employers = df.groupby(['employer_name', 'municipality'], as_index=False)['vacancies'].sum()
    fig = px.sunburst(
        top_employers,
        path =['municipality', 'vacancies'],
        values = 'vacancies',
        color = 'vacancies', 
        hover_data={'vacancies': True},
        color_continuous_scale='blues',
        color_continuous_midpoint=np.average(df['vacancies'], weights=df['vacancies'])
    )

    st.plotly_chart(fig)



    # ----------------------------------------------------- Generell funktion för charts -------------------------------------------------------------------------

def show_bar_chart(data: str, x: str, y: str):

    if isinstance(data, str):
        df = con.execute(data).fetch_df()  # om det är en SQL-sträng
    else:
        df = data

    fig = px.bar(df, x=x, y=y, 
                labels={x: x.replace("_", " ").title(),
                        y: y.replace("_", " ").title()}, 
                color=y, 
                color_continuous_scale= "ylgn")
    st.plotly_chart(fig, theme = "streamlit")

    # ------------------------------------------------------- Generell funktion för PyDeck map chart --------------------------------------------------------------#

def pydeck_chart(geojson_data, df, match_col_geojson, match_col_df, value_col, use_normalized=True,color_scale_factor=255, tooltip_title="område", tooltip_field = "kom_namn", zoom=4):

    df[match_col_df] = df[match_col_df].astype(str).str.strip().str.lower()
    for feature in geojson_data["features"]:
        geo_name = feature["properties"].get(match_col_geojson, "").strip().lower()
        match = df[df[match_col_df].str.strip().str.lower() == geo_name.strip().lower()]

        if not match.empty:
            feature["properties"]["value"] = int(match[value_col].values[0])
    else:
        feature["properties"]["value"] = 0
    
    if use_normalized:
        max_val = max([np.log1p(f["properties"].get("value", 0)) for f in geojson_data["features"] if isinstance(f["properties"].get("value", 0), (int,float))])
        for f in geojson_data["features"]:
            val = f["properties"].get("value", 0)
            log_val = np.log1p(val)
            f["properties"]["norm_value"] = log_val / max_val if max_val > 0 else 0
        else:
            for f in geojson_data["features"]:
                val = f["properties"].get("value", 0)
                f["properties"]["color_val"] = val * color_scale_factor


    layer = pdk.Layer(
        "GeoJsonLayer",
        geojson_data,
        pickable=True,
        opacity=0.3,
        stroked=True,
        filled=True,
        get_fill_color= "[properties.norm_value * 200, 100, 160,180]",#f"[value * {color_scale_factor}, 100, 160, 180]",
        get_line_color=[255, 255, 255],
    )

    view_state = pdk.ViewState(
        latitude=60.1282,
        longitude=18.6435,
        zoom=zoom, 
        pitch=30,
    )
    tooltip = {"text": f"{{{tooltip_field}}}\n{tooltip_title}: {{value}}"}

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip= tooltip
    )

    st.pydeck_chart(deck)

def call_pydeck_chart():
    with open("Data/swedish_municipalities.geojson", encoding="utf-8") as f:
        geojson_data = json.load(f)
    st.title("Antal platser per kommun – Pedagogik")
    pydeck_chart(
                geojson_data=geojson_data,
                df=df,
                match_col_geojson="kom_namn",         # geojson matchning
                match_col_df="municipality",      # matchar med municipality
                value_col="vacancies",
                use_normalized = True,
                tooltip_title="område",
                tooltip_field = "kom_namn"
            )


#######################       Denna är inte generell än, kommer bygga om den lite, men blir lättare att se för mig sen när jag ser helheten ############
#######################       Men kommer få pilla lite mer med den när jag ser datan ordentligt för färger etc ################






 ######################################## UNDER här är kpi's vilket vi kommer flytta ut sen ########################


    # ------------------------------------------------------ Top 10 inom lager vi stoppar in i den generella funktionen -----------------------------------------------

def show_top_employers_tdl():
    df = con.execute("SELECT * FROM marts.mart_tran_lager").fetch_df()
    top_employers = (df.groupby("employer_name", as_index=False)
                                ['vacancies'].sum()
                                .sort_values('vacancies',ascending=False).head(10))
    show_bar_chart(top_employers, "employer_name", 'vacancies', "Top 10 arbetsgivare inom Transport och Lager")

# ------------------------------------------------------ Top 10 inom pedagogik vi stoppar in i den generella funktionen -----------------------------------------------

def show_top_employers_pedagogik():
    df = con.execute("SELECT * FROM marts.mart_pedagogik").fetch_df()
    top_employers = (df.groupby("employer_name", as_index=False)
                                ["Totala jobb"].sum()
                                .sort_values("Totala jobb",ascending=False).head(10))
    show_bar_chart(top_employers, "employer_name", "Totala jobb", "Top 10 arbetsgivare inom Pedagogik")

# ------------------------------------------------------ Top 10 inom säkerhet och bevakning vi stoppar in i den generella funktionen -----------------------------------------------

def show_top_employers_sob():
    df = con.execute("SELECT * FROM marts.mart_sakr_bevak").fetch_df()
    top_employers = (df.groupby('vacancies', as_index=False)
                                ['vacancies'].sum()
                                .sort_values('vacancies',ascending=False).head(10))
    show_bar_chart(top_employers, "employer_name", 'vacancies', "Top 10 arbetsgivare inom Säkerhet och bevakning")

def show_experience_pie_chart(df):
    df_total = df.groupby('experience_required', as_index=False)['count'].sum()
    
    # Mappa true/false till tydliga etiketter
    mapping = {True: 'Erfarenhet krävs', False: 'Erfarenhet krävs ej', 'true': 'Erfarenhet krävs', 'false': 'Erfarenhet krävs ej'}
    df_total['experience_required'] = df_total['experience_required'].map(mapping)

    # Skapa pie chart
    fig = px.pie(df_total, names='experience_required', values='count',
                 title='Fördelning av erfarenhetskrav',
                 labels={'experience_required': 'Krav på erfarenhet'},
                 hover_data={'experience_required': True, 'count': True})

    # Hover-text och etiketter
    fig.update_traces(textinfo='percent+label', hovertemplate='<b>%{label}</b><br>Antal annonser: %{value}<extra></extra>')
    st.plotly_chart(fig)
