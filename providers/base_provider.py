from abc import ABC, abstractmethod


class BaseProvider(ABC):

    @abstractmethod
    def search(self, query: str, limit: int):
        pass