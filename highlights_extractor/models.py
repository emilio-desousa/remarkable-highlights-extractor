from dataclasses import dataclass

from highlights_extractor.file_reader import RawFile
from highlights_extractor.utils import extract_document_id_from_path


@dataclass
class DocumentContent:
    raw_file: RawFile

    def __post_init__(self) -> None:
        self.document_id = extract_document_id_from_path(self.raw_file.file_path)
        self.document_type = self.raw_file.content["fileType"]


@dataclass
class DocumentMetadata:
    raw_file: RawFile

    def __post_init__(self) -> None:
        self.document_id = extract_document_id_from_path(self.raw_file.file_path)
        self.document_name = self.raw_file.content["visibleName"]
