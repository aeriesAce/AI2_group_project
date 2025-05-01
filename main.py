import streamlit as st
import duckdb
import pandas as pd
from Dashboard.dashboard import set_bg_pic
from dbt_groupp.models.mart import mart_pedagogik, mart_säker_bevak, mart_transp_ditr_lager
con = duckdb.connect('jobs.duckdb')

#set_bg_pic('./Media/forest.png') 