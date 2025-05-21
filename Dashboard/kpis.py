import streamlit as st 

def show_kpis(df):
    col1, col2, col3 = st.columns(3)
    
    total_vacancies = df["vacancies"].sum()
    unique_regions = df["municipality"].nunique()
    most_common_type = df["employment_type"].mode().iloc[0] if not df["employment_type"].empty else "Ej tillgängligt"
    
    col1.metric("Lediga tjänster", total_vacancies)
    col2.metric("Kommuner", unique_regions)
    col3.metric("Populär anställningsform", most_common_type)