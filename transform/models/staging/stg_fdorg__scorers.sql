with source as (
    select * from {{ source('fdorg', 'scorers') }}
),

renamed as (
    select
        cast(player_id as bigint) as player_id,
        cast(player_name as varchar) as player_name,
        cast(team_id as bigint) as team_id,
        cast(team_name as varchar) as team_name,
        cast(goals as bigint) as goals,
        cast(assists as bigint) as assists,
        cast(penalties as bigint) as penalties
    from source
)

select * from renamed
