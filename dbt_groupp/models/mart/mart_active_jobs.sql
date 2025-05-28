-- mart schema for developement over time --
SELECT
    job_id,
    publication_date,
    deadline,
    occupation_category,
    occupation_group,
    occupation_label,
    region,
    municipality,
    number_of_vacancies,
    employer_name,
FROM {{ ref('stg_jobs') }}
WHERE deadline >= CURRENT_DATE
