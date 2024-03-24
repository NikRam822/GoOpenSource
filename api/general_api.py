import os.path
import typing
from abc import ABC, abstractmethod

from models.repository import Model


class GitAPI(ABC):
    @abstractmethod
    def get_repositories(self, query_for_project) -> typing.List[Model]:
        pass

    @staticmethod
    def get_number_of_repos() -> int:
        return 3

    @staticmethod
    def find_or_insert_readme(url: str, readme_func, args: typing.List) -> (str, bool):
        file_name = GitAPI.find_file_path(url)
        if file_name != "":
            return file_name, True

        readme = readme_func(*args)
        file_name = GitAPI.save_readme(url, readme)
        return file_name, False

    @staticmethod
    def find_file_path(url: str) -> str:
        url = url.replace("/", "_").replace(":", "_").replace("__", "_")
        file_name = f"./files/{url}/README.md"
        if os.path.exists(file_name):
            return file_name
        return ""

    @staticmethod
    def save_readme(url: str, readme: str) -> str:
        url = url.replace("/", "_").replace(":", "_").replace("__", "_")
        directory = f"./files/{url}"
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(f"{directory}/README.md", "w") as file:
            file.write(readme)
        return f"{directory}/README.md"
