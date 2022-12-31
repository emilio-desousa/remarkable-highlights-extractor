import io
from copy import copy
from pathlib import Path

import fitz
from PIL import Image

from highlights_extractor.models import (
    DocumentContent,
    DocumentHighlights,
    DocumentMetadata,
    PageHighlights,
)
from highlights_extractor.repository.file_reader import FileReader


class PDFReader:
    def __init__(self, document_path: Path) -> None:
        self.document_path = document_path
        self.reader = None

    def get_fitz_reader(self) -> fitz.Document:
        self.reader = self.reader or fitz.Document(self.document_path)
        return self.reader

    def get_page_image(self, page_number: int) -> Image.Image:
        reader = self.get_fitz_reader()
        pdf_page = reader.load_page(page_number)
        mat = fitz.Matrix(2, 2)
        pix = pdf_page.get_pixmap(matrix=mat)
        image = Image.open(io.BytesIO(pix.pil_tobytes(format="jpeg")))
        return image


def get_all_file_names(file_reader: FileReader) -> list[DocumentMetadata]:
    metadata_files = file_reader.read_all_metadata_files(["visibleName"])
    documents_metadata = [
        DocumentMetadata(metadata_file) for metadata_file in metadata_files
    ]
    return documents_metadata


def get_document_id_from_metadata_documents(
    documents_metadata: list[DocumentMetadata], index: int = 6
) -> DocumentMetadata:
    return documents_metadata[index]


def get_highlights(file_reader: FileReader, document_id: str) -> DocumentHighlights:
    highlights_files = file_reader.read_document_highlights(document_id)
    all_highlights = []
    for highlight_file in highlights_files:
        page_highlights = PageHighlights(highlight_file)
        all_highlights.append(page_highlights)
    doc_highlights = DocumentHighlights(all_highlights, document_id=document_id)
    return doc_highlights


def enrich_highlights_pages(
    document_content: DocumentContent,
    document_highlights: DocumentHighlights,
    pdf_reader: PDFReader | None,
) -> DocumentHighlights:
    current_document_highlights = copy(document_highlights)
    for page_highlights in current_document_highlights.page_highlights:
        page_number = get_page_number(document_content, page_highlights)
        page_highlights.set_page_number(page_number)
        if pdf_reader:
            page_image = pdf_reader.get_page_image(page_number)
            page_highlights.set_page_image(page_image)

    return current_document_highlights


def get_page_number(document_content: DocumentContent, page: PageHighlights) -> int:
    page_remarkable_index = document_content.remarkable_page_ids.index(page.page_id)
    page_number = document_content.page_numbers[page_remarkable_index]
    return page_number
