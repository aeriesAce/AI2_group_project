import streamlit as st
import pandas as pd

# here I map each occupation category to its mart table to load data dynamically
# its used to filter and load data based on the selected occupation in the dashboard
occupation_map = {
    "Pedagogik": "marts.mart_pedagogik",
    "Säkerhet och bevakning": "marts.mart_sakr_bevak",
    "Transport och lager": "marts.mart_tran_lager"
}

# a function to reset the search filters
def reset_filters():
    for key in [
        "occupation_group", "occupation_label", "region", "municipality",
        "experience_required", "driving_license", "duration"
    ]:
        st.session_state.pop(key, None)
    st.session_state.filters_reset = True  

def dashboard_filters(con, table):
    # setting to visually change boolean true to string ja and false to nej
    yn = [("Ja", True), ("Nej", False)]

    col1, col2, col3 = st.columns(3)
    with st.expander("Filtrera data", expanded=True):
        with col1:
            # filters the occupation_labels after occupation_group
            occup_groups = con.execute(f"""
                SELECT DISTINCT occupation_group 
                FROM {table} 
                WHERE occupation_group IS NOT NULL 
                ORDER BY occupation_group
            """).fetchdf()["occupation_group"].tolist()
                                                    # default = st.session_state.get("CHOICE", []) sets the multiselect to its default state by retrieving the saved value or showing an empty list after reset
            occup_group = st.multiselect("Yrkesgrupp", occup_groups, default=st.session_state.get("occupation_group", []), key="occupation_group")

            #  I fetch occupation labels filtered by selected groups
            occup_label_filter = f"WHERE occupation_label IS NOT NULL"
            if occup_group:
                occup_label_filter += f" AND occupation_group IN ({','.join([f'\'{x}\'' for x in occup_group])})"

            occup_labels = con.execute(f"""
                SELECT DISTINCT occupation_label 
                FROM {table} 
                {occup_label_filter} 
                ORDER BY occupation_label
            """).fetchdf()["occupation_label"].tolist()

            occup_label = st.multiselect("Yrke", occup_labels, default=st.session_state.get("occupation_label", []), key="occupation_label")

            # duration
            durations = con.execute(f"""
                SELECT DISTINCT duration 
                FROM {table} 
                WHERE duration IS NOT NULL 
                ORDER BY duration
            """).fetchdf()["duration"].tolist()

            duration = st.multiselect("Varaktighet", durations, default=st.session_state.get("duration", []), key="duration")

        # filter the municipalitys after region
        with col2:
            regions = con.execute(f"""
                SELECT DISTINCT region 
                FROM {table} 
                WHERE region IS NOT NULL 
                ORDER BY region
            """).fetchdf()["region"].tolist()

            region = st.multiselect("Län", regions, default=st.session_state.get("region", []), key="region")

            muni_filter = f"WHERE municipality IS NOT NULL"
            if region:
                muni_filter += f" AND region IN ({','.join([f'\'{x}\'' for x in region])})"

            municipalities = con.execute(f"""
                SELECT DISTINCT municipality 
                FROM {table} 
                {muni_filter} 
                ORDER BY municipality
            """).fetchdf()["municipality"].tolist()

            municipality = st.multiselect("Kommun", municipalities, default=st.session_state.get("municipality", []), key="municipality")

        # shows "Ja" & "Nej" labels for boolean values in the ui, goes back to True & False for filtering
        with col3:
            exp = st.multiselect("Erfarenhet", options=yn, format_func=lambda x: x[0],
                                 default=st.session_state.get("experience_required", []), key="experience_required")
            experience_required = [val[1] for val in exp]

            lic = st.multiselect("Körkort", options=yn, format_func=lambda x: x[0],
                                 default=st.session_state.get("driving_license", []), key="driving_license")
            driving_license = [val[1] for val in lic]

    # returns the filters
    return {
        "occupation_group": occup_group,
        "occupation_label": occup_label,
        "duration": duration,
        "region": region,
        "municipality": municipality,
        "experience_required": experience_required,
        "driving_license": driving_license
    }

def filter_value(value):
    if isinstance(value, list):
        return ', '.join(str(v) for v in value)
    return str(value)

def show_time_slider(df, date_column="publication_date"):
    df[date_column] = pd.to_datetime(df[date_column])
    
    if df[date_column].dropna().empty:
        st.error("Inga datum tillgängliga för datumväljaren.")
        return pd.Timestamp.min, pd.Timestamp.mi
    
    min_date = df[date_column].min().date()
    max_date = df[date_column].max().date()

    if min_date == max_date:
        st.warning("Endast annonser från en dag hittades. Datumväljaren visas med detta datum.")
        max_date = min_date + pd.Timedelta(days=1)

    date_range = st.slider(
        "Välj datumintervall",
        min_value=min_date,
        max_value=max_date,
        value=(min_date, max_date),
        format="YYYY-MM-DD"
    )
    
    return date_range