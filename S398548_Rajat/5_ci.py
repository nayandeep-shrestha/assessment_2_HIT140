import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
from pathlib import Path

script_dir=Path(__file__).resolve().parent
confidence_level=0.95

sample=pd.read_csv(script_dir/ 'sample_worldcup2026_passing.csv')

#Compute a t-bases CI for one group
def confidence_interval(data:pd.Series, confidence:float=0.95)-> dict:
    n=data.count()
    mean=data.mean()
    std=data.std(ddof=1)
    se=std/np.sqrt(n)

    df=n-1
    alpha=1-confidence
    t_critical=stats.t.ppf(1-alpha/2,df)
    
    margin_of_error=t_critical*se
    lower=mean-margin_of_error
    upper=mean+margin_of_error

    return{
        'n':n,
        "mean":round(mean,2),
        'std_dev':round(std,2),
        'std_error': round(se,3),
        'df':df,
        't_critical':round(t_critical,3),
        'margin_of_error':round(margin_of_error,2),
        'ci_lower':round(lower,2),
        'ci_upper':round(upper,2),
    }
results={}
for category in ["Winner", "Loser"]:
    subset=sample[sample["Result_category"]==category]["Passing_Accuracy"]
    results[category]=confidence_interval(subset, confidence_level)

ci_table=pd.DataFrame(results).T
print(f"{int(confidence_level*100)}% Confidence Interval for population" f"mean Passing_Accuracy\n")
print(ci_table)

ci_table.to_csv(script_dir/'confidence_intervals.csv')
print('\nSaved confidence_intervals.csv')

#Visualization of two confidence intervals
plt.figure(figsize=(7,5))
categories=list(results.keys())
means=[results[c]["mean"]for c in categories]
errors=[results[c]["margin_of_error"]for c in categories]

plt.errorbar(
    categories, means, yerr=errors, fmt='o', markersize=10, capsize=8, color="#2a78d6", ecolor="#52514e", elinewidth=2, capthick=2,
)
plt.ylabel("mean passing accuracy(%)")
plt.title(f"{int(confidence_level*100)}% confidence interval for mean passing" f'Accuracy\n(FIFA World Cup 2026, sample n=80)')
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig(script_dir/'confidence_intervals_plot.png', dpi=150)
print("Saved confidence_intervals_plot.png")
plt.close()

#CI for the difference in mean (Winner - Loser)
winner_vals=sample[sample['Result_category']=="Winner"]["Passing_Accuracy"]
loser_vals=sample[sample["Result_category"]=="Loser"]["Passing_Accuracy"]

n1,n2 = len(winner_vals),len(loser_vals)
mean_diff=winner_vals.mean()-loser_vals.mean()

pooled_var=(((n1-1)* winner_vals.var(ddof=1)+
             (n2-1)*loser_vals.var(ddof=1))/(n1+n2-2))
se_diff=np.sqrt(pooled_var*(1/n1+1/n2))

diff_df=n1+n2-2
diff_t_critical=stats.t.ppf(1-(1-confidence_level)/2, diff_df)
diff_margin=diff_t_critical*se_diff

diff_lower, diff_upper = mean_diff-diff_margin, mean_diff+diff_margin

print(f'n{int(confidence_level*100)}% confidence intervals for the difference in means ')
print("Mean difference(Winner- Loser)={mean_diff:.2f}percentage points")
print(f"Pooled SE={se_diff:.3f},df={diff_df}, t_critical={diff_t_critical:.3f}")
print(f"95% CI for the difference:[{diff_lower:.2f},{diff_upper:.2f}]")

includes_zero=diff_lower<=0 <=diff_upper
if includes_zero:
    print("\n The interval includes 0 i.e consistent with a non-signifincat t-test result")
else:
    print("\n The interval excludes 0 i.e consistent with a signifincat t-test result")

diff_result=pd.DataFrame([{
    'mean_difference':round(mean_diff,2),
    'se':round(se_diff,3),
    'df':diff_df,
    'ci_lower':round(diff_lower,2),
    'ci_upper': round(diff_upper,2),
    'includes_zero':includes_zero,
}])
diff_result.to_csv(script_dir/ 'ci_difference_of_means.csv', index=False)
print("\nSaved ci_difference_of_means.csv")