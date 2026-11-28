with scorers as (
    select * from {{ ref('stg_fdorg__scorers') }}
),

ranked as (
    select
        *,
        row_number() over (
            order by goals desc, player_name asc
        ) as scorer_rank
    from scorers
)

select
    scorer_rank,
    player_name,
    team_name,
    goals
from ranked
where scorer_rank <= 10
