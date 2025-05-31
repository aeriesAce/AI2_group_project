-- duplicate check in staging since we are running append on our database instead of replace,
-- just so we can save the history.

With source AS (
    SELECT
        *,
        ROW_NUMBER() OVER (PARTITION BY id ORDER BY publication_date desc) AS row_num
    FROM {{ source('jobs', 'jobs') }}
),

deduplicated AS (
    SELECT * FROM source WHERE row_num = 1
)

SELECT
    id AS job_id,
    external_id,
    relevance,
    headline,
    employer__name AS employer_name,
    employment_type__label AS employment_type,
    occupation_group__label AS occupation_group,
    occupation__label AS occupation_label,
    workplace_address__municipality AS municipality,
    workplace_address__municipality_code AS municipality_code,
    workplace_address__region AS region,
    workplace_address__region_code AS region_code,
    workplace_address__country AS country,
    workplace_address__country_code AS country_code,
    workplace_address__street_address AS workplace_address,
    workplace_address__postcode AS workplace_postcode,
    workplace_address__city AS workplace_city,
    application_details__information AS application_information,
    application_details__other as application_details,
    publication_date,
    last_publication_date,
    removed,
    number_of_vacancies,
    experience_required,
    access_to_own_car AS own_car,
    driving_license_required AS driving_license,
    application_deadline AS deadline,
    description__conditions AS conditions,
    description__text AS job_description,
    description__text_formatted as job_description_formatted,
    salary_type__label AS salary_type,
    salary_description,
    duration__label AS duration,
    working_hours_type__label AS working_hours,
    employer__organization_number AS organization_number,
    employer__workplace AS employer_workplace,
    scope_of_work__min as work_min,
    scope_of_work__max as work_max,

    CASE
        WHEN occupation_field__concept_id = 'MVqp_eS8_kDZ' THEN 'Pedagogik'
        WHEN occupation_field__concept_id = 'E7hm_BLq_fqZ' THEN 'Säkerhet och bevakning'
        WHEN occupation_field__concept_id = 'ASGV_zcE_bWf' THEN 'Transport och lager'
        ELSE 'Ospecifierad'
    END AS occupation_category

FROM deduplicated
 


