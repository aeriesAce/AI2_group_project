With source AS (
    SELECT
        id AS job_id,
        external_id,
        relevance,
        headline,
        employer__name AS employer_name,
        employment_type__label AS employment_type,
        occupation_group__label AS occupation_group,
        workplace_address__municipality AS municipality,
        workplace_address__region AS region,
        workplace_address__country AS country,
        last_publication_date,
        number_of_vacancies,
        experience_required,
        access_to_own_car AS own_car,
        driving_license_required AS driving_license,
        application_deadline AS deadline,

        CASE
            WHEN occupation_field__concept_id = 'MVqp_eS8_kDZ' THEN 'Pedagogik'
            WHEN occupation_field__concept_id = 'E7hm_BLq_fqZ' THEN 'Säkerhet och bevakning'
            WHEN occupation_field__concept_id = 'ASGV_zcE_bWf' THEN 'Transport och lager'
            ELSE 'Ospecifierad'
        END AS occupation_category
    FROM {{ source('staging', 'jobs') }}
)

Select * FROM source

