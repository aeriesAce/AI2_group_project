SELECT
    job_id,
    experience_required,
    driving_license,
    own_car
FROM {{ ref('stg_jobs') }}