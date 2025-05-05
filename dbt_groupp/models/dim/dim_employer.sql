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
    {{ dbt_utils.dbt_utils.generate_surrogate_key(['employer_name', 'region', 'municipality', 'country']) }} AS employer_id, --surrogat nyckel då vi har transformerat den datan i staging.
    employer_name,
    region,
    municipality,
    country
FROM source