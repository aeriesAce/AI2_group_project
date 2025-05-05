-- dim table för job details
WITH source AS (
    SELECT DISTINCT
        headline,
        employment_type
    FROM {{ ref ('stg_jobs') }}
)
SELECT 
    {{ dbt_utils.generate_surrogate_key(['headline', 'employment_type']) }} AS job_details_id, --surrogat nyckel då vi har transformerat den datan i staging.
    headline,
    employment_type
FROM source