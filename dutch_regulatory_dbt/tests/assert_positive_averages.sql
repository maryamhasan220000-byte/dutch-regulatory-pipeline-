SELECT * 
FROM {{ ref('int_source_historical_averages')}}
WHERE avg_monthly_publications < 0