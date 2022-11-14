#%%
import glob
import json
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Generator, Tuple

from remarks_extractor.config.constants import DATA_FOLDER


@dataclass
class RawFile:

    file_path: Path
    content: dict


class FileReader(metaclass=ABCMeta):
    @abstractmethod
    def read_all_content_files(self, fields_to_keep: list[str]) -> list[RawFile]:
        pass

    @abstractmethod
    def read_all_metadata_files(self, fields_to_keep: list[str]) -> list[RawFile]:
        pass

    # @abstractmethod
    # def read_highlights(self) -> dict:
    #     pass

    # @abstractmethod
    # def read_metadata(self) -> dict:
    #     pass

    # @abstractmethod
    # def read_pdf(self) -> dict:
    #     pass


class LocalFileReader(FileReader):
    def __init__(self, data_folder: Path = DATA_FOLDER) -> None:
        self.data_folder = data_folder

    def read_all_content_files(self, fields_to_keep: list[str]) -> list[RawFile]:
        all_content_files = []
        for file_data, file_path in self.read_files_from_glob_expression("*.content"):
            all_content_files.append(
                RawFile(
                    file_path=Path(file_path),
                    content={key: file_data[key] for key in fields_to_keep},
                )
            )
        return all_content_files

    def read_all_metadata_files(self, fields_to_keep: list[str]) -> list[RawFile]:

        all_content_files = []
        for file_data, file_path in self.read_files_from_glob_expression("*.metadata"):
            all_content_files.append(
                RawFile(
                    file_path=Path(file_path),
                    content={key: file_data[key] for key in fields_to_keep},
                )
            )
        return all_content_files

    def read_files_from_glob_expression(
        self, glob_expression: str
    ) -> Generator[Tuple[dict, str], None, None]:
        files_path = glob.glob(str(self.data_folder / glob_expression))
        for file_path in files_path:
            file_data = self.read_json(file_path)
            yield (file_data, file_path)

    def read_json(self, path: str) -> dict:
        with open(path, "rb") as json_file:
            return json.load(json_file)


# %%
