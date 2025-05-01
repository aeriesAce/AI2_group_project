--dim table för employeer och location
WITH source AS (
    SELECT DISTINCT
        employer_name,
        region,
        municipality,
        country
    FROM {{ ref ('stg_jobs') }}
)
SELECT
    ROW_NUMBER() OVER (ORDER BY employer_name) AS employer_id, --surrogat nyckel då vi har transformerat den datan i staging.
    employer_name,
    region,
    municipality,
    country
FROM source