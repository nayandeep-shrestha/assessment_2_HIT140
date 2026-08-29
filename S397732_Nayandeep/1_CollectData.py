"""
Data Collection Script

Analytic Question: Is there a significant difference in the average Total fouls committed per match 
(both team combined) between group stage and knockout matched at FIFA World Cup 2026?

Data source: FBref.com (via `soccerdata` package, which handles FBref's anti-bot measures, caching,
and rate limiting for you )
"""

import soccerdata as sd

# Initialise the FBref scraper for the World Cup 2026 tournament
fbref = sd.FBref(leagues= "INT-World Cup", seasons="2026")

#Pull Team match stats -- misc stats includes fouls + round
misc_stats= fbref.read_team_match_stats(stat_type="misc")
misc_stats= misc_stats.reset_index()

#FBref returns MultiIndex columns for grouped stats, so flatted these into single strings
# like 'Performance_Fls'
misc_stats.columns = [
    "_".join([str(lvl) for lvl in col if lvl]) if isinstance(col, tuple) else col
    for col in misc_stats.columns
]

print("Flattened columns:", misc_stats.columns.tolist())
print(f"\n Collected {len(misc_stats)} raw team-match rows (includes "
      f"qualifiers - these are filtered out in the next script).")

# Save the raw data
misc_stats.to_csv("raw_team_match_misc_stats.csv", index=False)
print("Saved")