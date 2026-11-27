with scorers as (
    select * from {{ ref('stg_fdorg__scorers') }}
),

ranked as (
    select
        *,
        row_number() over (
            order by goals desc, assists desc, player_name asc
        ) as scorer_rank
    from scorers
)

select * from ranked
