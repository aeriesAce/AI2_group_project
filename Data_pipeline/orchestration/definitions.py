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

# schedule that runs job_dlt every day at 8:17 UTC
schedule_dlt= dg.ScheduleDefinition(
    job= job_dlt,
    cron_schedule= "17 8 * * *"
)

# sensor that triggers job_dbt when a specific asset is update
@dg.asset_sensor(asset_key= dg.AssetKey("DET SOM VI VÄLJER UNDER JOB"), # <---- ÄNDRRAS
                 job_name= "job_dbt")
def dlt_load_sensor():
    yield dg.RunRequest()


# definition object that bundles assets, resources, jobs, schedules, and sensors
defs= dg.Definitions(
    assets = [dlt_load, dbt_models],
    resources= {"dlt": dlt_resource,
                "dbt": dbt_resource},
    jobs= [job_dlt, job_dbt],
    schedules= [schedule_dlt],
    sensors= [dlt_load_sensor]
)
