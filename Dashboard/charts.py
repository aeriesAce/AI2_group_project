import streamlit as st
import plotly_express as px
import duckdb
import numpy as np
import pandas as pd
con = duckdb.connect('jobs.duckdb')

# test bar chart with the kpis to run in main
def ads_per_occupation():
    df = con.execute("SELECT * FROM occupation.mart_tol").fetchdf()

    # use as_index=False to keep the group key (employer_name in this case) as a regular column
    # instead of an index, making it easier to access for visualization
    top_employers = df.groupby('employer_name', as_index=False)['number_of_vacancies'].sum().head(10)
    fig = px.bar(
        top_employers,
        x='employer_name',
        y='number_of_vacancies',
        labels={'employer_name': 'Arbetsgivare', 'number_of_vacancies': 'Antal platser'},
        title='Topp 10 arbetsgivare med flest antal platser inom Transport och Lager',
        color = 'number_of_vacancies',
        color_continuous_scale='blues'
    )

    st.plotly_chart(fig)

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