import streamlit as st
from Dashboard.ui import background_pic

st.set_page_config(page_title="HR Dashboard", layout="wide")
background_pic("Dashboard/Media/Hr.png")
st.title("Välkommen, \n# Navigera genom att göra ett val i sidebaren till vänster")
st.image("Dashboard/Media/HR_pic.png")