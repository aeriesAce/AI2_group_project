--dim table för extra job requirements
SELECT
    {{ dbt_utils.generate_surrogate_key(['experience_required', 'driving_license', 'own_car']) }} AS auxilliary_id,
    experience_required,
    driving_license,
    own_car,
    publication_date,
    last_publication_date
FROM {{ ref('src_auxilliary') }}
GROUP BY
    experience_required,
    driving_license,
    own_car,
    publication_date,
    last_publication_date