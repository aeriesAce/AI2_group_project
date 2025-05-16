SELECT
    job_id,
    occupation_group,
    occupation_label,
    occupation_category
FROM {{ ref('stg_jobs') }}