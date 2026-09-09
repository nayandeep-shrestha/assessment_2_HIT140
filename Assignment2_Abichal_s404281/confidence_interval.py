import numpy as np
import pandas as pd
from scipy import stats

above_median = pd.read_csv("datas/above_median.csv")
below_median = pd.read_csv("datas/below_median.csv")

above = above_median["Save%"]
below = below_median["Save%"]

#95% CI for each group's mean Save%; separately.
above_mean = above.mean()
above_sem = stats.sem(above)
above_ci = stats.t.interval(
    confidence=0.95, df=len(above) - 1, loc=above_mean, scale=above_sem
)

below_mean = below.mean()
below_sem = stats.sem(below)
below_ci = stats.t.interval(
    confidence=0.95, df=len(below) - 1, loc=below_mean, scale=below_sem
)

print("Above-median mean Save%:", above_mean, "| 95% CI:", above_ci)
print("Below-median mean Save%:", below_mean, "| 95% CI:", below_ci)

#95% CI for the DIFFERENCE in means.
n1, n2 = len(above), len(below)
mean1, mean2 = above.mean(), below.mean()
var1, var2 = above.var(), below.var()

mean_difference = mean1 - mean2
se = np.sqrt((var1 / n1) + (var2 / n2))

dof = ((var1 / n1) + (var2 / n2)) ** 2 / (
    ((var1 / n1) ** 2 / (n1 - 1)) + ((var2 / n2) ** 2 / (n2 - 1))
)

t_critical = stats.t.ppf(0.975, dof)
margin_of_error = t_critical * se

ci_lower = mean_difference - margin_of_error
ci_upper = mean_difference + margin_of_error

print("\nDifference in mean Save% (above - below):", mean_difference)
print("Welch degrees of freedom:", dof)
print("95% Confidence Interval for the difference:")
print("Lower:", ci_lower)
print("Upper:", ci_upper)