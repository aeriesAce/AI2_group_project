import streamlit as st
import duckdb
from Dashboard.ui import show_columns, background_pic
from Dashboard.kpis import show_kpis
from config import occupation_map, dashboard_filters, reset_filters
from Dashboard.query import build_sql_query
from Dashboard.charts import show_bar_chart
from Dashboard.llm import call_Gemeni

background_pic("Dashboard/Media/Hr.png")

def load_filtered_data(query):
    with duckdb.connect("jobs.duckdb") as con:
        return con.execute(query).fetchdf()
    
# Use context manager - safe!
with duckdb.connect("jobs.duckdb") as con:
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
            filtered_df = load_filtered_data(query)
        with col2:
            st.subheader("Annonser")
            show_columns(filtered_df)

    with st.container():
        st.subheader(f"Vad vill du visa?")
        choice = st.radio("Välj ett alternativ", ["KPI", "Karta", "Analys"])

        show_kpis(filtered_df)
        if choice == "KPI":
            show_bar_chart(filtered_df, x="vacancies", y="municipality")

        # elif choice == "Karta":
        #     call_pydeck_chart(filtered_df)

        elif choice == "Analys":
            # ⚠️ If async, wrap it!
            # Example:
            # response = asyncio.run(call_Gemeni(filtered_df))  # Not safe in Streamlit!
            # Better: make a sync wrapper
            call_Gemeni(filtered_df)

    #with st.container():
