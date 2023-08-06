from typing import List

from sikriml.services.models.abstracts.convertible_interface import (
    IConvertible,
)


class FileHelper:
    @staticmethod
    def read(path: str, model: IConvertible) -> List[IConvertible]:
        with open(path, "r", encoding="utf-8") as f:
            raw_data = f.read().split("\n")
            return model.from_dict(raw_data)

    @staticmethod
    def write(path: str, data_list: List[IConvertible]) -> None:
        with open(path, "w", encoding="utf-8") as f:
            for data in data_list:
                f.write(data.to_json())
