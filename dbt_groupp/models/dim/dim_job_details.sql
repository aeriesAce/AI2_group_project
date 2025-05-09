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
        conditions,
        CASE 
            WHEN LOWER(conditions) LIKE '%heltid%' THEN 'Heltid'
            WHEN LOWER(conditions) LIKE '%deltid%' THEN 'Deltid'
        END AS job_type
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
    work_max,
    job_type
FROM source
WHERE job_type IS NOT NULL
