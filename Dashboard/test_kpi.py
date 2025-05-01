# test kpi to try out the mart schemas
import streamlit as st
import duckdb
import pandas as pd
con = duckdb.connect("jobs.duckdb")

st.title("Test-KPI for the tre occupation fields")


# function to show a KPI per field
def show_kpis(df: pd.DataFrame, title: str):
    st.subheader(f"{title}")
    
    total_ads = df['job_id'].nunique()
    avg_vacancies = df['number_of_vacancies'].mean()

    st.metric("Totalt antal annonser", total_ads)
    st.metric("Snitt antal platser", f"{avg_vacancies:.1f}")

# Pedagogik

df_ped = con.execute("SELECT * FROM occupation.mart_pedagogik").fetchdf()
st.write("Rader i df_ped:", len(df_ped))
st.dataframe(df_ped.head())

show_kpis(df_ped, "Pedagogik")

# Säkerhet och Bevakning
df_sb = con.execute("SELECT * FROM occupation.mart_säker_bevak").fetchdf()
show_kpis(df_sb, "Säkerhet och Bevakning")

# Transport, Distrubition och Lager
df_sak = con.execute("SELECT * FROM occupation.mart_transp_ditr_lager").fetchdf()
show_kpis(df_sak, "Transport, Distrubition och Lager")


