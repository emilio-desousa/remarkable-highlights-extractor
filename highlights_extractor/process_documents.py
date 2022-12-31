import io
from pathlib import Path

import fitz
from PIL import Image

from highlights_extractor.models import DocumentContent, DocumentMetadata
from highlights_extractor.repository.file_reader import FileReader, RawHighlightFile


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


def get_page_number(document_content: DocumentContent, page: RawHighlightFile) -> int:
    page_remarkable_index = document_content.remarkable_page_ids.index(page.page_id)
    page_number = document_content.page_numbers[page_remarkable_index]
    return page_number
