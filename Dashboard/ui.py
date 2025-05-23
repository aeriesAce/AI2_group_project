import streamlit as st
import duckdb
import base64
import plotly_express as px
from config import occupation_map, load_mart
from Dashboard.kpis import show_kpis

con = duckdb.connect('jobs.duckdb')
def background_pic(image):
    with open(image, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def dashboard():
    background_pic("Dashboard/Media/Hr.png")
    st.title("HR Dashboard per kategori")

    # choosing a category
    category_choice = st.sidebar.selectbox("Välj yrkeskategori", list(occupation_map.keys()))
    table = occupation_map.get(category_choice)
    df = load_mart(table)

    # to filter the categories we want
    st.sidebar.header("Filter")
    occupation_group = st.sidebar.multiselect("Välj yrkesgrupp", sorted(df["occupation_group"].dropna().unique()))
    region = st.sidebar.multiselect("Välj kommun", sorted(df["region"].dropna().unique()))

    filtered_df = df.copy()
    if occupation_group:
        filtered_df = filtered_df[filtered_df["occupation_group"].isin(occupation_group)]
    if region:
        filtered_df = filtered_df[filtered_df["region"].isin(region)]

    st.markdown(f"Statistik för {category_choice}")
    show_kpis(filtered_df)

    # diagram for the data
    st.subheader("Annonser per kommun")
    if not filtered_df.empty:
        plot_df = (
            filtered_df.groupby("region")
            .size()
            .reset_index(name="Antal")
            .sort_values("Antal", ascending=False)
        )
        fig = px.bar(plot_df, x="region", y="Antal", title="Antal annonser per kommun")
        st.plotly_chart(fig)
    else:
        st.info("Ingen data att visa. Ändra filtren för att se resultat.")
    
