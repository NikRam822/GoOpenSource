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
                link="https://hub.mos.ru" + link['href'],
                clone_link="",
                name="",
                readme="",
                description="",
                stars=0,
                contributors=[],
                owner=Contributor(
                    username=""
                ),
            )
                for link in soup.find_all('a', class_='project')[:GitAPI.get_number_of_repos()]]
            return repo_links
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
