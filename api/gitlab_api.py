from gitlab import Gitlab
from dotenv import load_dotenv
import os

from api.general_api import GitAPI


class GitLabAPI(GitAPI):
    load_dotenv()

    def get_repositories(self, query_for_project):
        try:
            gl = Gitlab(os.getenv("GITLAB_API_URL"), private_token=os.getenv("GITLAB_ACCESS_TOKEN"))
            projects = gl.projects.list(search=query_for_project, per_page=GitAPI.get_number_of_repos())
            repo_links = [project.web_url for project in projects]
            return repo_links
        except Exception as e:
            print(f"An error occurred: {e}")
            return []
