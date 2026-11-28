---
title: Current Season
---

La Liga — the live table and the race for the golden boot.

## Standings

```sql standings
select * from src_fct_standings
order by position
```

<DataTable data={standings} rows=20>
  <Column id=position title="#"/>
  <Column id=team_crest contentType=image height=25px title=" "/>
  <Column id=team_name title="Team"/>
  <Column id=played_games title="P"/>
  <Column id=won title="W"/>
  <Column id=draw title="D"/>
  <Column id=lost title="L"/>
  <Column id=goals_for title="GF"/>
  <Column id=goals_against title="GA"/>
  <Column id=goal_difference title="GD"/>
  <Column id=points title="Pts"/>
</DataTable>

## Next Matchday

In La Liga every team plays every other team twice (once at home, once away) for **38 rounds** over the season. Each round is called a *matchday* (or *jornada* in Spanish): all 20 clubs play that weekend, so a matchday is **10 matches** spread across Friday, Saturday, Sunday and Monday. Teams don't all kick off at once; fixtures are staggered so each game gets its own slot, which is why one matchday stretches over several days.

Below are the fixtures for the upcoming matchday, ordered by kickoff. Times are shown in **Madrid local time** and **UTC** (Spain runs on Central European Time: UTC+1 in winter, UTC+2 in summer).

```sql next_fixtures
select * from src_fct_upcoming_fixtures
order by match_date, kickoff_madrid
```

<DataTable data={next_fixtures} rows=5>
  <Column id=matchday title="MD"/>
  <Column id=match_date title="Date"/>
  <Column id=kickoff_madrid title="Kickoff (Madrid)"/>
  <Column id=kickoff_utc title="Kickoff (UTC)"/>
  <Column id=home_team_crest contentType=image height=25px title=" "/>
  <Column id=home_team_name title="Home"/>
  <Column id=away_team_crest contentType=image height=25px title=" "/>
  <Column id=away_team_name title="Away"/>
</DataTable>

## Head to Head

Pick two teams to see their head-to-head record and recent meetings. "Team A" is the first dropdown and drives the W/D/L column and the win tally.

```sql h2h_teams
select distinct team_name
from (
    select home_team_name as team_name from src_fct_match_results
    union
    select away_team_name as team_name from src_fct_match_results
) t
order by team_name
```

<Dropdown data={h2h_teams} name=team_a value=team_name title="Team A" defaultValue={['Real Madrid CF']}/>
<Dropdown data={h2h_teams} name=team_b value=team_name title="Team B" defaultValue={['FC Barcelona']}/>

```sql h2h_summary
with meetings as (
    select *
    from src_fct_match_results
    where (home_team_name = '${inputs.team_a.value}' and away_team_name = '${inputs.team_b.value}')
       or (home_team_name = '${inputs.team_b.value}' and away_team_name = '${inputs.team_a.value}')
),
perspective as (
    select
        case when home_team_name = '${inputs.team_a.value}' then home_goals else away_goals end as team_a_goals,
        case when home_team_name = '${inputs.team_a.value}' then away_goals else home_goals end as team_b_goals
    from meetings
)
select
    count(*) as meetings,
    coalesce(sum(case when team_a_goals > team_b_goals then 1 else 0 end), 0) as team_a_wins,
    coalesce(sum(case when team_a_goals = team_b_goals then 1 else 0 end), 0) as draws,
    coalesce(sum(case when team_a_goals < team_b_goals then 1 else 0 end), 0) as team_b_wins
from perspective
```

<BigValue data={h2h_summary} value=team_a_wins title="Team A Wins"/>
<BigValue data={h2h_summary} value=draws title="Draws"/>
<BigValue data={h2h_summary} value=team_b_wins title="Team B Wins"/>

```sql h2h_meetings
with meetings as (
    select *
    from src_fct_match_results
    where (home_team_name = '${inputs.team_a.value}' and away_team_name = '${inputs.team_b.value}')
       or (home_team_name = '${inputs.team_b.value}' and away_team_name = '${inputs.team_a.value}')
)
select
    cast(cast(season as bigint) as varchar) || '/' || cast(cast((season + 1) % 100 as bigint) as varchar) as season_label,
    match_date,
    home_team_name,
    cast(cast(home_goals as bigint) as varchar) || ' - ' || cast(cast(away_goals as bigint) as varchar) as score,
    away_team_name,
    case
        when home_team_name = '${inputs.team_a.value}' and home_goals > away_goals then 'W'
        when home_team_name = '${inputs.team_a.value}' and home_goals < away_goals then 'L'
        when away_team_name = '${inputs.team_a.value}' and away_goals > home_goals then 'W'
        when away_team_name = '${inputs.team_a.value}' and away_goals < home_goals then 'L'
        else 'D'
    end as result_a
from meetings
order by match_date desc
```

<DataTable data={h2h_meetings} rows=5>
  <Column id=season_label title="Season"/>
  <Column id=match_date title="Date"/>
  <Column id=home_team_name title="Home"/>
  <Column id=score title="Score"/>
  <Column id=away_team_name title="Away"/>
  <Column id=result_a title="Result (A)"/>
</DataTable>


## The Pichichi Race

The Pichichi goes to La Liga's top scorer each season, an award given by the newspaper Marca and named after the Athletic Club striker Rafael "Pichichi" Moreno. Below are the current season's leading scorers by goals, refreshed every Thursday.

```sql top_scorers
select * from src_fct_top_scorers
order by scorer_rank
```

<DataTable data={top_scorers} rows=5>
  <Column id=scorer_rank title="#"/>
  <Column id=player_name title="Player"/>
  <Column id=team_name title="Team"/>
  <Column id=nationality title="Nationality"/>
  <Column id=age title="Age"/>
  <Column id=goals title="Goals"/>
</DataTable>

