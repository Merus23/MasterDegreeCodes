import csv
import os
import requests
import re

import csv
import os
import requests
import re

def download_test_files_from_csv(csv_file_path, output_directory):
    """
    Downloads test files from pull requests listed in a CSV file and organizes them into folders.

    Args:
        csv_file_path (str): The path to the CSV file.
        output_directory (str): The directory where the downloaded files will be organized.
    """

    # Create the output directory if it doesn't exist.
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    with open(csv_file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            pr_url = row['PR URL']
            pr_title = row['PR Title']  # Or any other unique identifier from the CSV
            test_file_count = int(row['test_file_count']) # Number of test files

            # Sanitize the PR title to create a valid directory name.
            pr_directory_name = re.sub(r'[^\w\s-]', '', pr_title).strip()  # Remove non-alphanumeric characters
            pr_directory_name = pr_directory_name.replace(' ', '_')  # Replace spaces with underscores
            pr_directory_name = f"{pr_directory_name[:50]}" # Limit the length of the directory name
            pr_directory_path = os.path.join(output_directory, pr_directory_name)

            # Create the PR-specific directory.
            if not os.path.exists(pr_directory_path):
                os.makedirs(pr_directory_path)

            print(f"Processing PR: {pr_title} ({pr_url})")

            # Extract owner, repo, and pull number from the PR URL
            match = re.match(r"https://github.com/(?P<owner>[^/]+)/(?P<repo>[^/]+)/pull/(?P<pull_number>\d+)", pr_url)
            if match:
                owner = match.group("owner")
                repo = match.group("repo")
                pull_number = match.group("pull_number")

                # Construct the GitHub API URL to get the files changed in the PR.
                api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pull_number}/files"

                try:
                    # Fetch the list of files changed in the PR.
                    print(f"  API URL: {api_url}")  # Debugging: Print the API URL
                    response = requests.get(api_url)
                    print(f"  Response Status Code: {response.status_code}")  # Debugging: Print status code
                    response.raise_for_status()  # Raise an exception for bad status codes.
                    files = response.json()
                    print(f"  Response Content: {response.json()}") #Debugging print content

                    # Download test files.
                    downloaded_count = 0
                    for file_data in files:
                        filename = file_data['filename']
                        raw_url = file_data['raw_url']

                        print(f"  Filename: {filename}")  # Debugging: Print filename

                        # Heuristic to identify test files (you might need to adjust this).
                        if 'test' in filename.lower() or 'tests' in filename.lower():
                            try:
                                # Download the file.
                                file_response = requests.get(raw_url)
                                file_response.raise_for_status()
                                file_content = file_response.content

                                # Save the file to the PR directory.
                                filepath = os.path.join(pr_directory_path, os.path.basename(filename))
                                with open(filepath, 'wb') as f:
                                    f.write(file_content)

                                print(f"  Downloaded: {filename}")
                                downloaded_count += 1
                            except requests.exceptions.RequestException as e:
                                print(f"  Error downloading {filename}: {e}")
                                print(f"  File Response Status Code: {file_response.status_code if 'file_response' in locals() else 'N/A'}")
                                print(f"  File Response Content: {file_response.content if 'file_response' in locals() else 'N/A'}")

                    # Optional: Verify the number of downloaded files
                    if test_file_count > 0 and downloaded_count < test_file_count:
                        print(f"  Warning: Expected {test_file_count} test files but only downloaded {downloaded_count}")

                except requests.exceptions.RequestException as e:
                    print(f"  Error fetching file list for {pr_url}: {e}")
                except Exception as e:
                    print(f"  An unexpected error occurred: {e}")
            else:
                print(f"  Could not parse PR URL: {pr_url}")

csv_file = str(input('Informe o caminho do csv: '))
save_name = csv_file.split('/')[-1]
output_path = '/home/mateus/Documents/University/Master Degree/2º Período/Estudos dirigidos/DB/'
output_dir = f'{output_path+save_name}'

download_test_files_from_csv(csv_file, output_dir)