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
),

aged as (
    select
        scorer_rank,
        player_name,
        team_name,
        nationality,
        -- Whole-year age, birthday-aware (not a naive year difference).
        extract(year from current_date) - extract(year from date_of_birth)
            - case
                when extract(month from current_date) < extract(month from date_of_birth)
                  or (
                    extract(month from current_date) = extract(month from date_of_birth)
                    and extract(day from current_date) < extract(day from date_of_birth)
                  )
                then 1
                else 0
              end as age,
        goals
    from ranked
)

select * from aged where scorer_rank <= 10
