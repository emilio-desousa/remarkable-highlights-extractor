from dataclasses import dataclass

from highlights_extractor.repository.file_reader import RawFile, RawHighlightFile
from highlights_extractor.utils import (
    extract_document_id_from_path,
    extract_page_id_from_path,
)


@dataclass
class DocumentContent:
    raw_file: RawFile

    def __post_init__(self) -> None:
        self.document_id = extract_document_id_from_path(self.raw_file.file_path)
        self.document_type = self.raw_file.content["fileType"]
        self.remarkable_page_ids = self.raw_file.content.get("pages", [])
        self.page_numbers = self.raw_file.content.get("redirectionPageMap", [])


@dataclass
class DocumentMetadata:
    raw_file: RawFile

    def __post_init__(self) -> None:
        self.document_id = extract_document_id_from_path(self.raw_file.file_path)
        self.document_name = self.raw_file.content["visibleName"]

    def __repr__(self) -> str:
        return self.document_name


@dataclass
class Highlights:
    color: int
    length: int
    rects: list[dict]
    start: int
    text: str


@dataclass
class PageHighlights:
    raw_file: RawHighlightFile
    page_number = None

    def __post_init__(self) -> None:
        self.page_id = extract_page_id_from_path(self.raw_file.file_path)
        self.highlights = [highlight["text"] for highlight in self.raw_file.content]

    def set_page_number(self, page_number: int) -> None:
        self.page_number = page_number

    def __repr__(self) -> str:
        return str(self.highlights)


@dataclass
class DocumentHighlights:
    page_highlights: list[PageHighlights]

    def __repr__(self) -> str:
        return str(self.page_highlights)


@dataclass
class Document:
    document_highlights: DocumentHighlights
    document_metadata: DocumentMetadata

    def __post_init__(self) -> None:
        self.name = self.document_metadata.document_name
