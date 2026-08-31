import pandas as pd
import matplotlib.pyplot as plt

# Loading the sample
sample = pd.read_csv("sample_worldcup2026_fouls.csv")
print("Sample shape: ", sample.shape)
print(sample.groupby("Stage")["Total_Fouls"].count())

# Computing descriptive statistics per group
def describe_group(data: pd.Series) -> pd.Series:
    return pd.Series({
        "n": data.count(),
        "mean": data.mean(),
        "median": data.median(),
        "mode": data.mode().iloc[0] if not data.mode().empty else float("nan"),
        "std_dev": data.std(),
        "variance": data.var(),
        "min": data.min(),
        "max": data.max(),
        "range": data.max()- data.min(),
        "Q1": data.quantile(0.25),
        "Q3": data.quantile(0.75),
        "IQR": data.quantile(0.75) - data.quantile(0.25),
        "skewness": data.skew(),
    })

summary = sample.groupby("Stage")["Total_Fouls"].apply(describe_group).unstack()
summary = summary.round(2)

print("\n --- Descriptive statistics summary ---")
print(summary)

summary.to_csv("descriptive_stats_summary.csv")
print("\n Saved")


# Visualize boxplot comparing the two groups
plt.figure(figsize=(7,5))
groups = ["Group Stage", "Knockout"]
data_to_plot = [sample[sample["Stage"] == g]['Total_Fouls'] for g in groups]
plt.boxplot(data_to_plot, labels=groups, showmeans=True)
plt.ylabel("Total fouls per match (both teams combined)")
plt.title("Distribution of Total Fouls per match: Group Stage vs Knockout\n(FIFA World Cup 2026, sample n=60)")
plt.grid(axis="y", alpha = 0.3)
plt.tight_layout()
plt.savefig("boxplot_fouls_by_stage.png", dpi = 150)
print("Saved boxplot visual")
plt.close()

#Visualize - histograms for each group
fig, axes = plt.subplots(1,2, figsize=(11, 5), sharey=True)
for ax, g, color in zip(axes, groups, ["#2a78d6", "#eb6834"]):
    subset = sample[sample["Stage"] == g]['Total_Fouls']
    ax.hist(subset, bins=8, color= color, edgecolor = 'white', alpha = 0.85)
    ax.axvline(subset.mean(), color="black", linestyle="--", linewidth=1.5, label=f"Mean = {subset.mean():.1f}")
    ax.set_title(g)
    ax.set_xlabel("Total fouls per match")
    ax.legend()
axes[0].set_ylabel("Frequency")
fig.suptitle("Histogram of Total Fouls per Match by Stage")
plt.tight_layout()
plt.savefig("histogram_fouls_by_stage.png", dpi=150)
print("Saved")
plt.close()

