from abc import ABC
from abc import abstractmethod

class ResponseBuilderInterface(ABC):

    @abstractmethod
    def _get_data_from_code(self, status):
        raise NotImplemented

    @abstractmethod
    def response(self) -> dict:
        raise NotImplemented


