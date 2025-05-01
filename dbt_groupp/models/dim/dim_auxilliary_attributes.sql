--dim table för extra job requirements
WITH source AS (
    SELECT DISTINCT
        md5(concat_ws('|',
            COALESCE(CAST(experience_required AS TEXT), ''),
            COALESCE(CAST(driving_license AS TEXT), ''),
            COALESCE(CAST(own_car AS TEXT), '')
        )) AS auxilliary_hash,
        experience_required,
        driving_license,
        own_car
    FROM {{ ref('stg_jobs') }}
    WHERE experience_required IS NOT NULL
        OR driving_license IS NOT NULL
        OR own_car IS NOT NULL
)
SELECT
    ROW_NUMBER() OVER (ORDER BY auxilliary_hash) AS auxilliary_attributes_id,
    --auxilliary_hash is needed for join logic only
    auxilliary_hash,
    experience_required,
    driving_license,
    own_car
FROM source