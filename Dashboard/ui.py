import streamlit as st
import base64

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

# creating pages for a more website feeling
def pages():
    pages = {
    "Hemskärm": [
        st.Page("Dashboard/Pages/homepage.py", title= "Hem")
    ],
        "Yrkeskategorier & statistik": [
            st.Page("Dashboard/Pages/dashboard.py", title= "Annonser"),
            st.Page("Dashboard/Pages/statistic_page.py", title= "Statistik"),
            st.Page("Dashboard/Pages/chart_page.py", title= "Karta")
        ]
    }
    pg = st.navigation(pages)
    pg.run()

