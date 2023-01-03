from dataclasses import dataclass
from typing import Iterator, Optional

from PIL import Image

from highlights_extractor.repository.file_reader import RawFile, RawHighlightFile
from highlights_extractor.utils import extract_document_id_from_path


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
    page_number: int
    chapter: str = ""
    image: Optional[Image.Image] = None

    def __post_init__(self) -> None:
        self.page_id = self.raw_file.page_id
        self.document_id = self.raw_file.document_id
        self.highlights = [highlight["text"] for highlight in self.raw_file.content]

    def __repr__(self) -> str:
        return str(self.highlights)


@dataclass
class ChapterHighlights:
    chapter: str
    page_highlights: list[PageHighlights]

    def __repr__(self) -> str:
        return str(self.page_highlights)

    def __iter__(self) -> Iterator[PageHighlights]:
        return iter(self.page_highlights)


@dataclass
class DocumentHighlights:
    chapters_highlights: list[ChapterHighlights]
    document_id: str

    def __repr__(self) -> str:
        return str(self.chapters_highlights)

    def __iter__(self) -> Iterator[ChapterHighlights]:
        return iter(self.chapters_highlights)


@dataclass
class DocumentMetadata:
    raw_file: RawFile

    def __post_init__(self) -> None:
        self.document_id = self.raw_file.document_id
        self.document_name = self.raw_file.content["visibleName"]

    def __repr__(self) -> str:
        return self.document_name


@dataclass
class Document:
    document_highlights: DocumentHighlights
    document_metadata: DocumentMetadata

    def __post_init__(
        self,
    ) -> None:
        self.name = self.document_metadata.document_name
        self.highlights = self.document_highlights.chapters_highlights

    def __iter__(self) -> Iterator[ChapterHighlights]:
        return iter(self.highlights)


@dataclass
class DocumentContent:
    raw_file: RawFile

    def __post_init__(self) -> None:
        self.document_id = extract_document_id_from_path(self.raw_file.file_path)
        self.remarkable_page_ids = self.raw_file.content.get("pages", [])
        self.page_numbers = self.raw_file.content.get("redirectionPageMap", [])
        self.file_type = self.raw_file.content.get("FileType", "")
