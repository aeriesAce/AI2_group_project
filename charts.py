import streamlit as st
import plotly_express as px
from Dashboard.test_kpi import show_kpis
import duckdb
con = duckdb.connect('jobs.duckdb')

# test bar chart with the kpis to run in main
def ads_per_occupation():
    df = con.execute("""
        SELECT job_id, employer_id, number_of_vacancies
        FROM occupation.mart_transp_ditr_lager
    """).fetchdf()

    show_kpis(df, "Översikt")
    top_employers = df.groupby('employer_id')['number_of_vacancies'].sum().reset_index()
    fig = px.bar(
        top_employers,
        x='employer_id',
        y='number_of_vacancies',
        labels={'employer_id': 'Arbetsgivare', 'number_of_vacancies': 'Antal platser'},
        title='Topp 10 arbetsgivare med flest antal platser'
    )

    st.plotly_chart(fig)