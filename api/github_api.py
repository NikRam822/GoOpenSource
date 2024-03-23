from github import Github
from dotenv import load_dotenv
import os

from api.general_api import GitAPI


class GitHubAPI(GitAPI):

    load_dotenv()

    def get_repositories(self, query_for_project):
        try:
            g = Github(os.getenv("GITHUB_ACCESS_TOKEN"))
            repositories = g.search_repositories(query=query_for_project)
            repo_links = [repo.html_url for repo in repositories[:GitAPI.get_number_of_repos()]]
            return repo_links
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

