{{      
     config(
        materialized='incremental', 
        unique_key = 'id'
     )
}}
SELECT 
    id,
    source,
    guid,
    title,
    pub_date,
    fetched_at
FROM
   {{ ref('stg_publications')}}
{% if is_incremental() %}
WHERE fetched_at > (SELECT MAX(fetched_at) from {{ this }})
{% endif %}
