import os
import typing

import requests
from dotenv import load_dotenv

from api.general_api import GitAPI
from models.repository import Model, Contributor


class GitVerseAPI(GitAPI):
    load_dotenv()

    def get_repositories(self, query_for_project) -> typing.List[Model]:
        try:
            repositories = requests.get(
                url=self.search_url(),
                params={
                    "page": 1,
                    "limit": GitAPI.get_number_of_repos(),
                    "q": query_for_project,
                })
            models = []
            for repo in repositories.json()["data"][
                        :min(GitAPI.get_number_of_repos(), len(repositories.json()["data"]))]:
                readme, first_time_seen = self.find_or_insert_readme(
                    self.url_owner_repo_name(repo["owner"]["username"], repo["name"]),
                    self.get_readme, [repo["owner"]["username"], repo["name"]],
                )

                models.append(
                    Model(
                        link="https://gitverse.ru/" + repo["full_name"],
                        clone_link=repo["clone_url"],
                        name=repo["name"],
                        readme=readme,
                        first_time_seen=first_time_seen,
                        description=repo["description"],
                        stars=repo["stars_count"],
                        contributors=[],
                        owner=Contributor(
                            username=repo["owner"]["username"],
                        ),
                    )
                )
            return models

        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    @staticmethod
    def url_owner_repo_name(owner: str, repo_name: str, ) -> str:
        return f'https://gitverse.ru/{owner}/{repo_name}'

    @staticmethod
    def search_url() -> str:
        return "https://gitverse.ru/sc/sbt/api/v1/repos/search"

    @staticmethod
    def readme_urls(owner: str, repo_name: str, ) -> typing.List[str]:
        prefix = f"https://gitverse.ru/api/repos/{owner}/{repo_name}/raw/branch/master/"
        return [
            prefix + "README.md",
            prefix + "readme.md",
            prefix + "ReadMe.md",
        ]

    def get_readme(self, owner: str, repo_name: str, ) -> str:
        try:
            for link in self.readme_urls(owner, repo_name):
                readme = requests.get(
                    url=link)

                if readme.status_code == 200:
                    return readme.content.decode()

            print(f"Can not find readme.md for gitverse {owner}/{repo_name}")
            return ""
        except Exception as e:
            print(f"An error occurred during getting readme: {e}")
            return ""
