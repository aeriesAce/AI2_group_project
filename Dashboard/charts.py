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
    FROM marts.mart_anställningsvillkor
    GROUP BY job_type;
    """

    # Utför SQL-frågan och hämta resultatet
    data = pd.read_sql(query, con)
    con.close()

    # Visa resultatet i Streamlit
    st.title("Jobbstatistik baserat på anställningsvillkor")
    st.bar_chart(data.set_index('job_type'))

# ------------------------------ TEST KPI FÖR MAP CHART -----------------------------------
df = con.execute("""
    SELECT municipality, SUM(vacancies) AS vacancies
    FROM occupation.mart_pedagogik
    GROUP BY municipality
""").fetchdf()


# ------------------------------------------------------- En Generell funktion för suncharts --------------------------------------------------------------------
#def show_sunburst_chart(df: pd.DataFrame, path: list[str], value_col: str, title: str, color_scale='blues', top_n=8):
    #df_grouped = (
    #    df.groupby(path, as_index=False)[value_col]
   #     .sum()
  #      .sort_values(value_col, ascending=False)
 #       .head(top_n))
#
    #fig = px.sunburst(
    #    df_grouped,
    #    path=path,
    #    values=value_col,
    #    color=value_col,
    #    hover_data={value_col: True},
    #    color_continuous_scale=color_scale,
    #    color_continuous_midpoint=np.average(
    #        df_grouped[value_col],
    #        weights=df_grouped[value_col]))
    #fig.update_layout(title=title)

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

def show_bar_chart(query: str, x: str, y: str, title: str, color_scale = "edge"):
    df = con.execute(query).fetch_df()
    st.write(df.head())

    fig = px.bar(df, x=x, y=y, 
                labels={x: x.replace("_", " ").title(),
                        y: y.replace("_", " ").title()},
                title=title, 
                color=y, 
                color_continuous_scale= "edge")
    st.plotly_chart(fig)

    # ------------------------------------------------------- Generell funktion för PyDeck map chart --------------------------------------------------------------#

def pydeck_chart(geojson_data, df, match_col_geojson, match_col_df, value_col, use_normalized=True,color_scale_factor=255, tooltip_title="område", tooltip_field = "name", zoom=4):

    for feature in geojson_data["features"]:
        geo_name = feature["properties"][match_col_geojson]
        match = df[df[match_col_df] == geo_name]

        if not match.empty:
            feature["properties"]["value"] = int(match[value_col].values[0])
        else:
            feature["properties"]["value"] = 0
    
    if use_normalized:
        max_val = max([np.log1p(f["properties"]["value"]) for f in geojson_data["features"]])
        for f in geojson_data["features"]:
            val = f["properties"]["value"]
            log_val = np.log1p(val)
            f["properties"]["norm_value"] = log_val / max_val if max_val > 0 else 0
        else:
            for f in geojson_data["features"]:
                val = f["properties"]["value"]
                f["properties"]["color_val"] = val * color_scale_factor


    layer = pdk.Layer(
        "GeoJsonLayer",
        regions_geojson,
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




    
with open("Dashboard/swedish_regions.geojson", encoding="utf-8") as f:
    regions_geojson = json.load(f)



df = con.execute("""
    SELECT municipality, SUM(vacancies) AS vacancies
    FROM occupation.mart_sob
    GROUP BY municipality
""").fetchdf()         ####### denna ska bort sen då vi har en ovanför också. ska köra select box för dom olika alternativen.

# Visa kartan
st.title("Antal platser per kommun – Pedagogik")
pydeck_chart(
    geojson_data=regions_geojson,
    df=df,
    match_col_geojson="name",         # geojson matchning
    match_col_df="municipality",      # matchar med municipality
    value_col="vacancies",
    use_normalized = True,
    tooltip_title="Platser",
    tooltip_field = "name"
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