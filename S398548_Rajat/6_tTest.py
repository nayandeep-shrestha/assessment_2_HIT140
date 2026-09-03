import pandas as pd
import numpy as np
from scipy import stats
from pathlib import Path

script_dir=Path(__file__).resolve().parent
alpha=0.05

sample=pd.read_csv(script_dir/'sample_worldcup2026_passing.csv')

winner=sample[sample['Result_category']=="Winner"]['Passing_Accuracy']
loser=sample[sample['Result_category']=="Loser"]['Passing_Accuracy']

#olve basic sats for each sample
n1,n2=len(winner), len(loser)
mean1,mean2=winner.mean(),loser.mean()
s1,s2=winner.std(ddof=1),loser.std(ddof=1)

print("---Basic stats----")
print(f"Winner:n={n1}, mean{mean1:.2f}%, s={s1:.2f}")
print(f"Loser: n={n2}, mean{mean2:.2f}% s={s2:.2f}")

#t-statistics, using the two-sample formula
se=np.sqrt((s1**2/n1)+(s2**2/n2))
t_stat=(mean1-mean2)/se

#conservative degree of freedom--the smaller of the two samples own df
df=min(n1-1,n2-2)

print(f'\n----t-statistics----')
print(f'standard error={se:.4f}')
print(f't*={t_stat:.3f}')
print(f"df (conservative, samller of n1-1,n2-1)={df}")

#precise p-calue via software, two-tailed since Ha is mu1!=mu2
p_value=2*stats.t.sf(abs(t_stat),df)

print(f"\n----p-value----")
print(f"two-tailed p-calue={p_value:.4f}")

#conclusion
print(f'\n---Conclusion---')
print("H0:mu_winner=mu_loser")
print(f"ha:mu_winner!=mu_loser(two-tailed,alpha={alpha})")
if p_value<=alpha:
    print(f"p-value({p_value:.4f})<=alpha{(alpha)}-> Reject H0")
    print("There is enough evidence to conclude that avergae passing accuracy differs between winning and losing teams at the FIFA world Cup 2026.")
else:
    print("p-value({p_value:.4f})>alpha({alpha})-> Faile to Reject H0")
    print("Ther is not enough evidence to conclude that average passing accuracy differs between winning and losing teams at the FIFA World Cup 2026.")

#Save 
results = pd.DataFrame([{
    "winner_mean": round(mean1, 2),
    "loser_mean": round(mean2, 2),
    "winner_n": n1,
    "loser_n": n2,
    "t_statistic": round(t_stat, 3),
    "degrees_of_freedom": df,
    "p_value": round(p_value, 4),
    "alpha": alpha,
    "significant": p_value <= alpha,
}])
results.to_csv(script_dir/'ttest_results.csv',index=False)
print("\n Saved")
    


