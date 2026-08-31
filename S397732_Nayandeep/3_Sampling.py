import pandas as pd

RANDOM_SEED = 42
SAMPLE_SIZE = 60

# Loading the wrangled data
wrangled = pd.read_csv("wrangled_worldcup2026_fouls.csv")
population = wrangled[["match_report", "round", "date", "Stage", "Total_Fouls"]]

N= len(population)
n_group = (population["Stage"] == "Group Stage").sum()
n_knockout = (population["Stage"] == "Knockout").sum()
print(f"Full Population : N = {N} matches"
      f"({n_group} Group Stage, {n_knockout} Knockot)")

# SRS - Pooled
sample = population.sample(n=SAMPLE_SIZE, random_state=RANDOM_SEED, replace=False)

print(f"\nDrew a pooled SRS of n={SAMPLE_SIZE} from N={N}"
      f" no stratification by Stage")

# Report the resulting stage composition
print(f"\n Resulting stage composition of the sample")
print(sample["Stage"].value_counts())

print("\nSample vs population means (Total_Fouls), for a quick sanity check:")
for stage in ["Group Stage", "Knockout"]:
    pop_mean = population[population["Stage"] == stage]["Total_Fouls"].mean()
    samp_subset = sample[sample["Stage"] == stage]["Total_Fouls"]
    print(f" {stage}: population mean = {pop_mean:.2f},"
          f"sample n = {len(samp_subset)}, sample mean = {samp_subset.mean():.2f}")

# Flag if either subgroup ended up too thin for later steps
counts = sample["Stage"].value_counts()
for stage, count in counts.items():
    if count <30 :
        print(f"\nNote: the {stage} subgroup in this sample has only {count} matches, below the usual n>=30 rule of thumb for"
              f"the CLT. This is an expected, honest consequence of pooled SRS when one stage is a minority of the population")

# Saving
sample.to_csv("sample_worldcup2026_fouls.csv", index=False)
print(f"\n Saved {len(sample)} sampled rows")