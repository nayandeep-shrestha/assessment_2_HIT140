import pandas as pd
import numpy as np

df = pd.read_csv("datas/raw_stats.csv")

# Keeping the columns that are relevant to this analytic question.
df = df[
    [
        "Player",
        "Pos",
        "Squad",
        "Starts",
        "Min",
        "90s",
        "SoTA",
        "Saves",
        "Save%",
    ]
].copy()

print("Position counts:")
print(df["Pos"].value_counts())

# Removing goalkeepers who never started a match at the tournament.
df = df[df["Starts"] > 0].copy()
print("\nShape after removing non-starters:", df.shape)

print("\nSquad counts (before reducing to one keeper per squad):")
print(df["Squad"].value_counts())

# Sorting so that, within each squad, the most-started (then most-minutes) goalkeeper appears first.
df = df.sort_values(
    ["Squad", "Starts", "Min"],
    ascending=[True, False, False],
)

# Keeping only the primary (most-used) goalkeeper per squad.
primary_gk = df.groupby("Squad").head(1).copy()
print("\nPrimary goalkeeper shape:", primary_gk.shape)
print("Number of unique squads:", primary_gk["Squad"].nunique())
print("Duplicate squads remaining:", primary_gk["Squad"].duplicated().sum())

# Shots on target faced, standardised per 90 minutes.
primary_gk["SoTA_per90"] = primary_gk["SoTA"] / primary_gk["90s"]

print("\nWrangled data:")
print(primary_gk[["Player", "Squad", "SoTA", "90s", "SoTA_per90", "Save%"]])

primary_gk.to_csv("datas/wrangled_primary_gk_stats.csv", index=False)
print("\nSaved checkpoint: datas/wrangled_primary_gk_stats.csv")