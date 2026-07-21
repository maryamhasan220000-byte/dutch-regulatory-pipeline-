SELECT 
     source,
     AVG(monthly_count) AS avg_monthly_publications
FROM (
SELECT 
    source,
    DATE_TRUNC('month', pub_date) AS month,
    COUNT(*) AS monthly_count 
FROM 
    {{ ref('stg_publications')}}
GROUP BY 
    source, DATE_TRUNC('month', pub_date)
) AS monthly_breakdown
GROUP BY 
    source