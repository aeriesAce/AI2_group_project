-- dim table för job details
SELECT
    {{ dbt_utils.generate_surrogate_key(['job_id', 'headline']) }} AS job_details_id,
    headline,
    job_description,
    job_description_formatted,
    employment_type,
    duration,
    salary_type,
    work_min,
    work_max
FROM {{ ref('src_job_details') }}
GROUP BY
    job_id,
    headline,
    job_description,
    job_description_formatted,
    employment_type,
    duration,
    salary_type,
    work_min,
    work_max