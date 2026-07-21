SELECT *
FROM {{ ref('mart_publications_monthly_trend')}}
WHERE change_from_previous_month IS NOT NULL
AND 
change_from_previous_month != (publication_count - 
previous_month_count )