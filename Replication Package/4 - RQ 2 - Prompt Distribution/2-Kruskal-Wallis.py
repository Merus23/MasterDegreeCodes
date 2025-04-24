import pandas as pd
from scipy.stats import kruskal

data = pd.read_csv('data.txt', sep=',', header=0)

data = data.rename(columns={'class': 'class_col'})

groups = data.groupby('class_col')['prompts'].apply(list)

stat, p_value = kruskal(*groups)
print(f"Kruskal-Wallis H-statistic: {stat}")
print(f"P-value: {p_value}")

if p_value < 0.05:
    print("YES! There is significant statistic difference between the medians of the groups")
else:
    print("NO! There is not significant statistic difference between the medians of the groups")
