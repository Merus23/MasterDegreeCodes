
import pandas as pd
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd

data = pd.read_csv('data.txt', sep=',', header=0)

groups = data.groupby('class')['prompts'].apply(list)

f_value, p_value = stats.f_oneway(*groups)
print(f"F-value: {f_value}")
print(f"P-value: {p_value}")

if p_value < 0.05:
    print("Yes! Significant statistic difference between groups.")
else:
    print("No! Significant statistic difference between groups.")

group_means = data.groupby('class')['prompts'].mean()
print("\nGroup average:")
print(group_means)

tukey = pairwise_tukeyhsd(endog=data['prompts'], groups=data['class'], alpha=0.05)
print("\nTukey Results:")
print(tukey)
