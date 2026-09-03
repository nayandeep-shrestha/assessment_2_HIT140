import pandas as pd

raw = pd.read_csv('raw_team_match_passing_stats.csv')
print("raw data shape:", raw.shape)
print("\ncolumn dtypes before cleaning:")
print(raw.dtypes)

# ---------handling missing values
key_cols = ["Match", "TEAM", "OPPONENT", "STAGE",
            'RESULT', 'PASSES COMPLETED', 'PASSES ATTEMPTED']
missing_summary = raw[key_cols].isna().sum()
print('\nMissing calues per key columns:')
print(missing_summary)

before = len(raw)
raw = raw.dropna(subset=key_cols)
print(
    f'n\Dropped {before - len(raw)} rows with missing key values ({len(raw)} rows remain)')

# -------------Passing figures should be numeric--------------#

raw['PASSES COMPLETED'] = pd.to_numeric(
    raw['PASSES COMPLETED'], errors='coerce')
raw['PASSES ATTEMPTED'] = pd.to_numeric(
    raw['PASSES ATTEMPTED'], errors="coerce")

before = len(raw)
raw = raw.dropna(subset=["PASSES COMPLETED", "PASSES ATTEMPTED"])
print(f"Dropped {before - len(raw)} rows where passing figures weren't numeric ({len(raw)} rows remain)")

# Guardd against a divide-by-zero, and agaisnt completed > attempted(impossible/ data-entry error)
before = len(raw)
raw = raw[raw["PASSES ATTEMPTED"] > 0]
print(
    f"Dropped {before - len(raw)} rows with 0 passes attempted ({len(raw)} rows remain)")

before = len(raw)
raw = raw[raw["PASSES COMPLETED"] <= raw["PASSES ATTEMPTED"]]
print(f"Droppes {before - len(raw)} rows where completed passes exceede attempted" f"data-entry errors) ({len(raw)} rows remain)")

# -------Removing duplicate rows-----------#
before = len(raw)
raw = raw.drop_duplicates(subset=["Match", "TEAM"])
print(f"Dropped {before-len(raw)} duplicate team-match rows.")

# ---checking if every match has two rows-------_#

team_counts = raw.groupby("Match")["TEAM"].count()
incomplete_matches = team_counts[team_counts != 2].index.tolist()
if incomplete_matches:
    print(f'\n Warning: {len(incomplete_matches)} match do not have exactly 2 team rows.'f'dropping these to keep the winner/loser valid.')
    raw = raw[~raw["Match"].isin(incomplete_matches)]

# ---------------Derive result category------------#
result_map = {"W": "Winner", "L": "Loser", "D": "Draw"}
raw["Result_category"] = raw["RESULT"].map(result_map)

unmapped = raw["Result_category"].isna().sum()
if unmapped:
    print(
        f'\nWarning:{unmapped}rows had a result value other than W\L\D and were dropped')
    raw = raw.dropna(subset=["Result_category"])

print('\nResult_category counts before dropping draws:')
print(raw["Result_category"].value_counts())

before = len(raw)
raw = raw[raw["Result_category"].isin(["Winner", "Loser"])]
print(f"\nDropped {before - len(raw)} draw rows -- this analysis only compares decisive " f"Winner vs Loser outcomes ({len(raw)} rows remain).")

# ---------Compute passing accuracy------------------#
raw["Passing_Accuracy"] = (raw["PASSES COMPLETED"] /
                           raw["PASSES ATTEMPTED"])*100
wrangled = raw[[
    "Match", "TEAM", 'OPPONENT', 'STAGE', 'Result_category',
    "PASSES COMPLETED", 'PASSES ATTEMPTED', 'Passing_Accuracy',
]].rename(columns={
    "Match": 'match_id',
    'TEAM': 'team',
    'OPPONENT': 'opponent',
    'STAGE': 'stage',
    'PASSES COMPLETED': 'passes_completed',
    "PASSES ATTEMPTED": 'passes_attempted',
}).reset_index(drop=True)

# -----------SAVING----------_#

print('\n ---- FINAL WRANGLED DATASET-----')
print('Shape :', wrangled.shape)
print('\nDtpyes:')
print(wrangled.dtypes)
print('\nMissing values:')
print(wrangled.isna().sum())
print('\n Rows per Result_category:')
print(wrangled["Result_category"].value_counts())
print("\nRows per stage:")
print(wrangled["stage"].value_counts())
print("\nSample rows:")
print(wrangled.head(10))

wrangled.to_csv("wrangled_worldcup2026_passing.csv", index=False)
print(
    f'\nSAved {len(wrangled)} team-match rows to wrangled_worldcup2026_passing.csv')
