from github import Github
import os
github_token = os.environ.get("GITHUB_TOKEN")  # Get from environment variable

if not github_token:
  print("Error: GITHUB_TOKEN environment variable not set.")
  exit(1)

def create_github_repo(repo_name, description, is_private, github_token):

    try:
        g = Github(github_token)
        user = g.get_user()
        repo = user.create_repo(repo_name, description=description, private=is_private)
        print(f"Repository '{repo_name}' created successfully: {repo.html_url}")
        return repo, None

    except Exception as e:
        error_message = f"An error occurred: {e}"
        print(error_message)
        return None, error_message


if __name__ == "__main__":
    repo_name = input("Enter the repository name: ")
    description = input("Enter the repository description: ")
    is_private_input = input("Make the repository private? (yes/no): ").lower()
    is_private = is_private_input == "yes"
    repo, error = create_github_repo(repo_name, description, is_private, github_token)

    if error:
      print(f"Failed to create repository: {error}")
    else:
      # Optionally, you can perform additional actions with the created repo object.
      # For example, add a README, collaborators, etc.
      pass