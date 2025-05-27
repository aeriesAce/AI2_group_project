import streamlit as st
from Dashboard.ui import show_columns, reset_filters
from Dashboard.kpis import show_kpis
from config import load_mart, occupation_map
from Dashboard.sql_builder import build_sql_query
import duckdb

    #background_pic("Dashboard/Media/Hr.png")
con = duckdb.connect("jobs.duckdb")
   
                                 
    # choosing a category
category_choice = st.sidebar.selectbox("Välj yrkeskategori", list(occupation_map.keys()))
table = occupation_map.get(category_choice)
df = load_mart(table)
    

    # setting to visually change boolean true to string ja and false to nej
yn = [("Ja", True), ("Nej", False)]

with st.expander("Filtrera data", expanded=True):
    if st.session_state.get("filters_reset"):
       st.session_state.filters_reset = False
       st.rerun()

        # a button to reset the filters by using the reset_filters function
    st.button("Rensa filter", on_click= reset_filters)
    col1, col2, col3 = st.columns(3)

    # filters the occupation_labels after occupation_group
with col1:
                               # default = st.session_state.get("CHOICE", []) sets the multiselect to its default state by retrieving the saved value or showing an empty list after reset
    occup_group = st.multiselect("Yrkesgrupp", sorted(df["occupation_group"].dropna().unique()), default=st.session_state.get("occupation_group", []), key="occupation_group")
    if occup_group:
        filtered_o_label = df[df["occupation_group"].isin(occup_group)]["occupation_label"].dropna().unique()
    else:
        filtered_o_label = df["occupation_label"].dropna().unique()
    occup_label = st.multiselect("Yrke", sorted(filtered_o_label), default=st.session_state.get("occupation_label", []), key= "occupation_label")

    duration_t = st.multiselect("Varaktighet", sorted(df["duration"].dropna().unique()), default=st.session_state.get("duration", []), key= "duration")


    # filter the municipalitys after region
with col2:
    region = st.multiselect("Län", sorted(df["region"].dropna().unique()), default=st.session_state.get("region", []), key="region")
    if region:
        filtered_munic = df[df["region"].isin(region)]["municipality"].dropna().unique()
    else:
         filtered_munic = df["municipality"].dropna().unique()
    munic = st.multiselect("Kommun", sorted(filtered_munic), default=st.session_state.get("municipality", []), key= "municipality")

with col3:
        # shows "Ja" & "Nej" labels for boolean values in the ui, goes back to True & False for filtering
        exp_require = st.multiselect("Erfarenhet", options= yn, format_func=lambda x: x[0], default=st.session_state.get("experience_required", []), key= "experience_required")
        exp_require = [val[1] for val in exp_require]

        d_license = st.multiselect("Körkort", options= yn, format_func=lambda x: x[0], default=st.session_state.get("driving_license", []), key= "driving_license")
        d_license = [val[1] for val in d_license]
  
    # to filter the categories we want
filters = {
        "occupation_group": occup_group,
        "occupation_label": occup_label,
        "duration": duration_t,
        "region": region,
        "municipality": munic,
        "experience_required": exp_require,
        "driving_license": d_license
    }
# using the sql_builder to check if it works with the filters.
use_sql = st.toggle("Visa SQL-Query istället för DF", value=False)
if use_sql:
        where_clause = build_sql_query(filters)
        query = f"SELECT * FROM {table} {where_clause}"
        st.code(query, language="sql")
        filtered_df = con.execute(query).fetchdf()
else:
    # creates a copy of the dataframe to use with the filters
        filtered_df = df.copy()
        for col, selected_values in filters.items():
            if selected_values:
                filtered_df = filtered_df[filtered_df[col].isin(selected_values)]
    

show_kpis(filtered_df)
show_columns(filtered_df)
con.close()