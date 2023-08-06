from abc import ABC, abstractmethod
from typing import List


class IConvertible(ABC):
    @staticmethod
    @abstractmethod
    def from_dict(fields: List[str]):
        pass

    @abstractmethod
    def to_json(self) -> str:
        pass
