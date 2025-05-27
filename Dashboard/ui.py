import streamlit as st
import base64
#from Dashboard.dashboard import dashboard
from config import occupation_map, load_mart
from Dashboard.charts import show_bar_chart
from Dashboard.query import get_top_employers

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

# show specified columns in the dataframe
def show_columns(df):
    sort_df = df.sort_values(by= "vacancies", ascending= False)

    columns = ["municipality", "vacancies", "employer_name", "occupation_label", "employment_type"]
    st.dataframe(
        sort_df[columns],
        column_config={
            "vacancies": st.column_config.NumberColumn("Lediga tjänster"),
            "municipality": st.column_config.TextColumn("Kommun"),
            "employer_name": st.column_config.TextColumn("Arbetsgivare"),
            "occupation_label": st.column_config.TextColumn("Yrke"),
            "employment_type": st.column_config.TextColumn("Anställingstyp")
        },
        hide_index=True
    )

# creating pages for a more
def pages():
    pg = st.navigation([
        st.Page(homepage, title= "Hem"),
        st.Page("Dashboard/dashboard.py", title= ("Jobb")),
        st.Page(statistic_page, title= "Statistik")
    ])
    pg.run()

# a function to reset the search filters
def reset_filters():
    for key in [
        "occupation_group", "occupation_label", "region", "municipality",
        "experience_required", "driving_license"
    ]:
        st.session_state.pop(key, None)
    st.session_state.filters_reset = True  

# homepage, first page
def homepage():
    background_pic("Dashboard/Media/Hr.png")
    st.title("Välkommen, \n# Navigera genom att göra ett val i sidebaren till vänster")

# statistic chart page
def statistic_page():
    category_choice = st.sidebar.selectbox("Välj yrkeskategori", list(occupation_map.keys()))
    table = occupation_map.get(category_choice)
    df = load_mart(table)

    # diagram for the data
    st.subheader(f"Top 10 arbetsgivare inom {category_choice}")
    query = get_top_employers(category_choice)
    show_bar_chart(query, x="Företag", y="Lediga tjänster")

#def occupation_select():
 
 #   category_choice = st.sidebar.selectbox("Välj yrkeskategori", list(occupation_map.keys()))
  #  table = occupation_map.get(category_choice)
   # df = load_mart(table)