import streamlit as st
from Dashboard.test_kpi import show_tdl, show_pk, show_sob, show_reg
from Dashboard.charts import ads_per_occupation

def pop_over():
    
    popover = st.popover("Kategorier")
    pk = popover.checkbox("Visa Pedagogik", True)
    sob = popover.checkbox("Visa Säkerhet och Bevakning", True)
    tdl = popover.checkbox("Visa Transport och Lager", True)
    reg = popover.checkbox("Visa annonser per region", True)

    if pk:
        show_pk()
    if sob:
        show_sob()
    if tdl:
        show_tdl()
    if reg:
        show_reg()

    tab1, tab2 = st.tabs(["Diagram", "Test, tom"])

    with tab1:
        st.subheader("Ett stapeldiagram")
        ads_per_occupation()

    with tab2:
        st.subheader("Tomt för test")
        st.write("#*Dance*")