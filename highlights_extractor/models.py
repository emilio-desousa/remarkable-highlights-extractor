from dataclasses import dataclass
from typing import Optional

from PIL import Image

from highlights_extractor.repository.file_reader import RawFile, RawHighlightFile
from highlights_extractor.utils import extract_document_id_from_path


@dataclass
class DocumentContent:
    raw_file: RawFile

    def __post_init__(self) -> None:
        self.document_id = extract_document_id_from_path(self.raw_file.file_path)
        self.remarkable_page_ids = self.raw_file.content.get("pages", [])
        self.page_numbers = self.raw_file.content.get("redirectionPageMap", [])
        self.file_type = self.raw_file.content.get("FileType", "")


@dataclass
class DocumentMetadata:
    raw_file: RawFile

    def __post_init__(self) -> None:
        self.document_id = self.raw_file.document_id
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
    page_number: int
    image: Optional[Image.Image] = None
    chapter: Optional[str] = None

    def __post_init__(self) -> None:
        self.page_id = self.raw_file.page_id
        self.document_id = self.raw_file.document_id
        self.highlights = [highlight["text"] for highlight in self.raw_file.content]

    def __repr__(self) -> str:
        return str(self.highlights)


def sort_page_highlights(
    page_highlights: list[PageHighlights],
) -> list[PageHighlights]:
    return sorted(page_highlights, key=lambda x: x.page_number)


@dataclass
class DocumentHighlights:
    page_highlights: list[PageHighlights]
    document_id: str

    def __post_init__(self) -> None:
        self.page_highlights_sorted = sort_page_highlights(self.page_highlights)
        del self.page_highlights

    def __repr__(self) -> str:
        return str(self.page_highlights)


@dataclass
class Document:
    document_highlights: DocumentHighlights
    document_metadata: DocumentMetadata

    def __post_init__(
        self,
    ) -> None:
        self.name = self.document_metadata.document_name
        self.highlights = self.document_highlights.page_highlights_sorted
