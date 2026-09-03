"""
Data Collection Script
 
Analytic Question: Is there a significant difference in average team passing accuracy (%)
between winning teams and losing teams at the FIFA World Cup 2026 ?

The dataset was built by taking a mix of an already available public GitHub repository 
and FIFA's official statistics of World Cup matches. The code that has been developed was extracted from the GitHub repository. 
There is a 104 match list for the FIFA World Cup 2026, which is used to identify the matches and teams. Passing statistics, 
Passes completed and passes attempted data was then manually collected and entered, including. 
As provided in FIFA's official match reports. This resulted in 208 team-match records, with two records for each match. 
Data that is included in the final data set are Match	TEAM	OPPONENT	STAGE	RESULT	PASSES COMPLETED	PASSES ATTEMPTED. 
Each team gets a result as a W, L, or D (from their point of view); penalty-shootout results as a W, L, or D are recorded. 
Scored as victories and defeats of the two teams.

"""
import pandas as pd
RAW_FILE="world_cup_2026_team_matches.csv"

raw=pd.read_csv(RAW_FILE)

print(f"Loaded{RAW_FILE}")
print("shape:", raw.shape)
print("\ncolumns:",raw.columns.tolist())
print("\nFirst few rows:")
print(raw.head())
print("\nDtypes:")
print(raw.dtypes)

print("\nMatches represented (unique Match id):", raw["Match"].nunique())
print("Team-match rows per Match id (should all be 2):")
print(raw.groupby("Match").size().value_counts())

print("\nStage present:")
print(raw["STAGE"].value_counts())

print("n\Result breakdown by stage (sanity check -- knockout stages should have zero 'D):")
print(pd.crosstab(raw["STAGE"], raw["RESULT"]))

#SAve a copy under the same "raw_" naming convention as the rest of the pripeline, so evert later script
#only ervr read from a file prdocued by the previous step in this folder --
#never straight from the original compiled file.
raw.to_csv("raw_team_match_passing_stats.csv", index=False)
print(f"\nSaved raw_team_match_passing_stats.csv ({len(raw)} team-match rows)")