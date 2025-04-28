import dlt
pipeline = dlt.pipeline(
    pipeline_name = "jobtech_pipeline",
    destination= "duckdb",
    dataset_name ="jobs_dataset"
)
info = pipeline.run(jobtech_source())
print(info)