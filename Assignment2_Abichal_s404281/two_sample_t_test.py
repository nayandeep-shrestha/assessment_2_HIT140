import pandas as pd
from scipy import stats

above_median = pd.read_csv("datas/above_median.csv")
below_median = pd.read_csv("datas/below_median.csv")

above = above_median["Save%"]
below = below_median["Save%"]

# Welch's two-sample t-test.
t_stat, p_value = stats.ttest_ind(above, below, equal_var=False)

print("t-statistic:", t_stat)
print("p-value:", p_value)

alpha = 0.05
if p_value < alpha:
    print("Reject the null hypothesis.")
    print("There is a statistically significant difference in average Save%.")
else:
    print("Fail to reject the null hypothesis.")
    print("There is no statistically significant difference in average Save%.")

mean_difference = above.mean() - below.mean()
print("\nDifference in mean Save% (above - below):", mean_difference)