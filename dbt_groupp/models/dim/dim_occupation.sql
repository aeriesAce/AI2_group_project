-- dim table för occupation grouping/category
SELECT
    {{ dbt_utils.generate_surrogate_key(['occupation_group', 'occupation_label', 'occupation_category']) }} AS occupation_id,
    occupation_group,
    occupation_label,
    occupation_category
FROM {{ ref('src_occupation') }}
GROUP BY
    occupation_group,
    occupation_label,
    occupation_category