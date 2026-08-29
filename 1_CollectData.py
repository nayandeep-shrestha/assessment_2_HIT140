import soccerdata as sd

fbref = sd.FBref(leagues= "INT-World Cup", seasons="2026")

misc_stats= fbref.read_team_match_stats(stat_type="misc")
misc_stats= misc_stats.reset_index()

misc_stats.columns = [
    "_".join([str(lvl) for lvl in col if lvl]) if isinstance(col, tuple) else col
    for col in misc_stats.columns
]

print("Flattened columns:", misc_stats.columns.tolist())
print(f"\n Collected {len(misc_stats)} raw team-match rows (includes "
      f"qualifiers - these are filtered out in the next script).")

misc_stats.to_csv("raw_team_match_misc_stats.csv", index=False)
print("Saved")