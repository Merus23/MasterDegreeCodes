import pandas as pd
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import statsmodels.api as sm
from statsmodels.formula.api import ols

data = pd.read_csv('data.txt', sep=',', header=0)

groups = data.groupby('class')['prompts'].apply(list)

normality_results = {}
for group_name, group_data in groups.items():
    stat, p_value = stats.shapiro(group_data)
    normality_results[group_name] = p_value
    print(f"Normality test for {group_name}: p-value = {p_value}")
    if p_value < 0.05:
        print(f"NO! The data in group {group_name} does not appear to follow a normal distribution.")
    else:
        print(f"YES! The data in group {group_name} does appear to follow a normal distribution.")