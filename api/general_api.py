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
    def readme_files_names(prefix: str) -> typing.List[str]:
        return [
            prefix + "README.md",
            prefix + "readme.md",
            prefix + "ReadMe.md"
        ]

    @abstractmethod
    def __get_readme(self, owner: str, repo_name: str, ) -> str:
