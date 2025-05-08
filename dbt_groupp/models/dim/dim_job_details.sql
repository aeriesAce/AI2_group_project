-- dim table för job details
WITH source AS (
    SELECT DISTINCT
        headline,
        job_description,
        job_description_formatted,
        employment_type,
        duration,
        salary_type,
        work_min,
        work_max,
    FROM {{ ref ('stg_jobs') }}
)
SELECT 
    {{ dbt_utils.generate_surrogate_key(['headline', 'employment_type']) }} AS job_details_id, --surrogat nyckel då vi har transformerat den datan i staging.
    headline,
    job_description,
    job_description_formatted,
    employment_type,
    duration,
    salary_type,
    work_min,
    work_max
FROM source