import duckdb
import streamlit as st
import pandas as pd
from Dashboard.ui import show_columns, background_pic
from Dashboard.kpis import show_kpis
from config import occupation_map, dashboard_filters, reset_filters, filter_value, show_time_slider
from Dashboard.query import build_sql_query
from Dashboard.charts import show_bar_chart
from Dashboard.llm import call_Gemeni

background_pic("Dashboard/Media/Hr.png")

@st.cache_resource
def get_connection():
    return duckdb.connect("jobs.duckdb")

con = get_connection()
                              
category_choice = st.sidebar.radio("Välj yrkeskategori", list(occupation_map.keys()))
st.session_state["category_choice"] = category_choice
table = occupation_map[category_choice]

# to reset the filters when we change occupation_group
# st.session_state keeps old filters, so we reset them manually when the category changes
if "last_category_choice" not in st.session_state:
    st.session_state["last_category_choice"] = category_choice

if st.session_state["last_category_choice"] != category_choice:
    reset_filters()
    st.session_state["last_category_choice"] = category_choice

st.title(f"Annonser inom {category_choice}")
with st.container():
    col1, col2= st.columns([1, 2])
    with col1:
        st.subheader("Filtrera annonser")
        filters = dashboard_filters(con, table)
        st.button("Rensa filter", on_click=reset_filters)

        st.markdown("### Valda filter:")
        for key, value in filters.items():
            if value:
                key_pretty = key.replace("_", " ").title()
                st.markdown(f"- **{key_pretty}**: {filter_value(value)}")

        query = f"SELECT * FROM {table} {build_sql_query(filters)}"
        filtered_df = con.execute(query).fetchdf()
    with col2:
        st.subheader("Annonser")
        show_kpis(filtered_df)
        show_columns(filtered_df)
with st.container():
        call_Gemeni(filtered_df)