import streamlit as st
from Dashboard.charts import show_bar_chart, show_top_employers_pedagogik,show_top_employers_sob,show_top_employers_tdl, pydeck_chart

def pop_over():
    selected_occupation = 'Pedagogik'
    selected_occupation2 = 'Säkerhet och bevakning'
    selected_occupation3 = 'Transport och lager'
    popover = st.popover("Kategorier")
    pk = popover.checkbox("Visa Pedagogik", True)
    sob = popover.checkbox("Visa Säkerhet och Bevakning", True)
    tdl = popover.checkbox("Visa Transport och Lager", True)

    if pk:
        show_top_employers_pedagogik(selected_occupation)
    if sob:
        show_top_employers_sob(selected_occupation2)
    if tdl:
        show_top_employers_tdl(selected_occupation3)
   
    tab1, tab2 = st.tabs(["Diagram", "Test, tom"])

    with tab1:
        st.subheader("Ett stapeldiagram")
        show_bar_chart()
        pydeck_chart()

    with tab2:
        st.subheader("Tomt för test")
        st.write("#*Dance*")

pop_over()