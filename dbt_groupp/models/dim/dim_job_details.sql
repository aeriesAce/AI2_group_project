-- dim table för job details
WITH source AS (
    SELECT DISTINCT
        headline,
        employment_type
    FROM {{ ref ('stg_jobs') }}
)
SELECT 
    ROW_NUMBER() OVER (ORDER BY headline) AS job_details_id, --surrogat nyckel då vi har transformerat den datan i staging.
    headline,
    employment_type
FROM source