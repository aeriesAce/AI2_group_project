import streamlit as st
import plotly_express as px
import duckdb
import numpy as np
import pandas as pd
import pydeck as pdk
import json

con = duckdb.connect('jobs.duckdb')

def jobs_per_type():
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


# ------------------------------------------- om vi vill ha kanske, vet inte? sparar den här, för då kan vi göra om den nedanför så vi kan ha alla occpupations ----------------------
def sun_chart(data, path: list, value_col: str):
    if isinstance(data, str):
        df = con.execute(data).fetch_df()
    else:
        df = data

    fig = px.sunburst(
        df,
        path=path, 
        values=value_col,
        color=value_col,
        color_continuous_scale='ylgn',
        color_continuous_midpoint=np.average(df[value_col], weights=df[value_col])
    )

    st.plotly_chart(fig)

def line_chart(data:str, x:str, y:str):
    if isinstance(data, str):
        df = con.execute(data).fetch_df()
    else:
        df = data

    fig = px.line(df, 
                  x=x, 
                  y=y, 
                  markers = True,
                  labels={x: x.replace("_", " ").title(),
                        y: y.replace("_", " ").title()})
    st.plotly_chart(fig, theme = "streamlit")
    # ----------------------------------------------------- Generell funktion för charts -------------------------------------------------------------------------

def show_bar_chart(data: str, x: str, y: str):

    if isinstance(data, str):
        df = con.execute(data).fetch_df()
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
            feature["properties"]["value"] = int(match[value_col].sum())
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

def call_pydeck_chart(filtered_df):
    with open("Data/swedish_municipalities.geojson", encoding="utf-8") as f:
        geojson_data = json.load(f)
    st.title("Antal platser per kommun")
    pydeck_chart(
                geojson_data=geojson_data,
                df=filtered_df,
                match_col_geojson="kom_namn",         # geojson matchning
                match_col_df="municipality",      # matchar med municipality
                value_col="vacancies",
                use_normalized = True,
                tooltip_title="område",
                tooltip_field = "kom_namn"
            )

# ------------------------------------------------------ Pie chart som visar andel jobb som kräver erfarenhet och andel jobb som ej kräver det i procent
def show_experience_pie_chart(df):
    df_total = df.groupby('experience_required', as_index=False)['count'].sum()
    
    # Mappa true/false till tydliga etiketter
    mapping = {True: 'Erfarenhet krävs', False: 'Erfarenhet krävs ej', 'true': 'Erfarenhet krävs', 'false': 'Erfarenhet krävs ej'}
    df_total['experience_required'] = df_total['experience_required'].map(mapping)

    # Skapa pie chart
    fig = px.pie(df_total, names='experience_required', values='count',
                 labels={'experience_required': 'Krav på erfarenhet'},
                 hover_data={'experience_required': True, 'count': True})

    # Hover-text och etiketter
    fig.update_traces(textinfo='percent+label', hovertemplate='<b>%{label}</b><br>Antal annonser: %{value}<extra></extra>')
    
    # Gör pie charten större
    fig.update_layout(
        width=600,    # Anpassa bredden
        height=600,   # Anpassa höjden
        margin=dict(l=50, r=50, t=50, b=50)  # Anpassa marginalen
    )
    
    st.plotly_chart(fig)

def show_driving_license_required(df):
    df_total = df.groupby('driving_license', as_index=False)['count'].sum()

    mapping = {True: 'Körkort krävs', False: 'Körkort krävs ej', 'true': 'Körkort krävs', 'false': 'Körkort krävs ej'}
    df_total['driving_license'] = df_total['driving_license'].map(mapping)

    fig = px.pie(df_total, names='driving_license', values='count',
                 labels={'driving_license': 'Krav på erfarenhet'},
                 hover_data={'driving_license': True, 'count': True})

    fig.update_traces(textinfo='percent+label', hovertemplate='<b>%{label}</b><br>Antal annonser: %{value}<extra></extra>')

    fig.update_layout(
        width=600,   
        height=600,   
        margin=dict(l=50, r=50, t=50, b=50)  
    )

    st.plotly_chart(fig)
