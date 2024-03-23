import os
import typing

import requests
from dotenv import load_dotenv

from api.general_api import GitAPI
from models.repository import Model, Contributor


class GitFlameAPI(GitAPI):
    load_dotenv()

    def get_repositories(self, query_for_project) -> typing.List[Model]:
        try:
            repositories = requests.get(
                url=self.search_url(),
                params={
                    "page": 1,
                    "limit": GitAPI.get_number_of_repos(),
                    "q": query_for_project,
                    "is_private": False,
                })
            models = [
                Model(
                    link=repo["html_url"],
                    clone_link=repo["clone_url"],
                    name=repo["name"],
                    readme=self.__get_readme(repo["owner"]["username"], repo["name"]),
                    description=repo["description"],
                    stars=repo["stars_count"],
                    contributors=[],
                    owner=Contributor(
                        username=repo["owner"]["username"],
                    ),
                )
                for repo in
                repositories.json()["repositories"][:GitAPI.get_number_of_repos()]]
            return models

        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    @staticmethod
    def search_url() -> str:
        return os.getenv("GITFLAME_API_URL") + "/search"

    @staticmethod
    def readme_urls(owner: str, repo_name: str, ) -> typing.List[str]:
        prefix = os.getenv("GITFLAME_API_URL") + f"/repos/{owner}/{repo_name}/raw//"
        return [
            prefix + "readme.md",
            prefix + "README.md",
            prefix + "ReadMe.md",
        ]

    def __get_readme(self, owner: str, repo_name: str, ) -> str:
        try:
            for link in self.readme_urls(owner, repo_name):
                readme = requests.get(
                    url=link)

                if readme.status_code == 200:
                    return readme.content.decode()

            print(f"Can not find readme.md for gitflame {owner}/{repo_name}")
            return ""
        except Exception as e:
            print(f"An error occurred during getting readme: {e}")
            return ""
