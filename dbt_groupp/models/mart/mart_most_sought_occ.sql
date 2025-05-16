-- mart schema for most sought after jobs per region --
WITH
    fct_job_ads as (select * from {{ ref('fct_job_ads') }}),
    dim_job_details as (select * from {{ ref('dim_job_details') }}),
    dim_occupation AS (SELECT * FROM {{ ref('dim_occupation')}}),
    dim_employer AS (SELECT * FROM {{ ref('dim_employer')}})

SELECT
    e.region AS "Län",
    e.municipality AS "Stad",
    o.occupation_category,
    jd.employment_type AS "Anställningsform"
FROM fct_job_ads f
LEFT JOIN dim_job_details jd ON f.job_details_id = jd.job_details_id
LEFT JOIN dim_occupation o ON f.occupation_id = o.occupation_id
LEFT JOIN dim_employer e ON f.employer_id = e.employer_id
GROUP BY jd.employment_type, o.occupation_category, e.region, e.municipality