import streamlit as st
import duckdb
#from Dashboard.dashboard import set_bg_pic
from Dashboard.charts import ads_per_occupation

#set_bg_pic('./Media/forest.png') 
ads_per_occupation()