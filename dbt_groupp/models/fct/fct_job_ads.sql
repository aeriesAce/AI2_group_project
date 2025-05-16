SELECT
    o.occupation_id,
    jd.job_details_id,
    e.employer_id,
    a.auxilliary_id,
    j.number_of_vacancies,
    j.relevance,
    j.deadline
FROM {{ ref('stg_jobs') }} j

LEFT JOIN {{ ref('dim_occupation') }} o
    ON j.occupation_group = o.occupation_group
    AND j.occupation_label = o.occupation_label
    AND j.occupation_category = o.occupation_category

LEFT JOIN {{ ref('dim_job_details') }} jd
    ON j.headline = jd.headline

LEFT JOIN {{ ref('dim_employer') }} e
    ON j.employer_name = e.employer_name
    AND j.municipality = e.municipality

LEFT JOIN {{ ref('dim_auxilliary_attributes') }} a
    ON j.experience_required = a.experience_required
    AND j.driving_license = a.driving_license
    AND j.own_car = a.own_car