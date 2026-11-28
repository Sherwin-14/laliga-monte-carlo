with source as (
    select * from {{ source('fdorg', 'matches') }}
),

renamed as (
    select
        cast(match_id as bigint) as match_id,
        cast(matchday as bigint) as matchday,
        cast(utc_date as timestamptz) as utc_date,
        cast(status as varchar) as status,
        cast(home_team_name as varchar) as home_team_name,
        cast(away_team_name as varchar) as away_team_name
    from source
)

select * from renamed
