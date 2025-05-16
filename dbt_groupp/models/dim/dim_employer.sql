--dim table för employeer och location
SELECT
    {{ dbt_utils.generate_surrogate_key(['employer_name', 'municipality']) }} AS employer_id,
    employer_name,
    employer_workplace,
    organization_number,
    region,
    municipality,
    workplace_address,
    workplace_postcode,
    workplace_city,
    country
FROM {{ ref('src_employer') }}
GROUP BY
    employer_name,
    employer_workplace,
    organization_number,
    region,
    municipality,
    workplace_address,
    workplace_postcode,
    workplace_city,
    country