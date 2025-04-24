import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('data.txt', sep=',')

palette = sns.color_palette("Set2")

plt.figure(figsize=(14, 8))
sns.boxplot(x='class', y='prompts', data=data, palette=palette)
plt.title('Distribution of Prompts per Category', fontsize=16)
plt.xlabel('Category', fontsize=14)
plt.ylabel('Number of Prompts', fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.yticks(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)

plt.gca().yaxis.grid(True, linestyle='--', which='both', color='gray', alpha=0.7)

plt.tight_layout()
plt.show()
