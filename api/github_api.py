import typing

from github import Github
from dotenv import load_dotenv
import os

from api.general_api import GitAPI
from models.repository import Model, Contributor


class GitHubAPI(GitAPI):
    load_dotenv()

    def get_repositories(self, query_for_project) -> typing.List[Model]:
        try:
            g = Github(os.getenv("GITHUB_ACCESS_TOKEN"))
            repositories = g.search_repositories(query=query_for_project)
            repo_links = [
                Model(
                    link=repo.html_url,
                    clone_link="",
                    name="",
                    readme="",
                    description="",
                    stars=0,
                    contributors=[],
                    owner=Contributor(
                        username=""
                    ),
                ) for repo in repositories[:GitAPI.get_number_of_repos()]]
            return repo_links
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
