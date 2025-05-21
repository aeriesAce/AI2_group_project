--dim table för employeer och location
SELECT
    {{ dbt_utils.generate_surrogate_key(['employer_workplace', 'municipality']) }} AS employer_id,
    MAX(COALESCE(employer_name, 'namn ej angiven')) AS employer_name,
    MAX(COALESCE(employer_workplace, 'plats ej angiven')) AS employer_workplace,
    MAX(COALESCE(organization_number, 'saknar organisationsnummer')) AS organization_number,
    MAX(COALESCE(region, 'län ej angivet')) AS region,
    MAX(COALESCE(municipality, 'kommun ej angiven')) AS municipality,
    MAX(COALESCE(workplace_address, 'address ej angiven')) AS workplace_address,
    MAX(COALESCE(workplace_postcode, 'post nummer saknas')) AS workplace_postcode,
    MAX(COALESCE(workplace_city, 'stad saknas')) AS workplace_city,
    MAX(COALESCE(country, 'land saknas')) AS country
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