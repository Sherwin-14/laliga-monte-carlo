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

## The Pichichi Race

La Liga's golden boot — current-season scorers ranked by goals.

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
