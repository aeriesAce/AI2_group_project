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
-- THIS IS A TEMPORARY FIX FOR TEST PURPOSE --
WHERE CAST(occupation_id AS TEXT) = 'MVqp_eS8_kDZ'