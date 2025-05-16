import streamlit as st
from Dashboard.kpis import show_kpis
from Dashboard.charts import show_bar_chart

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
            occupation_option = ["Pedagogik", "Säkerhet och bevakning", "Transport och lager"]
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
        show_kpis(choice)
    elif choice == "Säkerhet och bevakning":
        st.markdown("Totalt antal annonser för Säkerhet & Bevakning")
        show_kpis(choice)
    elif choice == "Transport och lager":
        st.markdown("Totalt antal annonser för Transport & Lager")
        show_kpis(choice)
    elif choice in ["Chart", "Charts"]:
        st.markdown("Bar chart for ads per occupation in Transport & Lager")
        show_bar_chart()