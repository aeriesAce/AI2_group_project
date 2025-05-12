WITH base AS (
    SELECT DISTINCT
        j.job_id,
        j.external_id,
        j.relevance,
        j.number_of_vacancies,
        j.deadline,
        o.occupation_id,
        d.job_details_id,
        e.employer_id,
        a.auxilliary_attributes_id,
        j.conditions
        FROM {{ ref('stg_jobs') }} j

        LEFT JOIN {{ ref('dim_occupation') }} o
            ON {{ dbt_utils.generate_surrogate_key(['j.occupation_group', 'j.occupation_category', 'j.occupation_label']) }} = o.occupation_id
        
        LEFT JOIN {{ ref('dim_job_details') }} d
            ON {{ dbt_utils.generate_surrogate_key(['j.headline', 'j.employment_type']) }} = d.job_details_id
        
        LEFT JOIN {{ ref('dim_employer') }} e
            ON {{ dbt_utils.generate_surrogate_key(['j.employer_name', 'j.region', 'j.municipality', 'j.country', 'j.organization_number']) }} = e.employer_id  
       
        LEFT JOIN {{ ref('dim_auxilliary_attributes') }} a
            ON {{ dbt_utils.generate_surrogate_key(['j.experience_required', 'j.driving_license', 'j.own_car']) }} = a.auxilliary_attributes_id
)

SELECT 
    job_id,
    occupation_id,
    job_details_id,
    employer_id,
    auxilliary_attributes_id,
    number_of_vacancies,
    relevance,
    deadline,
    conditions
FROM base
WHERE occupation_id IS NOT NULL
    AND job_details_id IS NOT NULL 
    AND employer_id IS NOT NULL
    AND auxilliary_attributes_id IS NOT NULL
