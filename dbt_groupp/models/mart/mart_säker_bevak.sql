-- mart schema for the occupation field "säkerhet och bevakning"
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
WHERE CAST(occupation_id AS TEXT) = 'E7hm_BLq_fqZ'