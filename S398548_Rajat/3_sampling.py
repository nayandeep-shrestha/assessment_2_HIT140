import pandas as pd
from pathlib import Path

script_dir=Path(__file__).resolve().parent
random_seed=42
sample_size=80

#Loadingg the wrangled data
wrangled=pd.read_csv(script_dir/'wrangled_worldcup2026_passing.csv')
population=wrangled[['match_id','team','opponent','stage','Result_category','Passing_Accuracy']]

N=len(population)
n_winner=(population["Result_category"]=='Winner').sum()
n_loser=(population['Result_category']=='Loser').sum()
print(f"Full population: N={N} team-amtch rows"
      f'9{n_winner} Winner, {n_loser} Loser')

#-------------Random sample of 80 rows, mixed together (not split evenly between Winner and Loser first)
sample=population.sample(n=sample_size, random_state=random_seed, replace=False)

print(f'\nDrew a pooled SRS of n={sample_size} from n={N}, no stratification by Result_category')

#-----------Report the resulting catgeory composition
print("\nResulting Result_category composition of the sample:")
print(sample["Result_category"].value_counts())

print('\nSample vs population means(Passing_accuracy), for a quick check:')
for category in ['Winner',"Loser"]:
    pop_mean=population[population["Result_category"]==category]["Passing_Accuracy"].mean()
    samp_subset=sample[sample['Result_category']==category]['Passing_Accuracy']
    print(f'{category}:population mean= {pop_mean:.2f}%,'
          f'sample n= {len(samp_subset)}, sample mean={samp_subset.mean():.2f}%')

#------------Here if the either subgroup end up too thin for later steps it is flagged
counts=sample['Result_category'].value_counts()
for category, count in counts.items():
    if count < 30:
        print(f'\n Note: the {category} subgroup in this sample has only {count} rows, below '
              f'the usual n>=30 rule of thumb for the CLT. This is an expected, honest '
              f'consequence of pooled SRS rather than a stratified draw.')
        
#----------SAVING-----------#
out_path=script_dir/'sample_worldcup2026_passing.csv'
sample.to_csv(out_path, index=False)
print(f'\n Saved {len(sample)} sampled rows to {out_path.name}')