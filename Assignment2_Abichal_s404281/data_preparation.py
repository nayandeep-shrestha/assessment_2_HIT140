import pandas as pd

cleaned_df = pd.read_csv("datas/wrangled_primary_gk_stats.csv")

print(cleaned_df.head())
print(cleaned_df.shape)
print(cleaned_df.columns.tolist())


# Keeping only the variables needed for the analysis.
analysis_df = cleaned_df[["Player", "Squad", "SoTA_per90", "Save%"]].copy()

print("\nAnalysis-ready data shape:", analysis_df.shape)
print("Missing values:")
print(analysis_df.isnull().sum())

print("\nFinal number of observations:", len(analysis_df))
print("Final number of teams:", analysis_df["Squad"].nunique())
print("Duplicate teams:", analysis_df["Squad"].duplicated().sum())

analysis_df.to_csv("datas/analysis_stats.csv", index=False)
print("\nSaved checkpoint: datas/analysis_stats.csv")