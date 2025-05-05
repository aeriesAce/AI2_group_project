-- mart schema for the occupation field "transport/distrubition/lager"
{{ config(materialized='view', schema='occupation') }}

SELECT
    job_id,
    occupation_id,
    employer_id,
    auxilliary_attributes_id,
    region,
    number_of_vacancies,
    relevance,
    deadline
FROM {{ ref('fct_job_ads') }}
WHERE occupation_category = 'Transport och lager'