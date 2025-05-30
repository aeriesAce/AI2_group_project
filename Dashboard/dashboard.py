import streamlit as st
import duckdb
from Dashboard.ui import show_columns, background_pic
from Dashboard.kpis import show_kpis
from config import occupation_map, dashboard_filters, reset_filters
from Dashboard.query import build_sql_query
from Dashboard.charts import show_bar_chart
background_pic("Dashboard/Media/Hr.png")
con = duckdb.connect("jobs.duckdb")
                              
category_choice = st.sidebar.radio("Välj yrkeskategori", list(occupation_map.keys()))
table = occupation_map[category_choice]
st.title(f"Annonser inom {category_choice}")
with st.container():
    col1, col2= st.columns([1, 2])
    with col1:
        st.subheader("Filtrera annonser")
        filters = dashboard_filters(table)
        st.button("Rensa filter", on_click=reset_filters)
        query = f"SELECT * FROM {table} {build_sql_query(filters)}"
        #st.code(query, language="sql") 
        filtered_df = con.execute(query).fetchdf()
    with col2:
        st.subheader("Annonser")
        show_columns(filtered_df)
        st.button("Egenskaper")

with st.container():
    st.subheader(f"Data inom {category_choice}")
    show_kpis(filtered_df)

with st.container():
    show_bar_chart(filtered_df, x="vacancies", y="municipality")

con.close()