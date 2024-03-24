import typing

import requests
from gitlab import Gitlab
from dotenv import load_dotenv
import os

from api.general_api import GitAPI
from models.repository import Model, Contributor


class GitLabAPI(GitAPI):
    load_dotenv()

    def get_repositories(self, query_for_project) -> typing.List[Model]:
        try:
            gl = Gitlab(os.getenv("GITLAB_API_URL"), private_token=os.getenv("GITLAB_ACCESS_TOKEN"))
            projects = gl.projects.list(search=query_for_project, per_page=GitAPI.get_number_of_repos(), get_all=False)
            repo_links = []
            for project in projects:
                readme, first_time_seen = self.find_or_insert_readme(
                    self.url_owner_repo_name(project.namespace['path'], project.path),
                    self.get_readme, [project.readme_url, project.namespace['path'], project.path],
                )

                repo_links.append(
                    Model(
                        link=project.web_url,
                        clone_link=project.http_url_to_repo,
                        name=project.name,
                        readme=readme,
                        first_time_seen=first_time_seen,
                        description=project.description,
                        stars=project.star_count,
                        contributors=[],
                        owner=Contributor(
                            username=project.namespace['name']
                        ),
                    ))

            return repo_links
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    @staticmethod
    def url_owner_repo_name(owner: str, repo_name: str, ) -> str:
        return f'https://gitlab.com/{owner}/{repo_name}'

    @staticmethod
    def get_readme(readme_link: str, owner: str, repo_name: str, ) -> str:
        if readme_link is None:
            return ""
        readme_name = readme_link.split("/")[-2:]
        link = f'https://gitlab.com/{owner}/{repo_name}/-/raw/{"/".join(readme_name)}'

        try:
            response = requests.get(link)
            return response.content.decode()
        except Exception as e:
            print(f"An error occurred during getting gitlab readme: {e}")
            return ""
