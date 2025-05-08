-- dim table för occupation grouping/category
WITH source AS(
    SELECT DISTINCT
        occupation_group,
        occupation_category,
        occupation_label,
    FROM {{ ref('stg_jobs') }}
)
SELECT
    {{ dbt_utils.generate_surrogate_key(['occupation_group', 'occupation_category']) }} AS occupation_id, --surrogat nyckel då vi har transformerat den datan i staging.
    occupation_group,
    occupation_category,
    occupation_label
FROM source