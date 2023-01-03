import io
import re
import string
from dataclasses import dataclass
from pathlib import Path
from typing import List

import fitz
import pandas as pd
from PIL import Image

from highlights_extractor.config.exceptions import DocumentNotProcessableError
from highlights_extractor.models import DocumentContent, DocumentMetadata
from highlights_extractor.repository.file_reader import FileReader, RawHighlightFile


@dataclass
class TableOfContentItem:
    level: int
    title: str
    page: int


class PDFReader:
    def __init__(self, document_path: Path, document_name: str) -> None:
        self.reader = self._get_fitz_reader(document_path)
        self.document_name = document_name

    def _get_raw_table_of_contents(self) -> List[TableOfContentItem]:
        if table_of_content := self.reader.get_toc():  # type: ignore
            return [TableOfContentItem(*item) for item in table_of_content]

        raise DocumentNotProcessableError(
            f"Document: {self.document_name} does not have a table of contents"
            "or it cannot be found."
        )

    @staticmethod
    def _get_table_of_contents_df(
        raw_table_of_content: List[TableOfContentItem],
    ) -> pd.DataFrame:
        table_of_contents = pd.DataFrame(
            raw_table_of_content, columns=["level", "title", "page"]
        )
        table_of_contents["title"] = table_of_contents["title"].apply(
            extract_table_content_item_text
        )
        return table_of_contents

    def get_chapter_title(self, page_number: int) -> str:
        table_of_content_items = self._get_raw_table_of_contents()
        table_of_contents = self._get_table_of_contents_df(table_of_content_items)

        table_of_contents = table_of_contents.assign(
            difference_between_page_and_chapters=lambda df: df["page"] - page_number
        )
        only_chapters_with_page_number_less_than_current_page_df = table_of_contents[
            table_of_contents["difference_between_page_and_chapters"] <= 0
        ]

        if only_chapters_with_page_number_less_than_current_page_df.empty:
            raise DocumentNotProcessableError(
                "Could not find chapter title "
                f"for page: {page_number} in {self.document_name}"
            )

        chapter_corresponding_to_the_current_page = table_of_contents.iloc[
            only_chapters_with_page_number_less_than_current_page_df[
                "difference_between_page_and_chapters"
            ].argmax()
        ]

        chapter_title = chapter_corresponding_to_the_current_page["title"]
        if isinstance(chapter_title, str):
            return chapter_title
        return list(chapter_title)[0]

    def _get_fitz_reader(self, document_path: Path) -> fitz.Document:
        return fitz.Document(document_path)

    def get_page_image(self, page_number: int) -> Image.Image:
        pdf_page = self.reader.load_page(page_number)
        mat = fitz.Matrix(2, 2)
        pix = pdf_page.get_pixmap(matrix=mat)
        image = Image.open(io.BytesIO(pix.pil_tobytes(format="jpeg")))
        return image

    def get_page_text(self, page_number: int) -> str:
        page = self.reader.load_page(page_number).get_text("dict")
        return page


def extract_table_content_item_text(text: str) -> str:
    valid_characters = string.printable

    text_without_special_chars = "".join(i for i in text if i in valid_characters)
    text_without_special_chars_and_chapter_number = re.sub(
        r"^[0-9. ]*", "", text_without_special_chars
    )
    return text_without_special_chars_and_chapter_number


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
