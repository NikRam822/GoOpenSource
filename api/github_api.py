from github import Github
from dotenv import load_dotenv
import os

from api.general_api import GitAPI


class GitHubAPI(GitAPI):

    load_dotenv()

    def get_repositories(self, query_for_project):
        g = Github(os.getenv("GITHUB_ACCESS_TOKEN"))
        repositories = g.search_repositories(query=query_for_project)
        repo_links = [repo.html_url for repo in repositories[:5]]
        return repo_links
