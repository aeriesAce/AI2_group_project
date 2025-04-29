import dlt
import requests

# Function to get data
def fetch_jobs(occupation_fields):
    base_url = "https://jobsearch.api.jobtechdev.se/search?offset=100&limit=100"
    for field in occupation_fields:
        params = {'occupation-field': field}
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        for job in data.get("hits", []):
            yield job  # DLT generator

# DLT source (connectts to the pipeline)
@dlt.source
def jobtech_source():
    occupation_fields = [
        "MVqp_eS8_kDZ",  # Pedagogik
        "E7hm_BLq_fqZ",  # Säkerhet och bevakning
        "ASGV_zcE_bWf"   # Transport, distribution, lager
    ]
    return dlt.resource(fetch_jobs(occupation_fields), name="jobs")