import streamlit as st
import base64
from Dashboard.charts import sun_chart

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
        "Yrkeskategorier": [
            st.Page("Dashboard/Pages/dashboard.py", title= "Annonser"),
            st.Page("Dashboard/Pages/statistic_page.py", title= "Trender")
        ]
    }
    pg = st.navigation(pages)
    pg.run()

def sunburst_choice(df):
    path_choice = st.multiselect(
    "Välj nivåer för sunburst:",
    options=['occupation_category', 'occupation_group', 'occupation_label',
             'region', 'municipality', 'employer_name',
             'employment_type', 'duration', 'experience_required', 'driving_license'],
    default=['occupation_category', 'occupation_group', 'occupation_label']
)

    if path_choice:
        sun_chart(df, path=path_choice, value_col='Lediga tjänster')

