import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

above_median = pd.read_csv("datas/above_median.csv")
below_median = pd.read_csv("datas/below_median.csv")

print("Above-median group Save% summary:")
print(above_median["Save%"].describe())

print("\nBelow-median group Save% summary:")
print(below_median["Save%"].describe())

print("\nAbove-median mean Save%:", above_median["Save%"].mean())
print("Above-median median Save%:", above_median["Save%"].median())
print("Above-median standard deviation:", above_median["Save%"].std())

print("\nBelow-median mean Save%:", below_median["Save%"].mean())
print("Below-median median Save%:", below_median["Save%"].median())
print("Below-median standard deviation:", below_median["Save%"].std())

plt.figure(figsize=(8, 6))
plt.boxplot(
    [below_median["Save%"], above_median["Save%"]],
    tick_labels=["Below-median SoTA/90", "Above-median SoTA/90"],
)
plt.ylabel("Save Percentage (%)")
plt.title("Save Percentage by Shots on Target Faced per 90 Minutes")
plt.savefig("datas/savepct_boxplot.png", dpi=150, bbox_inches="tight")
print("\nSaved boxplot: datas/savepct_boxplot.png")