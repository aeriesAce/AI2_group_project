# test kpi to try out the mart schemas
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

#def show_reg():
 
 # show_kpis(avgre1, avgre2 "Antal platser per region") ## lägga till denna som option istället för att visa hela tiden?
# ----------------------------------------- 

# Adding some more KPIS, seperating them for sanity


