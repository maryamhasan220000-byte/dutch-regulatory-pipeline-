WITH monthly_count AS(
SELECT 
    source,
    DATE_TRUNC('month', pub_date) AS month,
    COUNT(*) AS publication_count 
FROM 
   {{ ref('stg_publications')}}
GROUP BY
    source, DATE_TRUNC('month', pub_date)
)

SELECT 
    source,
    month, 
    publication_count,
    LAG(publication_count) OVER(
        PARTITION BY source
        ORDER BY month
    ) AS previous_month_count, 
    publication_count - LAG(publication_count) OVER (
        PARTITION BY source
        ORDER BY month
    ) AS change_from_previous_month
FROM
    monthly_count 
ORDER BY 
   source, month 

    



