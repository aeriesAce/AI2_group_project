-- mart schema for developement over time --
WITH base AS (
    SELECT *
    FROM {{ ref('stg_jobs') }}
    WHERE deadline >= CURRENT_DATE
)

SELECT
    DATE_TRUNC('month', publication_date) AS month,
    DATE_TRUNC('quarter', publication_date) AS quarter,
    DATE_TRUNC('year', publication_date) AS year,
    occupation_category,
    occupation_group,
    region,
    municipality,
    COUNT(job_id) AS antal_annonser,
    SUM(number_of_vacancies) AS "Totala jobb",
    MIN(deadline) AS första_deadline,
    MAX(deadline) AS sista_deadline
FROM base
GROUP BY
    DATE_TRUNC('month', publication_date),
    DATE_TRUNC('quarter', publication_date),
    DATE_TRUNC('year', publication_date),
    occupation_category,
    occupation_group,
    region,
    municipality