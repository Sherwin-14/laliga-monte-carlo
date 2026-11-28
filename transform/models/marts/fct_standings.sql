select
    position,
    team_name,
    played_games,
    won,
    draw,
    lost,
    goals_for,
    goals_against,
    goal_difference,
    points
from {{ ref('stg_fdorg__standings') }}
order by position
