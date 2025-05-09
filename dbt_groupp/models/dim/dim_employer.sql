--dim table för employeer och location
WITH source AS (
SELECT DISTINCT
    employer_name,
    employer_workplace,
    organization_number,
    workplace_address,
    region,
    workplace_postcode,
    municipality,
    country
FROM {{ ref ('stg_jobs') }}
)
SELECT
{{ dbt_utils.generate_surrogate_key(['employer_name', 'region', 'municipality', 'country','organization_number']) }} AS employer_id, --surrogat nyckel då vi har transformerat den datan i staging.
employer_name,
employer_workplace,
organization_number,
workplace_address,
region,
workplace_postcode,
municipality,
country
FROM source