####################
#imports
####################
from utils import reuse_requests
import sys
import csv
from decouple import config
####################
#global_variables
####################
gh_pat = config('github_pat')
headers = {
    'Authorization': f'Token {gh_pat}',
    'Accept': 'application/vnd.github.v3+json'
}
def get_repo_info(owner,repo):
    # Make the API request to get repository information
    url = f'https://api.github.com/repos/{owner}/{repo}'
    response = reuse_requests.get(url, headers=headers)

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        repo_info = response.json()
        
        # Print some relevant information from the response
        print(f"Repository Name: {repo_info['name']}")
        print(f"Description: {repo_info['description']}")
        print(f"Stars: {repo_info['stargazers_count']}")
        print(f"Forks: {repo_info['forks_count']}")
    else:
        print(f"Failed to retrieve repository information. Status code: {response.status_code}")


with open('repositories.csv', 'r') as file:
    csv_reader = csv.DictReader(file)
    for row in csv_reader:
        username = row['username']
        repository = row['repository']
        get_repo_info(username, repository)