import dlt
from data_pipeline.get_data import jobtech_source

pipeline = dlt.pipeline(
    pipeline_name = "jobs",
    destination= "duckdb",
    dataset_name ="staging"
)
info = pipeline.run(jobtech_source())
print(info)

## test to see how much is being loaded from the pipeline after it has run.
##con = duckdb.connect("jobs.duckdb")
##result = con.execute("SELECT COUNT(*) FROM staging.jobs").fetchone()
##print(f"Rows loaded into staging.jobs: {result[0]}")