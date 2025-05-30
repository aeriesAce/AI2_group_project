import streamlit as st
import base64
from Dashboard.query import get_top_employers, get_experience_distribution
from Dashboard.charts import show_bar_chart, show_experience_pie_chart
from Dashboard.llm import call_Gemeni
from config import occupation_map

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


# homepage, first page
def homepage():
    st.set_page_config(page_title="HR Dashboard", layout="wide")
    background_pic("Dashboard/Media/Hr.png")
    st.title("Välkommen, \n# Navigera genom att göra ett val i sidebaren till vänster")

# statistic chart page
def statistic_page():
    background_pic("Dashboard/Media/Hr.png")
    category_choice = st.sidebar.radio("Välj yrkeskategori", list(occupation_map.keys()))

    # diagram for the data
    st.subheader(f"Top 10 arbetsgivare inom {category_choice}")
    query = get_top_employers(category_choice)
    show_bar_chart(query, x="Företag", y="Lediga tjänster")
    
    # Pie chart för erfarenhetskrav i vald kategori
    st.subheader(f"Fördelning av erfarenhetskrav inom {category_choice}")
    df_exp = get_experience_distribution(category_choice)
    show_experience_pie_chart(df_exp)
    

# creating pages for a more website feeling
def pages():
    pages = {
    "Hemskärm": [
        st.Page(homepage, title= "Hem")
    ],
        "Yrkeskategorier": [
            st.Page("Dashboard/dashboard.py", title= "Annonser"),
            st.Page(statistic_page, title= "Trender")
        ]
    }
    pg = st.navigation(pages)
    pg.run()
