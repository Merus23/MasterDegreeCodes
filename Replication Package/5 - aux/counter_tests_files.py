import csv
import requests
import os

def count_test_files_from_file(csv_file_path, github_token):
    """
    Counts the number of test files in each pull request listed in a CSV file.

    Args:
        csv_file_path: The path to the CSV file.
        github_token: A GitHub API token with read access.

    Returns:
        A tuple containing:
            - A string containing the new CSV data with an added 'test_file_count' field.
            - The total number of test files found across all PRs.
    """

    try:
        with open(csv_file_path, 'r') as csvfile:
            reader = csv.reader(csvfile)
            header = next(reader)
            header = header + ['test_file_count']
            new_csv_lines = [header]

            total_test_files = 0

            for row in reader:
                pr_url = row[0]
                owner, repo = pr_url.split('/')[-4:-2]
                pr_number = int(pr_url.split('/')[-1])

                test_file_count = get_test_file_count_from_pr(owner, repo, pr_number, github_token)
                total_test_files += test_file_count
                row.append(test_file_count)
                new_csv_lines.append(row)

        new_csv_string = '\n'.join([','.join(map(str, line)) for line in new_csv_lines])

        # Save the new CSV data to a file
        output_file_path = csv_file_path.replace(".csv", "_with_test_counts.csv") # Create a new file name
        with open(output_file_path, 'w', newline='') as outfile:
            writer = csv.writer(outfile)
            writer.writerows(new_csv_lines)

        return new_csv_string, total_test_files, output_file_path

    except FileNotFoundError:
        return "Error: CSV file not found.", 0, None
    except Exception as e:
        return f"Error: An unexpected error occurred: {e}", 0, None



def get_test_file_count_from_pr(owner, repo, pr_number, github_token):
    """
    Retrieves the list of files modified in a pull request and counts those
    that appear to be test files (based on filename or path including "test").

    Args:
        owner (str): The owner of the repository.
        repo (str): The name of the repository.
        pr_number (int): The pull request number.
        github_token (str): A Github API token.

    Returns:
        int: The number of test files found in the PR.
    """
    test_file_count = 0
    cursor = None
    has_next_page = True

    while has_next_page:
        query = """
        query($owner: String!, $repo: String!, $pr_number: Int!, $cursor: String) {
          repository(owner: $owner, name: $repo) {
            pullRequest(number: $pr_number) {
              files(first: 100, after: $cursor) {
                nodes {
                  path
                }
                pageInfo {
                  hasNextPage
                  endCursor
                }
              }
            }
          }
        }
        """

        variables = {
            "owner": owner,
            "repo": repo,
            "pr_number": pr_number,
            "cursor": cursor
        }

        headers = {"Authorization": f"Bearer {github_token}"}
        url = "https://api.github.com/graphql"
        try:
            response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            data = response.json()

            files = data['data']['repository']['pullRequest']['files']['nodes']
            for file_data in files:
                file_path = file_data['path']
                if "test" in file_path.lower():
                    test_file_count += 1

            page_info = data['data']['repository']['pullRequest']['files']['pageInfo']
            has_next_page = page_info['hasNextPage']
            cursor = page_info['endCursor']

        except requests.exceptions.RequestException as e:
            print(f"Error during API call: {e}")
            return -1  # Indicate an error

    return test_file_count

# Example Usage (replace with your actual CSV file path and token)
csv_file_path = str(input("Please, paste your folder path:"))
github_token = os.getenv("GITHUB_API_KEY")

if github_token == "YOUR_GITHUB_TOKEN":
   print("Please provide the github token to proceed.")
elif csv_file_path == "your_file.csv":
    print("Please provide the CSV file path to proceed.")
else:
    new_csv_string, total_test_files, output_file_path = count_test_files_from_file(csv_file_path, github_token)

    if output_file_path:
        print(f"New CSV data saved to: {output_file_path}")
        print(f"Total test files found: {total_test_files}")
    else:
        print(new_csv_string) #Print error