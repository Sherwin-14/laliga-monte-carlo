with current_results as (
    select * from {{ ref('stg_fdorg__matches') }}
    where status = 'FINISHED'
),

historical_results as (
    select * from {{ ref('stg_fdorg__matches_history') }}
    where status = 'FINISHED'
),

all_results as (
    select * from current_results
    union all
    select * from historical_results
)

select
    season,
    cast(utc_date at time zone 'Europe/Madrid' as date) as match_date,
    matchday,
    home_team_name,
    home_team_crest,
    away_team_name,
    away_team_crest,
    home_goals,
    away_goals,
    winner
from all_results
