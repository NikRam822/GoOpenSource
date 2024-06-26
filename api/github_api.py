import typing

from github import Github
from dotenv import load_dotenv
import os

from api.general_api import GitAPI
from models.repository import Model, Contributor


class GitHubAPI(GitAPI):
    load_dotenv()

    def __init__(self):
        self.g = Github(os.getenv("GITHUB_ACCESS_TOKEN"))

    def get_repositories(self, query_for_project) -> typing.List[Model]:
        try:
            repositories = self.g.search_repositories(query=query_for_project)
            repo_links = []
            for repo in repositories[:min(GitAPI.get_number_of_repos(), repositories.totalCount)]:
                readme, first_time_seen = self.find_or_insert_readme(
                    self.url_owner_repo_name(repo.owner.login, repo.name),
                    self.get_readme, [repo.owner.login, repo.name, repo.description],
                )

                repo_links.append(
                    Model(
                        link=repo.html_url,
                        clone_link=repo.clone_url,
                        name=repo.name,
                        readme=readme,
                        first_time_seen=first_time_seen,
                        description=repo.description,
                        stars=repo.watchers_count,
                        contributors=[],
                        owner=Contributor(
                            username=repo.owner.login,
                        ),
                    ))

            return repo_links
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    @staticmethod
    def url_owner_repo_name(owner: str, repo_name: str, ) -> str:
        return f'https://github.com/{owner}/{repo_name}'

    def get_readme(self, owner: str, repo_name: str, descr: str ) -> str:
        return descr + "\n" + self.g.get_repo(full_name_or_id=f"{owner}/{repo_name}", lazy=True).get_readme().decoded_content.decode()
