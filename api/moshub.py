from dotenv import load_dotenv
from api.general_api import GitAPI
from bs4 import BeautifulSoup
import requests


class MosHub(GitAPI):
    load_dotenv()

    def get_repositories(self, query_for_project):
        try:
            url = "https://hub.mos.ru/explore/projects"+"?name=" + query_for_project+"&sort=latest_activity_desc"
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')

            repo_links = [link['href'] for link in soup.select('#content-body div[5] ul li div[1] a')]

            return repo_links
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
