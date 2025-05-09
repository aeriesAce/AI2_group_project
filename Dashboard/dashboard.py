import streamlit as st
import duckdb
import pandas as pd

# Anslut till din DuckDB-fil
conn = duckdb.connect('jobs.duckdb')

# SQL-fråga för att få antalet jobb per job_type
query = """
SELECT job_type, COUNT(*) as count
FROM occupation.mart_anställningsvillkor_pedagogik
GROUP BY job_type;
"""

# Utför SQL-frågan och hämta resultatet
data = pd.read_sql(query, conn)
conn.close()

# Visa resultatet i Streamlit
st.title("Jobbstatistik baserat på anställningsvillkor")
st.bar_chart(data.set_index('job_type'))
