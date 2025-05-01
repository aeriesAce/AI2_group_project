-- mart schema for the occupation field "pedagogik"
{{ config(materialized='view', schema='occupation') }}

SELECT
    job_id,
    occupation_id,
    employer_id,
    auxilliary_attributes_id,
    number_of_vacancies,
    relevance,
    deadline
FROM {{ ref('fct_job_ads') }}
WHERE occupation_category = 'Pedagogik'