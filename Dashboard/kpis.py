import streamlit as st 

def show_kpis(df):
    col1, col2, col3 = st.columns(3)
    
    total_vacancies = df["vacancies"].sum()
    total_regions = df["municipality"].nunique()
    top_occupation = (
    df.groupby("occupation_label")["vacancies"]
    .sum()
    .sort_values(ascending=False)
    .head(1)
)
    name = top_occupation.index[0]
    
    col1.metric("Totala lediga tjänster", total_vacancies)
    col2.metric("Kommuner med lediga tjänster", total_regions)
    col3.metric("Mest eftersökta tjänsten", name)
