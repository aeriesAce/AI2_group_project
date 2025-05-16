import streamlit as st
import duckdb
import pandas as pd
con = duckdb.connect("jobs.duckdb")

# function to show a KPI per field
def show_kpis(df: pd.DataFrame, title: str):
    st.subheader(f"{title}")

    total_ads = df['job_id'].nunique()
    avg_vacancies = round(df["number_of_vacancies"].median(), 1)
    avg_region = (df.dropna(subset=['region'])
                  .groupby('region', as_index = False )['number_of_vacancies']
                  .sum()
                  .sort_values(by='number_of_vacancies', ascending = False))

    st.metric("Totalt antal annonser", total_ads)
    st.metric("Snitt antal platser per annons", avg_vacancies)

    st.subheader("Antal platser per region")
    st.dataframe(avg_region)

# Pedagogik
def show_pk():
    df_ped = con.execute("SELECT * FROM occupation.mart_pedagogik").fetchdf()
    show_kpis(df_ped, "Pedagogik")

# Säkerhet och Bevakning
def show_sob():
  df_sob = con.execute("SELECT * FROM occupation.mart_sob").fetchdf()
  show_kpis(df_sob, "Säkerhet och Bevakning")

# Transport, Distrubition och Lager
def show_tdl():
  df_tdl = con.execute("SELECT * FROM occupation.mart_tol").fetchdf()
  show_kpis(df_tdl, "Transport, Distrubition och Lager")

def get_jobs_per_city():
    query = """
        SELECT occupation_category, 
        region, 
        municipality, 
        "Totala jobb"
        FROM marts.mart_jobs_per_city
        """
    return con.execute(query).fetchdf()

def get_vacant_jobs_per_occ():
    query = """
        SELECT occupation_category, 
            Yrke, 
            "Totala jobb"
        FROM marts.mart_jobs_per_occ
        """
    return con.execute(query).fetchdf()

def get_form_of_employement():
    query = """
        SELECT conditions, 
            occupation_category, 
            region, 
            municipality, 
            number_of_vacancies
        FROM marts.mart_anställningsvillkor
        """
    return con.execute(query).fetchdf()

def get_most_sought_occ():
    query = """
        SELECT "Län", 
           "Stad", 
            occupation_category, 
            "Anställningsform"
        FROM marts.mart_most_sought_occ
        """
    return con.execute(query).fetchdf()

def get_jobs_over_time():
    query = """
        SELECT
            "month",
            "quarter",
            "year",
            occupation_group,
            occupation_category,
            "Totala jobb",
        FROM marts.mart_active_jobs
        GROUP BY "month", "quarter", "year", "Totala jobb", occupation_group, occupation_category
    """
    return con.execute(query).fetchdf()