import pandas as pd
import numpy as np


df = pd.read_csv("datas/goalkeeper_stats.csv", header=1)

print("First 5 rows:")
print(df.head())

print("\nDataset shape (rows, columns):")
print(df.shape)

print("\nColumn names:")
print(df.columns.tolist())

print("\nDataset info:")
print(df.info())

print("\nMissing values per column:")
print(df.isnull().sum())


df.to_csv("datas/raw_stats.csv", index=False)
print("\nSaved checkpoint: datas/raw_stats.csv")