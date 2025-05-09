-- mart schema for the occupation field "säkerhet och bevakning"
{{ config(materialized='view', schema='occupation') }}

-- Join fct_job_ads with dim_employer to create a mart view for Transport och lager occupation
SELECT
    f.job_id,
    f.employer_id,
    d.employer_name,
    f.number_of_vacancies,
    d.region,
    d.municipality,
    d.country,
    o.occupation_category
FROM {{ ref('fct_job_ads') }} f
LEFT JOIN {{ ref('dim_employer') }} d ON f.employer_id = d.employer_id
left join {{ref('dim_occupation') }} o ON o.occupation_id = o.occupation_id
WHERE o.occupation_category = 'Säkerhet och bevakning'