# test kpi to try out the mart schemas
import streamlit as st
import duckdb
import pandas as pd
import math
con = duckdb.connect("jobs.duckdb")

st.title("Test-KPI for the tre occupation fields")


# function to show a KPI per field
def show_kpis(df: pd.DataFrame, title: str):
    st.subheader(f"{title}")
    
    total_ads = df['job_id'].nunique()
    avg_vacancies = df["number_of_vacancies"].mean()
    avg_region = (df.groupby('region')['number_of_vacancies'].sum().reset_index().sort_values(by = 'number_of_vacancies', ascending=False))

    st.metric("Totalt antal annonser", total_ads)
    st.metric("Snitt antal platser", math.floor(avg_vacancies))

    st.subheader("Antal platser per region")
    st.dataframe(avg_region)

# Pedagogik

df_ped = con.execute("SELECT * FROM occupation.mart_pedagogik").fetchdf()
show_kpis(df_ped, "Pedagogik")

# Säkerhet och Bevakning
df_sob = con.execute("SELECT * FROM occupation.mart_säker_bevak").fetchdf()
show_kpis(df_sob, "Säkerhet och Bevakning")

# Transport, Distrubition och Lager
df_tdl = con.execute("SELECT * FROM occupation.mart_transp_ditr_lager").fetchdf()
show_kpis(df_tdl, "Transport, Distrubition och Lager")

#df_reg = con.execute("SELECT 'region' FROM occupation.mart_pedagogik").fetchdf()
#show_kpis(df_reg, "awdawd")

# ----------------------------------------- 

# Adding some more KPIS, seperating them for sanity

st.title = "Amount of jobs per region"

#def show_amount_per_region(df: pd.DataFrame, title: str):
 #   st.subheader(f"{title}")
    
   # region_df = df_ped.groupby(['number'].sum()
  #  avg_vacancies = df['number_of_vacancies'].mean()

   # st.metric("Totalt antal annonser per region", total_ads)
    #st.metric("Snitt antal platser per region", f"{avg_vacancies:.1f}")
