import streamlit as st
import duckdb
from Dashboard.ui import show_columns, background_pic
from Dashboard.kpis import show_kpis
from config import occupation_map, dashboard_filters, reset_filters
from Dashboard.query import build_sql_query
from Dashboard.llm import call_Gemeni
background_pic("Dashboard/Media/Hr.png")
con = duckdb.connect("jobs.duckdb")
                              
category_choice = st.sidebar.selectbox("Välj yrkeskategori", list(occupation_map.keys()))
table = occupation_map[category_choice]

st.button("Rensa filter", on_click=reset_filters)

filters = dashboard_filters(table)
query = f"SELECT * FROM {table} {build_sql_query(filters)}"
st.code(query, language="sql")
filtered_df = con.execute(query).fetchdf()

show_kpis(filtered_df)
show_columns(filtered_df)
call_Gemeni(filtered_df)

con.close()