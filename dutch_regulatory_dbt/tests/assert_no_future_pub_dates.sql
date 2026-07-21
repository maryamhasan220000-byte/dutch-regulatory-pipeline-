select * 
FROM {{ ref('stg_publications')}}
WHERE pub_date > CURRENT_TIMESTAMP