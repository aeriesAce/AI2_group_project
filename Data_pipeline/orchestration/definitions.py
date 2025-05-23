#setup
import dagster as dg
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets
from dagster_dlt import DagsterDltResource, dlt_assets

import dlt
from pathlib import Path

import sys
sys.path.insert(0, '../Data_pipeline')
from pipeline import jobtech_source

db_path = str(Path(__file__).parents[1] /"jobs.duckdb")

#dlt asset

#dbt asset

#job

#sensor

#definitions