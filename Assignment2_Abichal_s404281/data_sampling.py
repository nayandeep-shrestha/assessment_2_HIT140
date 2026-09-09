import pandas as pd

analysis_df = pd.read_csv("datas/analysis_stats.csv")

median_sota_per90 = analysis_df["SoTA_per90"].median()
print("Median SoTA per 90:", median_sota_per90)

above_median = analysis_df[analysis_df["SoTA_per90"] > median_sota_per90].copy()
below_median = analysis_df[analysis_df["SoTA_per90"] < median_sota_per90].copy()

print("\nAbove-median group shape:", above_median.shape)
print("Below-median group shape:", below_median.shape)

print("\nAbove-median group:")
print(above_median[["Player", "SoTA_per90", "Save%"]])

print("\nBelow-median group:")
print(below_median[["Player", "SoTA_per90", "Save%"]])

above_median.to_csv("datas/above_median.csv", index=False)
below_median.to_csv("datas/below_median.csv", index=False)
print("\nSaved checkpoints: datas/above_median.csv, datas/below_median.csv")