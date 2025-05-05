-- mart schema for the occupation field "pedagogik"
{{ config(materialized='view', schema='occupation') }}

-- Join fct_job_ads with dim_employer to create a mart view for Transport och lager occupation
SELECT
    f.job_id,
    f.employer_id,
    d.employer_name,
    f.number_of_vacancies,
    d.region,
    d.municipality,
    d.country
FROM {{ ref('fct_job_ads') }} f
LEFT JOIN refined.dim_employer d ON f.employer_id = d.employer_id
WHERE f.occupation_category = 'Pedagogik'