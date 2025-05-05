WITH base AS (
    SELECT *
    FROM {{ ref('fct_job_ads') }}
)

SELECT
    *,
    deadline <CURRENT_DATE AS is_expired, --ger oss aktiva annonser
    DATE_DIFF('day', CURRENT_DATE, deadline) AS days_until_deadline --visar hur många dagar kvar tills annonsen tar slut
FROM base
WHERE deadline >= CURRENT_DATE