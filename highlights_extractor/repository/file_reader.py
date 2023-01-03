# %%
import glob
import json
from abc import ABCMeta, abstractmethod
from dataclasses import dataclass
from pathlib import Path
from typing import Generator, Optional, Tuple

from highlights_extractor.constants import DATA_FOLDER
from highlights_extractor.utils import (
    extract_document_id_from_path,
    extract_page_id_from_path,
)


@dataclass
class RawFile:
    file_path: Path
    content: dict

    def __post_init__(self) -> None:
        self.document_id = extract_document_id_from_path(self.file_path)


@dataclass
class RawHighlightFile:
    file_path: Path
    content: list[dict]

    def __post_init__(self) -> None:
        self.page_id = extract_page_id_from_path(self.file_path)
        self.document_id = extract_document_id_from_path(self.file_path)


class FileReader(metaclass=ABCMeta):
    @abstractmethod
    def read_all_metadata_files(self, fields_to_keep: list[str]) -> list[RawFile]:
        pass

    @abstractmethod
    def read_document_highlights(self, document_id: str) -> list[RawHighlightFile]:
        pass

    @abstractmethod
    def read_all_content_files(self, fields_to_keep: list[str]) -> list[RawFile]:
        pass

    @abstractmethod
    def read_document_content(
        self, document_id: str, fields_to_keep: Optional[list[str]] = None
    ) -> RawFile:
        pass


class LocalFileReader(FileReader):
    def __init__(self, data_folder: Path = DATA_FOLDER) -> None:
        self.data_folder = data_folder

    def read_all_metadata_files(self, fields_to_keep: list[str]) -> list[RawFile]:
        return self._create_raw_file("*.metadata", fields_to_keep)

    def read_all_content_files(self, fields_to_keep: list[str]) -> list[RawFile]:
        return self._create_raw_file("*.content", fields_to_keep)

    def _create_raw_file(self, glob_expression: str, fields_to_keep: list[str]) -> list[RawFile]:
        all_content_files = [
            RawFile(
                file_path=Path(file_path),
                content={key: file_data[key] for key in fields_to_keep},
            )
            for file_data, file_path in self.read_files_from_glob_expression(glob_expression)
        ]
        return all_content_files

    def read_document_content(
        self, document_id: str, fields_to_keep: Optional[list[str]] = None
    ) -> RawFile:
        file_path = DATA_FOLDER / f"{document_id}.content"
        file_data = self.read_json(file_path)
        if fields_to_keep:
            file_content = {key: file_data[key] for key in fields_to_keep}
        else:
            file_content = file_data
        return RawFile(file_path=file_path, content=file_content)

    def read_document_highlights(self, document_id: str) -> list[RawHighlightFile]:
        files = []
        file_path = ""
        for file_data, file_path in self.read_files_from_glob_expression(
            str(DATA_FOLDER / f"{document_id}.highlights/*.json")
        ):
            data = recursive_function_to_get_all_dicts(file_data["highlights"])
            files.append(RawHighlightFile(file_path=Path(file_path), content=data))

        return files

    def read_files_from_glob_expression(
        self, glob_expression: str
    ) -> Generator[Tuple[dict, str], None, None]:
        files_path = glob.glob(str(self.data_folder / glob_expression))
        for file_path in files_path:
            file_data = self.read_json(Path(file_path))
            yield (file_data, file_path)

    def read_json(self, path: Path) -> dict:
        with open(str(path), "rb") as json_file:
            return json.load(json_file)


def recursive_function_to_get_all_dicts(highlights: list) -> list:
    list_of_dict = []
    for dict_or_list in highlights:
        if isinstance(dict_or_list, dict):
            list_of_dict.append(dict_or_list)
        else:
            list_of_dict = list_of_dict + recursive_function_to_get_all_dicts(dict_or_list)

    return list_of_dict
