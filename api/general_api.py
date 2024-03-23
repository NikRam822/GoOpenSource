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

