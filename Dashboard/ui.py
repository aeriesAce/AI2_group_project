import streamlit as st
import base64
from Tests.test_kpi import show_tdl, show_pk, show_sob
from Dashboard.charts import ads_per_occupation

  # parameter set to _ only for testing
def set_sidebar(_):
    add_selectbox = st.sidebar.selectbox(
        "Choices",
        [
            "Occupation",
            "Chart"
        ]
    )
    selected_value = None 
    
    with st.sidebar:
        if add_selectbox == "Occupation":
            occupation_option = ["Pedagogik", "Transport & Lager", "Säkerhet & Bevakning"]
            selected_value = st.radio("Choose an occupation", occupation_option)
        elif add_selectbox == "Chart":
            chart_option = "Chart"
            selected_value = st.radio("Choose a chart to show", chart_option)
    return add_selectbox, selected_value

def sidebar_choices(choice):
    if choice is None:
        st.info("Välj ett alternativ i sidopanelen.")
        return
    if choice == "Pedagogik":
        st.markdown("Totalt antal annonser för Pedagogik")
        show_pk()
    elif choice == "Säkerhet & Bevakning":
        st.markdown("Totalt antal annonser för Säkerhet & Bevakning")
        show_sob()
    elif choice == "Transport & Lager":
        st.markdown("Totalt antal annonser för Transport & Lager")
        show_tdl()
    elif choice in ["Chart", "Charts"]:
        st.markdown("Bar chart for ads per occupation in Transport & Lager")
        ads_per_occupation()