#setup
import dagster as dg
from dagster_dbt import DbtCliResource, DbtProject, dbt_assets
from dagster_dlt import DagsterDltResource, dlt_assets

import dlt
from pathlib import Path

import sys
sys.path.insert(0, str(Path(__file__).parents[1] / '../Data'))
from pipeline import jobtech_source
from dlt.destinations import duckdb

db_path = str(Path(__file__).parent /"jobs.duckdb")

#dlt asset
dlt_resource = DagsterDltResource()

@dlt_assets(
    dlt_source = jobtech_source(),
    dlt_pipeline = dlt.pipeline(
        pipeline_name = "jobs",
        dataset_name = "staging",
        destination = duckdb(db_path)
    ),
)
def dlt_load(context: dg.AssetExecutionContext, dlt: DagsterDltResource):
    yield from dlt.run(context=context)

#dbt asset
dbt_project_directory = Path(__file__).parents[1].parent / "dbt_groupp"

profiles_dir = Path.home()/".dbt"

dbt_project = DbtProject(project_dir = dbt_project_directory,
                         profiles_dir = profiles_dir)

dbt_resource = DbtCliResource(project_dir=dbt_project)

dbt_project.prepare_if_dev()

@dbt_assets(manifest = dbt_project.manifest_path,)

def dbt_models(context: dg.AssetExecutionContext, dbt: DbtCliResource):
    yield from dbt.cli(["build"], context=context).stream()
#job
job_dlt = dg.define_asset_job("job_dlt", selection=dg.AssetSelection.keys("dlt_jobtech_source_jobs"))
job_dbt = dg.define_asset_job("job_dbt", selection=dg.AssetSelection.keys("stg_jobs"))

# schedule that runs job_dlt every day at 8:17 UTC
schedule_dlt= dg.ScheduleDefinition(
    job= job_dlt,
    cron_schedule= "05 10 * * *"
)

# sensor that triggers job_dbt when a specific asset is update
@dg.asset_sensor(asset_key= dg.AssetKey("dlt_jobtech_source_jobs"), 
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
