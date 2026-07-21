WITH monthly_count AS(
    SELECT 
        source, 
        DATE_TRUNC('month', pub_date) AS month, 
        COUNT(*) publication_count
    FROM 
       {{ ref('stg_publications') }}
    GROUP BY 
       source, DATE_TRUNC('month', pub_date)

)

SELECT 
    monthly_count.source, 
    monthly_count.month,
    monthly_count.publication_count,
    historical.avg_monthly_publications,
    monthly_count.publication_count > historical.avg_monthly_publications AS above_average
FROM 
    monthly_count 
JOIN
    {{  ref('int_source_historical_averages')}} AS historical
    ON monthly_count.source = historical.source
ORDER BY 
    monthly_count.source, monthly_count.month 