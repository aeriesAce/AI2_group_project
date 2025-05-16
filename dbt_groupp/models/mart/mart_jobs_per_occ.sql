-- mart schema for jobs per occupation"
WITH
    fct_job_ads as (select * from {{ ref('fct_job_ads') }}),
    dim_occupation as (select * from {{ ref('dim_occupation') }}),
    dim_employer as (select * from {{ ref('dim_employer') }})

SELECT
    o.occupation_category,
    o.occupation_group AS Yrke,
    f.number_of_vacancies AS "Lediga jobb"
FROM fct_job_ads f
LEFT JOIN dim_employer e ON f.employer_id = e.employer_id
LEFT JOIN dim_occupation o ON f.occupation_id = o.occupation_id
GROUP BY o.occupation_group, o.occupation_category, f.number_of_vacancies