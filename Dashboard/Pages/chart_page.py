import streamlit as st
import duckdb
import pandas as pd
from Dashboard.ui import background_pic
from config import occupation_map, show_time_slider
from Dashboard.charts import call_pydeck_chart, show_bar_chart
background_pic("Dashboard/Media/Hr.png")

@st.cache_resource
def get_connection():
    return duckdb.connect("jobs.duckdb")

con = get_connection()

category_choice = st.sidebar.radio("Välj yrkeskategori", list(occupation_map.keys()))
table = occupation_map[category_choice]
query = f"SELECT * FROM {table}"
filtered_df = con.execute(query).fetchdf()

with st.container():
        call_pydeck_chart(filtered_df)
with st.container():
    st.markdown("## Antal utlagda tjänster per företag \n(Under en viss tidsperiod)")

    start_date, end_date = show_time_slider(filtered_df)
    st.markdown(
    f"**Filtrerar tjänster från {start_date.strftime('%Y-%m-%d')} till {end_date.strftime('%Y-%m-%d')}**")

    df_filtered_time = filtered_df[
            (filtered_df["publication_date"] >= pd.to_datetime(start_date)) &
            (filtered_df["publication_date"] <= pd.to_datetime(end_date))
        ]

    df_filtered_time = df_filtered_time.copy()
    df_filtered_time["employer_name"] = df_filtered_time["employer_name"].str.strip()

    show_all = st.checkbox("Visa alla företag", value=True)

    if show_all:
            df_trend = df_filtered_time
    else:
            top_n = st.slider("Välj företagen med flest tjänster", min_value=1, max_value=25, value=10)
            top_employers = df_filtered_time["employer_name"].value_counts().nlargest(top_n).index.tolist()
            df_trend = df_filtered_time[df_filtered_time["employer_name"].isin(top_employers)]

    df_grouped = df_trend.groupby("employer_name").size().reset_index(name="Lediga tjänster")
    df_grouped = df_grouped.rename(columns={"employer_name": "Företag"})

    if df_grouped.empty:
        st.warning("Inga annonser hittades för vald period.")
    else:
        show_bar_chart(df_grouped, x="Lediga tjänster", y="Företag")
    