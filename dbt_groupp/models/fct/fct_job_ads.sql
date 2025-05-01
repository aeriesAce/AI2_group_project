WITH base AS(
    SELECT
        j.job_id,
        j.external_id,
        j.relevance,
        j.last_publication_date,
        j.number_of_vacancies,
        j.deadline,
        j.occupation_category,
        o.occupation_id,
        d.job_details_id,
        e.employer_id,
        a.auxilliary_attributes_id
        FROM {{ ref('stg_jobs') }} j

        LEFT JOIN {{ ref('dim_occupation') }} o
            ON j.occupation_group = o.occupation_group
                AND j.occupation_category = o.occupation_category
        
        LEFT JOIN {{ ref('dim_job_details') }} d
            ON j.headline = d.headline
                AND j.employment_type = d.employment_type
        
        LEFT JOIN {{ ref('dim_employer') }} e
            ON j.employer_name = e.employer_name
                AND j.region = e.region
                AND j.municipality = e.municipality
                AND j.country = e.country
        
        LEFT JOIN {{ ref('dim_auxilliary_attributes') }} a
            ON md5(concat_ws('|',
                COALESCE(j.experience_required, ''),
                COALESCE(j.driving_license, ''),
                COALESCE(j.own_car, '')
            )) = a.auxilliary_hash
)

SELECT 
    occupation_id,
    job_id,
    occupation_category,
    employer_id,
    auxilliary_attributes_id,
    number_of_vacancies,
    relevance,
    deadline
FROM base
