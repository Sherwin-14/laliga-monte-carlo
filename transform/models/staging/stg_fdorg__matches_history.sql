with source as (
    select * from {{ source('fdorg', 'matches_history') }}
),

renamed as (
    select
        cast(match_id as bigint) as match_id,
        cast(season as bigint) as season,
        cast(matchday as bigint) as matchday,
        cast(utc_date as timestamptz) as utc_date,
        cast(status as varchar) as status,
        cast(home_team_id as bigint) as home_team_id,
        cast(home_team_name as varchar) as home_team_name,
        cast(home_team_crest as varchar) as home_team_crest,
        cast(away_team_id as bigint) as away_team_id,
        cast(away_team_name as varchar) as away_team_name,
        cast(away_team_crest as varchar) as away_team_crest,
        cast(home_goals as bigint) as home_goals,
        cast(away_goals as bigint) as away_goals,
        cast(winner as varchar) as winner
    from source
)

select * from renamed
