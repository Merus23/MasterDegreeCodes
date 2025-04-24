import pandas as pd

def extract_repo_url(pr_url):
    return '/'.join(pr_url.split('/')[:5])

file_path = 'data.txt'  
df = pd.read_csv(file_path)

df['Repo URL'] = df['PR URL'].apply(extract_repo_url)

unique_pr_count = df['PR URL'].nunique()
print(f"Number of distinct pull requests: {unique_pr_count}")

unique_repos = df[['Repo URL', 'stars', 'collaborators', 'language']].drop_duplicates()

output_file_path = 'unique_repos.txt'
unique_repos.to_csv(output_file_path, index=False, sep=',')

print(f"Unique repositories saved to {output_file_path}")