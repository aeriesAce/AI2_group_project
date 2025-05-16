SELECT 
    job_id,
    employer_name,
    employer_workplace,
    organization_number,
    region,
    municipality,
    workplace_address,
    workplace_postcode,
    workplace_city,
    country
FROM {{ ref('stg_jobs') }}