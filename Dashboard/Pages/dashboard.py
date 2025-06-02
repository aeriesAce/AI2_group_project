import duckdb
import streamlit as st
from Dashboard.ui import show_columns, background_pic, sunburst_choice
from Dashboard.kpis import show_kpis
from config import occupation_map, dashboard_filters, reset_filters
from Dashboard.query import build_sql_query, trend_time
from Dashboard.llm import call_Gemeni
from Dashboard.charts import line_chart

background_pic("Dashboard/Media/Hr.png")

con = duckdb.connect("jobs.duckdb")
                              
category_choice = st.sidebar.radio("Välj yrkeskategori", list(occupation_map.keys()))
st.session_state["category_choice"] = category_choice
table = occupation_map[category_choice]
st.title(f"Annonser inom {category_choice}")
with st.container():
    col1, col2= st.columns([1, 2])
    with col1:
        st.subheader("Filtrera annonser")
        filters = dashboard_filters(table)
        st.button("Rensa filter", on_click=reset_filters)

        st.markdown("### Valda filter:")
        for key, value in filters.items():
            if value:
                key_pretty = key.replace("_", " ").title()
                st.markdown(f"- **{key_pretty}**: {', '.join([str(v) for v in value])}")

        query = f"SELECT * FROM {table} {build_sql_query(filters)}"
        filtered_df = con.execute(query).fetchdf()
    with col2:
        st.subheader("Annonser")
        show_kpis(filtered_df)
        show_columns(filtered_df)

with st.container():
    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown("## Analysera annonserna")
        call_Gemeni(filtered_df)
    with col2:
        #sunburst_choice(filtered_df, path=[path_choice], value_col= 'Lediga tjänster')
        query = trend_time()
        df_trend = con.execute(query).fetchdf()
        line_chart(df_trend, x="datum", y="Antal annonser")
