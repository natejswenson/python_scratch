"""GitHub API integration for repository information retrieval."""
import csv
from typing import Dict, Optional
from decouple import config
from utils import reuse_requests

def get_repo_info(owner: str, repo: str, headers: Dict[str, str]) -> Optional[Dict]:
    """
    Retrieve repository information from GitHub API.

    Args:
        owner: Repository owner username
        repo: Repository name
        headers: HTTP headers including authorization

    Returns:
        Dict containing repository information, or None if request fails
    """
    url = f'https://api.github.com/repos/{owner}/{repo}'

    try:
        response = reuse_requests.get(url, headers=headers)

        if response.status_code == 200:
            repo_info = response.json()

            # Print some relevant information from the response
            print(f"Repository Name: {repo_info['name']}")
            print(f"Description: {repo_info['description']}")
            print(f"Stars: {repo_info['stargazers_count']}")
            print(f"Forks: {repo_info['forks_count']}")

            return repo_info
        else:
            print(f"Failed to retrieve repository information. Status code: {response.status_code}")
            return None
    except Exception as e:
        print(f"Error retrieving repository information: {e}")
        return None

def main():
    """Main function to process repositories from CSV file."""
    # Load GitHub PAT from environment
    gh_pat = config('github_pat')
    headers = {
        'Authorization': f'Token {gh_pat}',
        'Accept': 'application/vnd.github.v3+json'
    }

    try:
        with open('repositories.csv', 'r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                username = row['username']
                repository = row['repository']
                get_repo_info(username, repository, headers)
    except FileNotFoundError:
        print("Error: repositories.csv file not found")
    except KeyError as e:
        print(f"Error: Missing required column in CSV: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()