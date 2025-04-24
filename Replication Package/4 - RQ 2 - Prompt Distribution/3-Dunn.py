import pandas as pd
import scikit_posthocs as sp

data = pd.read_csv('data.txt', sep=',', header=0)

dunn = sp.posthoc_dunn(data, val_col='prompts', group_col='class', p_adjust='bonferroni')

print("\nDunn Test Results:")
print(dunn)
