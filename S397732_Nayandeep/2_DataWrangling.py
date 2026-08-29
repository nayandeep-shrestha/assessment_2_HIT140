import pandas as pd

#Load the raw data collected in 1_CollectData.py
raw = pd.read_csv("raw_team_match_misc_stats.csv")
print("raw data shape:", raw.shape)
print("\n Column dtypes before cleaning:")
print(raw.dtypes)

foul_col = [c for c in raw.columns if "Fls" in c][0]
print(f"\nUsing '{foul_col}' as the fouls-committed column.")

# FBref sometimes returns an entirely blank 'team'column depending on how the index was
# structured internally. It isn't needed for this analysis, so we  don't rely on it, but
# flag it here
if raw["team"].isna().all():
    print("\n NOTE: 'team' column is entirely blank in this scrape. Not a problem" \
    "for this analysis (we use 'opponent' + 'match_report' instead)")

# 'date' arrives as text from the CSV; fouls should be numeric
raw["date"] = pd.to_datetime(raw["date"], errors="coerce")
raw[foul_col] = pd.to_numeric(raw[foul_col], errors="coerce")

# Handling missing values
missing_summary = raw[["opponent", 'date', 'round', 'match_report', foul_col]].isna().sum()
print("\nMIssing values per key columns:")
print(missing_summary)

before = len(raw)
raw = raw.dropna(subset=[ 'date', 'round', 'match_report', foul_col])
print(f"\n Dropped {before - len(raw)} rows with missing key values"
      f"({len(raw)} rows remain)")

#Removing Duplicate rows
before = len(raw)
raw = raw.drop_duplicates(subset=['match_report', 'opponent'])
print(f"Dropped {before - len(raw)} duplicate team-match rows.")

# Filtering scope to the actual final tournament
Tournament_start = "2026-06-11"
Tournament_end = "2026-07-19"

before = len(raw)
raw = raw[(raw['date'] >= Tournament_start) & (raw['date'] <= Tournament_end)]
print(f"\n Dropped {before - len(raw)} qualifier rows;"
      f"{len(raw)} rows remain from the final tournament")

print("\, Rounds present after filtering:",raw['round'].value_counts())

# Derive 'stage variable'
def classify_stage(round_name: str) -> str:
    if isinstance(round_name, str) and 'group' in round_name.lower():
        return 'Group Stage'
    return "Knockout"

raw['Stage'] = raw['round'].apply(classify_stage)

# REshape - aggregate two team-rows per match into one match-row
team_counts = raw.groupby('match_report')[foul_col].count()
incomplete_matches = team_counts[team_counts != 2].index.tolist()
if incomplete_matches:
    print(f"\n Warning: {len(incomplete_matches)} match(es) do not haave exactly 2 team rows. Dropping tese to keep totals valid")
    raw = raw[~raw['match_report'].isin(incomplete_matches)]

wrangled = (
    raw.groupby(['match_report', 'round', 'date', 'Stage'], as_index= False)[foul_col]
    .sum()
    .rename(columns ={foul_col: 'Total_Fouls'})
)

# Saving
print("\n ---- Finall wrangled dataset ----")
print("Shape:", wrangled.shape)
print("\n Dtypes:", wrangled.dtypes)
print("\n Missing values:", wrangled.isna().sum())
print("\n Matches per stage:", wrangled["Stage"].value_counts())
print("\n Sample rows:")
print(wrangled.head(10))

wrangled.to_csv("wrangled_worldcup2026_fouls.csv", index=False)
print(f"\n Saved {len(wrangled)} match-level rowsj")