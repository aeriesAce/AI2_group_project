-- dim table för occupation grouping/category
WITH source AS(
    SELECT DISTINCT
        occupation_group,
        occupation_category
    FROM {{ ref('stg_jobs') }}
)
SELECT
    ROW_NUMBER() OVER (ORDER BY occupation_group) AS occupation_id, --surrogat nyckel då vi har transformerat den datan i staging.
    occupation_group,
    occupation_category
FROM source