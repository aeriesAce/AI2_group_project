import streamlit as st
import plotly_express as px
import duckdb
import numpy as np
import pandas as pd
con = duckdb.connect('jobs.duckdb')

def jobs_per_type():
    # SQL-fråga för att få antalet jobb per job_type
    query = """
    SELECT job_type, COUNT(*) as count
    FROM occupation.mart_anställningsvillkor_pedagogik
    GROUP BY job_type;
    """

    # Utför SQL-frågan och hämta resultatet
    data = pd.read_sql(query, con)
    con.close()

    # Visa resultatet i Streamlit
    st.title("Jobbstatistik baserat på anställningsvillkor")
    st.bar_chart(data.set_index('job_type'))

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
def sun_chart():
    df = con.execute("SELECT * FROM occupation.mart_tol").fetch_df()

    top_employers = df.groupby(['employer_name', 'region', 'municipality'], as_index=False)['number_of_vacancies'].sum().head(8)
    fig = px.sunburst(
        top_employers,
        path =['employer_name', 'number_of_vacancies'],
        values = 'number_of_vacancies',
        color = 'number_of_vacancies', 
        hover_data={'number_of_vacancies': True},
        color_continuous_scale='blues',
        color_continuous_midpoint=np.average(df['number_of_vacancies'], weights=df['number_of_vacancies'])
    )

    st.plotly_chart(fig)



    # ----------------------------------------------------- Generell funktion för charts -------------------------------------------------------------------------

def show_bar_chart(df: pd.DataFrame, x: str, y: str, title: str, color_scale = "edge"):
    fig = px.bar(df, x=x, y=y, 
                labels={x: x.replace("_", " ").title(),
                        y: y.replace("_", " ").title()},
                title=title, color= y, color_continuous_scale= color_scale)
    st.plotly_chart(fig)

    # ------------------------------------------------------ Top 10 inom lager vi stoppar in i den generella funktionen -----------------------------------------------

def show_top_employers_tdl():
    df = con.execute("SELECT * FROM occupation.mart_tol").fetch_df()
    top_employers = (df.groupby("employer_name", as_index=False)
                                ["number_of_vacancies"].sum()
                                .sort_values("number_of_vacancies",ascending=False).head(10))
    show_bar_chart(top_employers, "employer_name", "number_of_vacancies", "Top 10 arbetsgivare inom Transport och Lager")

# ------------------------------------------------------ Top 10 inom pedagogik vi stoppar in i den generella funktionen -----------------------------------------------

def show_top_employers_pedagogik():
    df = con.execute("SELECT * FROM occupation.mart_pedagogik").fetch_df()
    top_employers = (df.groupby("employer_name", as_index=False)
                                ["number_of_vacancies"].sum()
                                .sort_values("number_of_vacancies",ascending=False).head(10))
    show_bar_chart(top_employers, "employer_name", "number_of_vacancies", "Top 10 arbetsgivare inom Pedagogik")

# ------------------------------------------------------ Top 10 inom säkerhet och bevakning vi stoppar in i den generella funktionen -----------------------------------------------

def show_top_employers_sob():
    df = con.execute("SELECT * FROM occupation.mart_sob").fetch_df()
    top_employers = (df.groupby("employer_name", as_index=False)
                                ["number_of_vacancies"].sum()
                                .sort_values("number_of_vacancies",ascending=False).head(10))
    show_bar_chart(top_employers, "employer_name", "number_of_vacancies", "Top 10 arbetsgivare inom Säkerhet och bevakning")