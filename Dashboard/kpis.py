import streamlit as st
import duckdb
con = duckdb.connect('jobs.duckdb') 

def show_kpis(df):
    col1, col2, col3, col4 = st.columns(4)
    
    total_vacancies = df["vacancies"].sum()
    unique_employers = df["employer_name"].nunique()
    total_occupations = df["occupation_label"].nunique()
    latest_ad = df["publication_date"].max()
    latest_ad_str = latest_ad.strftime("%d/%m-%y")
    
    col1.metric("Totala lediga tjänster", total_vacancies)
    col2.metric("Antal arbetsgivare", unique_employers)
    col3.metric("Totala olika yrkesroller", total_occupations)
    col4.metric("Senaste annonsen", latest_ad_str)
