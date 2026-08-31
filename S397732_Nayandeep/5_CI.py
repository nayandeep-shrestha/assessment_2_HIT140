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
          f"Fouls per Match\n (FIFA World Cup 2026, sample n=60)")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
plt.savefig("confidence_intervals_plot.png", dpi=150)
print("\n Saved")
plt.close()


# CI for the difference in means
group_stage_vals = sample[sample["Stage"] == "Group Stage"]["Total_Fouls"]
knockout_vals = sample[sample["Stage"] == "Knockout"]["Total_Fouls"]

n1,n2 = len(knockout_vals), len(group_stage_vals)
mean_diff = knockout_vals.mean() - group_stage_vals.mean()

pooled_var = (((n1 -1) * knockout_vals.var(ddof=1) +
              (n2 -1) * group_stage_vals.var(ddof=1)) / (n1 +n2 -2))
se_diff = np.sqrt(pooled_var * (1/n1 + 1/n2))

diff_df = n1 + n2 -2
diff_t_critical = stats.t.ppf(1 - (1 - CONFIDENC_LEVEL) / 2, diff_df)
diff_margin = diff_t_critical * se_diff

diff_lower, diff_upper = mean_diff - diff_margin, mean_diff + diff_margin

print(f"\n --- {int(CONFIDENC_LEVEL*100)}% Confidence Interval for the Difference in means ---")
print(f"Mean difference = {mean_diff:.2f}")
print(f"Pooled SE = {se_diff:.3f}, df= {diff_df},"
      f"t_critical = {diff_t_critical:.3f}")
print(f"95% CI for the difference: [{diff_lower:.2f}], {diff_upper:.2f}")

includes_zero = diff_lower <= 0 <= diff_upper
if includes_zero:
    print("\n The interval INCLUDES 0 -> consistent with a non-significant t-test result")
else:
    print("\n The interval EXCLUDES 0 -> consistent with a significant t-test result")

diff_result = pd.DataFrame([{
    "mean_difference": round(mean_diff, 2),
    "se": round(se_diff, 3),
    "df": diff_df,
    "ci_lower": round(diff_lower, 2),
    "ci_upper": round(diff_upper, 2),
    "includes_zero": includes_zero,
}])
diff_result.to_csv("ci_difference_of_means.csv", index=False)
print("\n Saved")
