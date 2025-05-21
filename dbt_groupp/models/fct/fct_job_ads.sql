SELECT
    {{ dbt_utils.generate_surrogate_key(['occupation_group', 'occupation_label', 'occupation_category']) }} AS occupation_id,
    {{ dbt_utils.generate_surrogate_key(['job_id', 'headline']) }} AS job_details_id,
    {{ dbt_utils.generate_surrogate_key(['employer_name', 'municipality']) }} AS employer_id,
    {{ dbt_utils.generate_surrogate_key(['experience_required', 'driving_license', 'own_car']) }} AS auxilliary_id,
    COALESCE(CAST(number_of_vacancies AS INTEGER), 1) AS vacancies,
    relevance,
    deadline,
    working_hours AS conditions
FROM {{ ref('stg_jobs') }} 
