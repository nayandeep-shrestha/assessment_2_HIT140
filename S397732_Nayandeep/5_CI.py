import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

CONFIDENC_LEVEL = 0.95

sample = pd.read_csv("sample_worldcup2026_fouls.csv")

# Comput a t-based CI for each stage
def confidence_interval(data: pd.Series, confidence: float = 0.95) -> dict:
    n= data.count()
    mean= data.mean()
    std = data.std(ddof=1)
    se = std / np.sqrt(n)

    df = n-1
    alpha = 1 - confidence
    t_critical = stats.t.ppf(1 - alpha /2, df)

    margin_of_error = t_critical * se
    lower = mean - margin_of_error
    upper = mean + margin_of_error

    return {
        "n" : n,
        "mean": round(mean,2),
        "std_dev": round(std, 2),
        "std_error": round(se, 3),
        "df": df,
        "t_critical": round(t_critical, 3),
        "margin_of_error": round(margin_of_error, 2),
        "ci_lower": round(lower, 2),
        "ci_upper": round(upper, 2),
    }

results = {}
for stage in ["Group Stage", "Knockout"]:
    subset = sample[sample["Stage"] == stage]["Total_Fouls"]
    results[stage] = confidence_interval(subset, CONFIDENC_LEVEL)

ci_table = pd.DataFrame(results).T
print(f" ---- {int(CONFIDENC_LEVEL*100)}% Confidence Intervals for population"
      f"mean Total_Fouls per mathc ----\n")
print(ci_table)

ci_table.to_csv("confidenve_intervals.csv")
print("\n Saved")

# Visualize the two confidence intervals
plt.figure(figsize=(7,5))
stages = list(results.keys())
means = [results[s]["mean"] for s in stages]
errors = [results[s]["margin_of_error"] for s in stages]

plt.errorbar(
    stages, means, yerr=errors, fmt="o", markersize=10, capsize=8,
    color="#2a78d6", ecolor= "#52514e", elinewidth=2, capthick=2,
)
plt.ylabel("Mean total fouls per match")
plt.title(f"{int(CONFIDENC_LEVEL*100)}% Confidence Intervals for Mean Total "
          f"Fouls per Match\n (FIFA World Cup 2026, sample n=30 per group)")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("confidence_intervals_plot.png", dpi=150)
print("\n Saved")
plt.close()
