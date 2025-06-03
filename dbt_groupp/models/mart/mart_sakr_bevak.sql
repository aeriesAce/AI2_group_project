-- mart schema for the occupation field Säkerhet och bevakning --
{{ config(materialized='view') }}
WITH
    fct_job_ads AS (SELECT * FROM {{ ref('fct_job_ads') }}),
    dim_job_details AS (SELECT * FROM {{ ref('dim_job_details') }}),
    dim_occupation AS (SELECT * FROM {{ ref('dim_occupation') }}),
    dim_employer AS (SELECT * FROM {{ ref('dim_employer') }}),
    dim_auxilliary_attributes AS (SELECT * FROM {{ ref('dim_auxilliary_attributes') }})
SELECT
    f.vacancies,
    f.relevance,
    f.deadline,
    CAST(f.publication_date AS DATE) AS publication_date,
    e.employer_name,
    e.employer_workplace,
    e.country,
    e.region,
    e.municipality,
    o.occupation_label,
    o.occupation_group,
    o.occupation_category,
    jd.job_id,
    jd.headline,
    jd.job_description,
    jd.job_description_formatted,
    jd.employment_type,
    jd.duration,
    jd.salary_type,
    jd.work_min,
    jd.work_max,
    a.experience_required,
    a.driving_license,
    a.own_car
FROM fct_job_ads f
LEFT JOIN dim_job_details jd ON f.job_details_id = jd.job_details_id
LEFT JOIN dim_occupation o ON f.occupation_id = o.occupation_id
LEFT JOIN dim_employer e ON f.employer_id = e.employer_id
LEFT JOIN dim_auxilliary_attributes a ON f.auxilliary_id = a.auxilliary_id
WHERE o.occupation_category = 'Säkerhet och bevakning'