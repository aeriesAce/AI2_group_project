--dim table för extra job requirements
WITH source AS (
    SELECT DISTINCT
        experience_required,
        driving_license,
        own_car
    FROM {{ ref('stg_jobs') }}
    WHERE experience_required IS NOT NULL
        OR driving_license IS NOT NULL
        OR own_car IS NOT NULL
)
SELECT
    {{ dbt_utils.generate_surrogate_key(['experience_required', 'driving_license', 'own_car']) }} AS auxilliary_attributes_id,
    experience_required,
    driving_license,
    own_car
FROM source