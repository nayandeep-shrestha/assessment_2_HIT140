import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

script_dir=Path(__file__).resolve().parent

#Loading the sample
sample=pd.read_csv(script_dir/ "sample_worldcup2026_passing.csv")
print("Sample shape:",sample.shape)
print(sample.groupby("Result_category")["Passing_Accuracy"].count())

#Computing decrriptive statistics per group
def describe_group(data: pd.Series) -> pd.Series:
    return pd.Series({
        "n":data.count(),
        'mean':data.mean(),
        'median':data.median(),
        'mode':data.median(),
        'mode':data.mode().iloc[0] if not data.mode().empty else float('nan'),
        'std_dev':data.std(),
        'variance':data.var(),
        'min':data.min(),
        'max':data.max(),
        'range':data.max()-data.min(),
        'Q1':data.quantile(0.25),
        'Q3':data.quantile(0.75),
        'IQR':data.quantile(0.75)-data.quantile(0.25),
        'skewness': data.skew(),
    })

summary= sample.groupby("Result_category")["Passing_Accuracy"].apply(describe_group).unstack()
summary=summary.round(2)

print('\n---DEscriptive statistics summary----')
print(summary)

summary.to_csv(script_dir/'decriptive_stats_summary.csv')
print('\nSaved decriptive_stats_summary.csv')

# Visualisation of boxplot comparing the two groups
plt.figure(figsize=(7,5))
groups=['Winner','Loser']
data_to_plot=[sample[sample['Result_category'] == g]["Passing_Accuracy"]for g in groups]
plt.boxplot(data_to_plot, tick_labels=groups, showmeans=True)
plt.ylabel("Passing accuracy per team-match(%)")
plt.title("Distribution of passing accuracy: Winners vs Losers\n(FIFA World Cup 2026, sample n=80)")
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(script_dir/ 'boxplot_pasing_by_result.png', dpi=150)
print("Saved boxplot_passing_by_result.png")
plt.close()

#Visualisation of histograms for each group
fig, axes = plt.subplots(1,2, figsize=(11,5), sharey=True)
for ax, g, color in zip(axes, groups, ["#2a78d6",'#eb6834']):
    subset=sample[sample['Result_category'] == g]['Passing_Accuracy']
    ax.hist(subset, bins=8, color=color, edgecolor='white', alpha=0.85)
    ax.axvline(subset.mean(),color='black',linestyle='--',linewidth=1.5, label=f"Mean={subset.mean():.1f}%")
    ax.set_title(g)
    ax.set_xlabel("Passing accuracy (%)")
    ax.legend()

axes[0].set_ylabel('Frequency')
fig.suptitle('Histogram of Passing Accuracy per Team-Match by Result')
plt.tight_layout()
plt.savefig(script_dir/'histogram_passing_by_result.png', dpi=150)
print("Saved histogarms_passing_by_result.png")
plt.close()