from abc import ABC, abstractmethod


class GitAPI(ABC):
    @abstractmethod
    def get_repositories(self, query_for_project):
        pass

    @staticmethod
    def get_number_of_repos():
        return 10
