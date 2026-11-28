---
title: The Pichichi Race
---

La Liga's golden boot — current-season scorers ranked by goals.

```sql top_scorers
select * from src_fct_top_scorers
order by scorer_rank
```

<DataTable data={top_scorers} rows=5>
  <Column id=scorer_rank title="#"/>
  <Column id=player_name title="Player"/>
  <Column id=team_name title="Team"/>
  <Column id=goals title="Goals"/>
</DataTable>
