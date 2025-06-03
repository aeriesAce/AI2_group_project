import dlt
import duckdb
from get_data import jobtech_source

DB_path = "jobs.duckdb"
TABLE_NAME = "staging.jobs"

def run_pipeline():
    con = duckdb.connect(DB_path)
    try: 
        before_count = con.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}").fetchone()[0]
    except duckdb.CatalogException:
        before_count = 0

    pipeline = dlt.pipeline(
        pipeline_name = "jobs",
        destination= "duckdb",
        dataset_name ="staging"
    )
    info = pipeline.run(jobtech_source())
    print(info)

    after_count = con.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}").fetchone()[0]
    new_rows = after_count - before_count

    print(f"new adds added: {new_rows}")

if __name__ == "__main__":
    run_pipeline()
## test to see how much is being loaded from the pipeline after it has run.
##con = duckdb.connect("DB_path")
##result = con.execute(f"SELECT COUNT(*) FROM {TABLE_NAME}").fetchone()
##print(f"Rows loaded into staging.jobs: {result[0]}")