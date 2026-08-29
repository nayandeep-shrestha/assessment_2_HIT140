import pandas as pd
from scipy import stats
ALPHA = 0.05

sample= pd.read_csv("sample_worldcup2026_fouls.csv")

group_stage = sample[sample["Stage"] == "Group Stage"]["Total_Fouls"]
knockout = sample[sample["Stage"]== "Knockout"]["Total_Fouls"]

print(f"Group Stage: n={len(group_stage)}, mean={group_stage.mean():.2f},"
      f"std={group_stage.std(ddof=1):.2f}")
print(f"Knockout: n={len(knockout)}, mean={knockout.mean():.2f},"
      f"std={knockout.std(ddof=1):.2f}")

# Check the equal variance assumption ( Levene's Test)
levene_stat, levene_p = stats.levene(group_stage, knockout)
print(f"\n --- Levene's test for equal variances ---")
print(f"Lvene Statistivs = { levene_stat:.3f}, p-value = {levene_p:.4f}")

equal_var = levene_p >= ALPHA
if equal_var:
    print(f"p >= {ALPHA} -> fail to reject equal variances  -> using "
          f"Student's t-test (equal_var= True)")
else:
    print(f"p < {ALPHA} -> variances significantly different -> using "
          f"Welch's t-test (equal_var=False)")

#Run the two-sample independent t-test
t_stat, p_value = stats.ttest_ind(knockout, group_stage, equal_var=equal_var)

if equal_var:
    df= len(group_stage) + len(knockout) - 2
else:
    v1, n1 = group_stage.var(ddof=1), len(group_stage)
    v2, n2 = knockout.var(ddof=1), len(knockout)
    df = (v1 / n1 +v2 / n2) ** 2 / (
        (v1 / n1) ** 2 / (n1 -1) +(v2/n2) ** 2 / (n2 - 1)
    )

print(f"\n --- Two-sample {'Student' if equal_var else 'Welch'} t-test ---")
print(f"H0: mu_group_stage = mu_knockout")
print(f"H1: mu_group_stage != mu_knockout  (two-tailed, alpha = {ALPHA})")
print(f"t-statistics = {t_stat:.3f}")
print(f"degrees of freedom = {df:.2f}")
print(f"p-value = {p_value:.4f}")

# Effecct size (Cohen's d)
pooled_std = ((group_stage.var(ddof=1) * (len(group_stage) -1) +
               knockout.var(ddof=1) * (len(knockout) -1)) /
               (len(group_stage) +len(knockout) -2 )) ** 0.5
cohens_d = (knockout.mean() - group_stage.mean()) / pooled_std
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
if p_value < ALPHA:
    print(f"p-value ({p_value:.4f}) < alpha ({ALPHA}) -> Reject H0")
    print(f"There is a statistically significant difference in average total fouls per match between Group Stage and Knockout matches at the FIFA World Cup 2026 (alpha= {ALPHA}).")
else:
    print(f"p-value ({p_value:.4f}) >= alpha ({ALPHA}) -> Fail to Reject H0")
    print(f"There is not enough evidence to conclude a statisticallyy significant difference in avg total fouls per match between Group Stage and Knockout matches at the FIFA World Cup 2026 (alpha {ALPHA})."
          f"Te higher sample mean observed in Knockout matches could plausibly be due to samplinf variability rather than a true underlying difference.")

# Save results
results = pd.DataFrame([{
    "test": "Welch's t-test" if not equal_var else "Student's t-test",
    "group_stage_mean": round(group_stage.mean(),2),
    "knockout_mean": round(knockout.mean(),2),
    "levene_p_value": round(levene_p, 4),
    "t_stattistic": round(t_stat, 3),
    "degrees_of_freedom": round(df, 2),
    "p_value": round(p_value, 4),
    "alpha": ALPHA,
    "cohes_d": round(cohens_d, 3),
    "significant": p_value < ALPHA
}])
results.to_csv("ttest_results.csv", index=False)
print("\n Saved")