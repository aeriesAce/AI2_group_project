import streamlit as st
import duckdb
import pandas as pd
con = duckdb.connect("jobs.duckdb")

def get_jobs_per_city():
    query = """
        SELECT occupation_category,  
        "Totala jobb"
        FROM marts.mart_jobs_per_city
        """
    return con.execute(query).fetchdf()

def get_vacant_jobs_per_occ():
    query = """
        SELECT occupation_category, 
            Yrke, 
            "Lediga jobb"
        FROM marts.mart_jobs_per_occ
        """
    return con.execute(query).fetchdf()

def get_form_of_employement():
    query = """
        SELECT conditions, 
            occupation_category, 
            region, 
            municipality, 
            number_of_vacancies
        FROM marts.mart_anställningsvillkor
        """
    return con.execute(query).fetchdf()

def get_most_sought_occ():
    query = """
        SELECT "Län", 
           "Stad", 
            occupation_category, 
            "Anställningsform"
        FROM marts.mart_most_sought_occ
        """
    return con.execute(query).fetchdf()

def get_jobs_over_time():
    query = """
        SELECT
            "month",
            "quarter",
            "year",
            occupation_group,
            occupation_category,
            "Totala jobb",
        FROM marts.mart_active_jobs
        GROUP BY "month", "quarter", "year", "Totala jobb", occupation_group, occupation_category
    """
    return con.execute(query).fetchdf()