SELECT
    job_id,
    headline,
    job_description,
    job_description_formatted,
    employment_type,
    duration,
    salary_type,
    work_min,
    work_max
FROM {{ ref('stg_jobs') }}