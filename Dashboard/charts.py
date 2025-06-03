import streamlit as st
import plotly_express as px
import duckdb
import pandas as pd
import pydeck as pdk
import numpy as np
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


def line_chart(data:str, x:str, y:str, color: str = None):
    if isinstance(data, str):
        df = con.execute(data).fetch_df()
    else:
        df = data

    fig = px.line(df, 
                  x=x, 
                  y=y, 
                  markers = True,
                  labels={x: x.replace("_", " ").title(),
                        y: y.replace("_", " ").title()},
                        color=color)
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

def pydeck_chart(geojson_data, df, match_col_geojson, match_col_df, value_col, tooltip_title="Annonser", zoom=4):
    # Preprocess df
    df[match_col_df] = (
    df[match_col_df]
    .astype(str)
    .str.replace(r"s? län$", "", regex=True)  # Tar bort "s län" eller " län"
    .str.replace(r"\s+", " ", regex=True)     # Tar bort dubbla mellanslag
    .str.strip()
    .str.lower()
)
    for feature in geojson_data["features"]:
        geo_name = feature["properties"].get(match_col_geojson, "").strip().lower()
        match = df[df[match_col_df] == geo_name]
        value = int(match[value_col].sum()) if not match.empty else 0
        feature["properties"]["value"] = value

    max_value = max([feature["properties"]["value"] for feature in geojson_data["features"]])
    if max_value == 0:
        max_value = 1

        # Skapa GeoJsonLayer med extrusion
    layer = pdk.Layer(
        "GeoJsonLayer",
        geojson_data,
        stroked=True,
        filled=True,
        extruded=True,
        elevation_scale=40,
        get_fill_color = "[255, 255, 255, 180]",
        get_line_color=[0, 255, 0],
        pickable=True,
        auto_highlight=True,
        highlight_color=[100, 0, 150, 200],
    )

    view_state = pdk.ViewState(
        latitude=60.1282,
        longitude=18.6435,
        zoom=zoom,
        pitch=45,
    )
    tooltip = {"html": "<b>{name}</b><br/>" + tooltip_title + ": {value}", "style": {"color": "white"}}

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        tooltip=tooltip
    )

    st.pydeck_chart(deck)


def call_pydeck_chart(filtered_df):
    with open("Data/swedish_regions.geojson", encoding="utf-8") as f:
        geojson_data = json.load(f)
    st.title("Antal annonser per län")
    pydeck_chart(
                geojson_data=geojson_data,
                df=filtered_df,
                match_col_geojson="name",         # geojson matchning
                match_col_df="region",      # matchar med region
                value_col="vacancies",
                tooltip_title="Annonser",
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
                 hover_data={'experience_required': True, 'count': True},
                color_discrete_sequence = px.colors.sequential.YlGn[-2:])

    # Hover-text och etiketter
    fig.update_traces(textinfo='percent+label', hovertemplate='<b>%{label}</b><br>Antal annonser: %{value}<extra></extra>')
    
    st.plotly_chart(fig)

def show_driving_license_required(df):
    df_total = df.groupby('driving_license', as_index=False)['count'].sum()

    mapping = {True: 'Körkort krävs', False: 'Körkort krävs ej', 'true': 'Körkort krävs', 'false': 'Körkort krävs ej'}
    df_total['driving_license'] = df_total['driving_license'].map(mapping)

    fig = px.pie(df_total, names='driving_license', values='count',
                 labels={'driving_license': 'Krav på erfarenhet'},
                 hover_data={'driving_license': True, 'count': True},
                 color_discrete_sequence = px.colors.sequential.YlGn[-2:])

    fig.update_traces(textinfo='percent+label', hovertemplate='<b>%{label}</b><br>Antal annonser: %{value}<extra></extra>')

    st.plotly_chart(fig)

