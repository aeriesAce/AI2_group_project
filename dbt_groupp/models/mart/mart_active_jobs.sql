-- mart schema for developement over time --
{{ config(materialized='view') }}
SELECT
    publication_date,
    last_publication_date
FROM {{ ref('stg_jobs') }}

WHERE publication_date >= CURRENT_DATE