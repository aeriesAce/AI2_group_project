import dlt
from Test_dlt import jobtech_source
pipeline = dlt.pipeline(
    pipeline_name = "jobs",
    destination= "duckdb",
    dataset_name ="staging"
)
info = pipeline.run(jobtech_source())
print(info)