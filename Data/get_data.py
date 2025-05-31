import dlt
import requests

# Function to get data
def fetch_jobs(occupation_fields):
    base_url = "https://jobsearch.api.jobtechdev.se/search"
    limit = 100
    for field in occupation_fields:
        offset = 0
        while True:
            params = {
                'occupation-field': field,
                'limit': limit,
                'offset': offset
            }
            response = requests.get(base_url, params=params)
            response.raise_for_status()
            data = response.json()
            hits = data.get("hits", [])

            if not hits:
                break

            for job in hits:
                yield job

            if len(hits) < limit or offset >= 1900:
                break

            offset += limit


# DLT source (connectts to the pipeline)
@dlt.source
def jobtech_source():
    occupation_fields = [
        "MVqp_eS8_kDZ",  # Pedagogik
        "E7hm_BLq_fqZ",  # Säkerhet och bevakning
        "ASGV_zcE_bWf"   # Transport, distribution, lager
    ]
    return dlt.resource(fetch_jobs(occupation_fields), name="jobs", primary_key="id", write_disposition="merge")