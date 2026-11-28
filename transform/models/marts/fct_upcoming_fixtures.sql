with matches as (
    select * from {{ ref('stg_fdorg__matches') }}
),

upcoming as (
    select *
    from matches
    where status != 'FINISHED'
),

-- The next round is the earliest upcoming matchday at or after the last
-- finished round. The `>=` guard skips postponed leftovers from past matchdays.
next_matchday as (
    select min(matchday) as matchday
    from upcoming
    where matchday >= (select max(matchday) from matches where status = 'FINISHED')
),

localised as (
    select
        *,
        utc_date at time zone 'Europe/Madrid' as kickoff_madrid_ts,
        utc_date at time zone 'UTC' as kickoff_utc_ts
    from upcoming
)

select
    matchday,
    status,
    cast(kickoff_madrid_ts as date) as match_date,
    strftime(kickoff_madrid_ts, '%H:%M') as kickoff_madrid,
    strftime(kickoff_utc_ts, '%H:%M') as kickoff_utc,
    home_team_name,
    away_team_name
from localised
where matchday = (select matchday from next_matchday)
order by match_date, kickoff_madrid
