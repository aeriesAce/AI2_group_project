-- mart schema for the occupation field "pedagogik"
WITH
    fct_job_ads as (select * from {{ ref('fct_job_ads') }}),
    dim_job_details as (select * from {{ ref('dim_job_details') }}),
    dim_occupation as (select * from {{ ref('dim_occupation') }}),
    dim_employer as (select * from {{ ref('dim_employer') }}),
    dim_auxilliary_attributes as (select * from {{ ref('dim_auxilliary_attributes')}})

SELECT
    o.occupation_category,
    f.job_id,
    f.number_of_vacancies,
    jd.job_description,
    e.employer_name,
    e.employer_id,
    e.region,
    e.municipality,
    e.country,
    f.conditions,
    CASE 
        WHEN LOWER(conditions) LIKE '%heltid%' THEN 'Heltid'
        WHEN LOWER(conditions) LIKE '%deltid%' THEN 'Deltid'
    END AS job_type
    
FROM fct_job_ads f
LEFT JOIN dim_employer e ON f.employer_id = e.employer_id
LEFT JOIN dim_job_details jd ON f.job_details_id = jd.job_details_id
LEFT JOIN dim_occupation o ON f.occupation_id = o.occupation_id
WHERE 
    o.occupation_category = 'Pedagogik' 
    AND (LOWER(f.conditions) LIKE '%heltid%' OR LOWER(f.conditions) LIKE '%deltid%')
