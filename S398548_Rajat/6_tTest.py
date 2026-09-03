import pandas as pd
from scipy import stats
from pathlib import Path

script_dir=Path(__file__).resolve().parent
alpha=0.05

sample=pd.read_csv(script_dir/'sample_worldcup2026_passing.csv')

winner=sample[sample['Result_category']=="Winner"]['Passing_Accuracy']
loser=sample[sample['Result_category']=="Loser"]['Passing_Accuracy']

print(f"Winner: n={len(winner)}, mean={winner.mean():.2f}%, std={winner.std(ddof=1):.2f}")
print(f"Loser: n={len(loser)}, mean={loser.mean():.2f}%, std={loser.std(ddof=1):.2f}")

# Check the equal variance assumption ( Levene's Test)
levene_stat, levene_p = stats.levene(winner, loser)
print(f"\n --- Levene's test for equal variances ---")
print(f"Lvene Statistivs = { levene_stat:.3f}, p-value = {levene_p:.4f}")

equal_var = levene_p >= alpha
if equal_var:
    print(f"p >= {alpha} -> fail to reject equal variances  -> using "
          f"Student's t-test (equal_var= True)")
else:
    print(f"p < {alpha} -> variances significantly different -> using "
          f"Welch's t-test (equal_var=False)")

#Running the two-sample independent t-test
t_stat, p_value = stats.ttest_ind(winner, loser, equal_var=equal_var)

if equal_var:
    df= len(winner) + len(loser) - 2
else:
    v1, n1 = winner.var(ddof=1), len(winner)
    v2, n2 = loser.var(ddof=1), len(loser)
    df = (v1 / n1 +v2 / n2) ** 2 / (
        (v1 / n1) ** 2 / (n1 -1) +(v2/n2) ** 2 / (n2 - 1)
    )

print(f"\n --- Two-sample {'Student' if equal_var else 'Welch'} t-test ---")
print(f"H0: mu_winner = mu_loser")
print(f"H1: mu_winner != mu_loser  (two-tailed, alpha = {alpha})")
print(f"t-statistics = {t_stat:.3f}")
print(f"degrees of freedom = {df:.2f}")
print(f"p-value = {p_value:.4f}")

# Effecct size (Cohen's d)
pooled_std = ((winner.var(ddof=1) * (len(winner) -1) +
               loser.var(ddof=1) * (len(loser) -1)) /
               (len(winner) +len(loser) -2 )) ** 0.5
cohens_d = (winner.mean() - loser.mean()) / pooled_std
print(f"\nEffect size = {cohens_d:.3f}")
if abs(cohens_d) < 0.2:
    effect_label = "negligible"
elif abs(cohens_d) < 0.5:
    effect_label ="small"
elif abs(cohens_d) < 0.8:
    effect_label = "medium"
else:
    effect_label= "large"

print(f"(Interpreted as a {effect_label} effect size)")

# Conclusion
print(f"\n --- Conclusion ---")
if p_value < alpha:
    print(f"p-value ({p_value:.4f}) < alpha ({alpha}) -> Reject H0")
    print(f"There is a statistically significant difference in average passing accuracy between winning an losing teams at the FIFA World Cup 2026 (alpha= {alpha}).")
else:
    print(f"p-value ({p_value:.4f}) >= alpha ({alpha}) -> Fail to Reject H0")
    print(f"There is not enough evidence to conclude a statisticallyy significant difference in avg passing accuracy between winning and losing teams at the FIFA World Cup 2026 (alpha {alpha})."
          f"Any difference observed in this sample could plausibly be due to sampling variability rather than a true underlying difference.")

# Save results
results = pd.DataFrame([{
    "test": "Welch's t-test" if not equal_var else "Student's t-test",
    "winner_mean": round(winner.mean(),2),
    "loser_mean": round(loser.mean(),2),
    "levene_p_value": round(levene_p, 4),
    "t_statistic": round(t_stat, 3),
    "degree_of_freedom": round(df, 2),
    "p_value": round(p_value, 4),
    "alpha": alpha,
    "cohes_d": round(cohens_d, 3),
    "significant": p_value < alpha
}])
results.to_csv(script_dir/"ttest_results.csv", index=False)
print("\n Saved")