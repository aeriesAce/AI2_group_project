import streamlit as st
from Dashboard.query import get_form_of_employement, get_jobs_per_city, get_most_sought_occ, get_vacant_jobs_per_occ, get_jobs_over_time

def show_kpis(selected_occupation):
    jobs_df = get_jobs_per_city()
    vacancies_df = get_vacant_jobs_per_occ()
    sought_df = get_most_sought_occ()
    jobs_over_t_df = get_jobs_over_time()
    form_of_employ = get_form_of_employement()
    
    # KPI for total jobs
    total_jobs = jobs_df[jobs_df['occupation_category'] == selected_occupation]["Totala jobb"].sum()
    st.metric(f"Totalt antal jobb inom {selected_occupation}", total_jobs)

    # KPI for total vacancies
    total_vacancies = vacancies_df[vacancies_df['occupation_category'] == selected_occupation]["Lediga jobb"].sum()
    st.metric("Lediga tjänster", total_vacancies)

    # KPI for regions with jobs
    # num_municipalities = jobs_df[jobs_df['occupation_category'] == selected_occupation]["municipality"].nunique()
    # st.metric("Antal kommuner", num_municipalities)

    # KPI most sought employement form
    most_common_form = sought_df[sought_df['occupation_category'] == selected_occupation]["Anställningsform"].mode()
    most_common_form = most_common_form.iloc[0] if not most_common_form.empty else "N/A"
    st.metric("Populäraste anställningsform", most_common_form)
