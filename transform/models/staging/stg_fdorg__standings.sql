with source as (
    select * from {{ source('fdorg', 'standings') }}
),

renamed as (
    select
        cast(position as bigint) as position,
        cast(team_id as bigint) as team_id,
        cast(team_name as varchar) as team_name,
        cast(played_games as bigint) as played_games,
        cast(won as bigint) as won,
        cast(draw as bigint) as draw,
        cast(lost as bigint) as lost,
        cast(points as bigint) as points,
        cast(goals_for as bigint) as goals_for,
        cast(goals_against as bigint) as goals_against,
        cast(goal_difference as bigint) as goal_difference
    from source
)

select * from renamed
