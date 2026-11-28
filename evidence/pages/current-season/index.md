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

```sql next_fixtures
select * from src_fct_upcoming_fixtures
order by match_date
```

<DataTable data={next_fixtures} rows=10>
  <Column id=matchday title="MD"/>
  <Column id=status title="Status"/>
  <Column id=match_date title="Date"/>
  <Column id=kickoff_madrid title="Kickoff (Madrid)"/>
  <Column id=kickoff_utc title="Kickoff (UTC)"/>
  <Column id=home_team_name title="Home"/>
  <Column id=away_team_name title="Away"/>
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
