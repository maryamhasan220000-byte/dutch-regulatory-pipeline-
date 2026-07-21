SELECT 
    id,
    LOWER(source) AS source,
    guid,
    title,
    link,
    description,
    pub_date,
    language,
    fetched_at
FROM
    {{ source('raw', 'publications')}}
