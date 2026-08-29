import pandas as pd

RANDOM_SEED = 42
SAMPLE_SIZE_PER_GROUP = 30

# Loading the wrangled data
wrangled = pd.read_csv("wrangled_worldcup2026_fouls.csv")

analysis_vars = wrangled[['match_report', 'round', 'date', 'Stage', 'Total_Fouls']]

# Defining populations
population_group = analysis_vars[analysis_vars['Stage'] == 'Group Stage']
population_knockout = analysis_vars[analysis_vars['Stage'] == 'Knockout']

print("---- Population sizes ----")
print(f"Group Stage Population: N = {len(population_group)} matches")
print(f"Knockout Population: N = {len(population_knockout)} matches")

print("\n --- Population parameters ---")
print(f"Group Stage: mean = {population_group['Total_Fouls'].mean():.2f}, "
      f"std = {population_group['Total_Fouls'].std():.2f}")
print(f"Knocknout : mean = {population_knockout['Total_Fouls'].mean():.2f}, "
      f"std = {population_knockout['Total_Fouls'].std():.2f}")

# Draw the samples using Simple Random Sampling
sample_group = population_group.sample(
    n= SAMPLE_SIZE_PER_GROUP, random_state=RANDOM_SEED, replace=False
)
sample_knockout = population_group.sample(
    n=SAMPLE_SIZE_PER_GROUP, random_state=RANDOM_SEED, replace=False
)

sample = pd.concat([sample_group, sample_knockout], ignore_index=True)

# Quick Sanity chekc on the sample
print("\n --- Sample Sizes ---")
print(sample["Stage"].value_counts())

print("\n --- Sample means (Total_Fouls) - quick check against population ---")
print(sample.groupby("Stage")["Total_Fouls"].mean().round(2))

# Saving
sample.to_csv("sample_worldcup2026_fouls.csv", index=False)
print(f"\n Saved {len(sample)} sampled rows")