SELECT
    job_id,
    experience_required,
    driving_license,
    own_car,
    publication_date,
    last_publication_date
FROM {{ ref('stg_jobs') }}