-- mart schema for developement over time --
{{ config(materialized='view') }}
SELECT
    publication_date,
    last_publication_date,
    number_of_vacancies,
    deadline
FROM {{ ref('stg_jobs') }}

WHERE deadline >= CURRENT_DATE