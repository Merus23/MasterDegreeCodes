import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

data = pd.read_csv('unique_repos.txt', sep=',')

palette = sns.color_palette("Set2")

fig, axes = plt.subplots(1, 3, figsize=(18, 6))

sns.boxplot(ax=axes[0], y='stars', data=data, color=palette[0], width=0.3)
axes[0].set_xlabel('Stars')
axes[0].set_ylabel('')

sns.boxplot(ax=axes[1], y='collaborators', data=data, color=palette[1], width=0.3)
axes[1].set_xlabel('Collaborators')
axes[1].set_ylabel('')

sns.countplot(ax=axes[2], y='language', data=data, order=data['language'].value_counts().index, palette=palette)
axes[2].set_xlabel('Programming Language')
axes[2].set_ylabel('')

plt.tight_layout()
plt.show()
