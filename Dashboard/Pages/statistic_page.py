import streamlit as st
from Dashboard.ui import background_pic
from Dashboard.query import get_top_employers, get_experience_distribution, get_driving_license_requierd, get_top_titles
from Dashboard.charts import show_experience_pie_chart, show_bar_chart, show_driving_license_required, sun_chart
from config import occupation_map
background_pic("Dashboard/Media/Hr.png")
category_choice = st.sidebar.radio("Välj yrkeskategori", list(occupation_map.keys()))
col1, col2 = st.columns(2)
with col1:
    # diagram for the data
    st.subheader(f"Top 10 arbetsgivare inom {category_choice}")
    query = get_top_employers(category_choice)
    show_bar_chart(query, x="Företag", y="Lediga tjänster")

with col2:
    st.subheader(f"10 högst sökta titlarna inom {category_choice}")
    query = get_top_titles(category_choice)
    show_bar_chart(query, x="Titlar", y= 'Lediga tjänster')
    
# Pie chart för erfarenhetskrav i vald kategori
st.subheader(f"Fördelning av krav inom {category_choice}")
col1, col2 = st.columns(2)

with col1:
    df_exp = get_experience_distribution(category_choice)
    show_experience_pie_chart(df_exp)

with col2:
    df_dl = get_driving_license_requierd(category_choice)
    show_driving_license_required(df_dl)