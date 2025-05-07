import streamlit as st
import plotly_express as px
import duckdb
import pandas as pd
con = duckdb.connect('jobs.duckdb')

# test bar chart with the kpis to run in main
def ads_per_occupation():
    df = con.execute("SELECT * FROM occupation.mart_transp_ditr_lager").fetchdf()

    # use as_index=False to keep the group key (employer_name in this case) as a regular column
    # instead of an index, making it easier to access for visualization
    top_employers = df.groupby('employer_name', as_index=False)['number_of_vacancies'].sum().head(10)
    fig = px.bar(
        top_employers,
        x='employer_name',
        y='number_of_vacancies',
        labels={'employer_name': 'Arbetsgivare', 'number_of_vacancies': 'Antal platser'},
        title='Topp 10 arbetsgivare med flest antal platser inom Transport och Lager'
    )

    st.plotly_chart(fig)

def test_ads_occu(start_date, end_date):
    df = con.execute("SELECT * FROM occupation.mart_transp_ditr_lager").fetchdf()
    st.write("DEBUG: Kolumner i tabellen:", df.columns.tolist())
    df["deadline"] = pd.to_datetime(df["deadline"])  # säkerställ rätt format

    # Filtrera på valt datumintervall
    df = df[(df["deadline"].dt.date >= start_date) & (df["deadline"].dt.date <= end_date)]
    # use as_index=False to keep the group key (employer_name in this case) as a regular column
    # instead of an index, making it easier to access for visualization
    top_employers = df.groupby('employer_name', as_index=False)['number_of_vacancies'].sum().head(10)
    fig = px.bar(
        top_employers,
        x='employer_name',
        y='number_of_vacancies',
        labels={'employer_name': 'Arbetsgivare', 'number_of_vacancies': 'Antal platser'},
        title=f'Topp 10 arbetsgivare med flest antal platser inom Transport och Lager ({start_date} - {end_date})'
    )

    st.plotly_chart(fig)