import os

import requests
from dotenv import load_dotenv

from api.general_api import GitAPI


class GitFlameAPI(GitAPI):
    load_dotenv()

    def get_repositories(self, query_for_project):
        try:
            repositories = requests.get(
                url=self.search_url(),
                params={
                    "page": 1,
                    "limit": GitAPI.get_number_of_repos(),
                    "q": query_for_project,
                    "is_private": False,
                })
            repo_links = [repo["html_url"] for repo in repositories.json()["repositories"][:GitAPI.get_number_of_repos()]]
            return repo_links
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    @staticmethod
    def search_url() -> str:
        return os.getenv("GITFLAME_API_URL") + "/search"
