import typing

from dotenv import load_dotenv
from api.general_api import GitAPI
from bs4 import BeautifulSoup
import requests

from models.repository import Model, Contributor


class MosHub(GitAPI):
    load_dotenv()

    def get_repositories(self, query_for_project) -> typing.List[Model]:
        try:
            url = "https://hub.mos.ru/explore/projects" + "?name=" + query_for_project + "&sort=latest_activity_desc"
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            repo_links = [Model(
                link="https://hub.mos.ru" + link.find_all('div', class_='project-cell gl-w-11')[0].find_all('a')[0][
                    'href'],
                clone_link="",
                name=link.find_all('div', class_='project-cell gl-w-11')[0].find_all('a')[0]['href'].split("/")[2],
                readme=self.get_readme(
                    link.find_all('div', class_='project-cell gl-w-11')[0].find_all('a')[0]['href'].split("/")[1],
                    link.find_all('div', class_='project-cell gl-w-11')[0].find_all('a')[0]['href'].split("/")[2]),
                description="",
                stars=int(
                    link.find_all('div', class_='controls gl-display-flex gl-align-items-center')[1].find_all('a')[
                        0].text.replace("\n", "")),
                contributors=[],
                owner=Contributor(
                    username=link.find_all('div', class_='project-cell gl-w-11')[0].find_all('a')[0]['href'].split("/")[
                        1]
                ),
            )
                for link in soup.find_all('li', class_='project-row')[:GitAPI.get_number_of_repos()]]
            return repo_links
        except Exception as e:
            print(f"An error occurred: {e}")
            return []

    def readme_urls(self, owner: str, repo_name: str, ) -> typing.List[str]:
        prefix = f"https://hub.mos.ru/{owner}/{repo_name}/-/raw/"
        return [
            prefix + "main/README.md",
            prefix + "main/readme.md",
            prefix + "main/ReadMe.md",
            prefix + "master/README.md",
            prefix + "master/readme.md",
            prefix + "master/ReadMe.md",
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
