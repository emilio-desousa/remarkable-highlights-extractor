import io
from dataclasses import dataclass
from pathlib import Path
from typing import List

import fitz
import pandas as pd
from PIL import Image

from highlights_extractor.config.exceptions import DocumentNotProcessableError
from highlights_extractor.models import DocumentContent
from highlights_extractor.repository.file_reader import RawHighlightFile


@dataclass
class TableOfContentItem:
    """Class to represent a table of content item."""

    level: int
    title: str
    page: int


class PDFExtractor:
    """Class to read and extract information from a PDF document."""

    def __init__(self, document_path: Path, document_name: str) -> None:
        self.reader = self._get_fitz_reader(document_path)
        self.document_name = document_name

    def get_chapter_title(self, page_number: int) -> str:
        """Get the chapter title for a given page number.
        The way this works is that it gets the table of contents and then
        take the page number of the highlight page, find it in the table of contents
        and return the corresponding chapter title.
        Ex:
            If the table of contents is:
                1. Introduction (page 1)
                2. Chapter 1 (page 5)
            and we want to get the chapter title for our highlight that is page 4, it will return
            the chapter title for page 1, which is "Introduction".
        Args:
            page_number: page number of the highlight

        Raises:
            DocumentNotProcessableError: if the document does not have a table of contents

        Returns:
            the chapter title for the given page number
        """
        table_of_content_items = self._get_raw_table_of_contents()
        table_of_contents = self._get_table_of_contents_df(table_of_content_items)

        only_chapters_before_current_page_df = self._get_only_chapters_before_current_page(
            page_number, table_of_contents
        )
        if only_chapters_before_current_page_df.empty:
            raise DocumentNotProcessableError(
                f"Could not find chapter title for page: {page_number} in {self.document_name}"
            )
        chapter_corresponding_to_the_current_page = self._get_most_closest_chapter_before_page(
            only_chapters_before_current_page_df
        )
        chapter_title = chapter_corresponding_to_the_current_page["title"]
        if isinstance(chapter_title, str):
            return chapter_title
        return list(chapter_title)[0]

    def get_page_image(self, page_number: int) -> Image.Image:
        """Get the image of a page in the document.
        It is a bit hacky so if you have a better way to do it, please let me know by opening
        an issue on the repo.

        Args:
            page_number: page number of the highlight

        Returns:
            image of the page
        """
        pdf_page = self.reader.load_page(page_number)
        zoom = 2
        mat = fitz.Matrix(zoom, zoom)
        pix = pdf_page.get_pixmap(matrix=mat)
        image = Image.open(io.BytesIO(pix.pil_tobytes(format="jpeg")))
        return image

    def get_page_text(self, page_number: int) -> str:
        page = self.reader.load_page(page_number).get_text("dict")
        return page

    def _get_most_closest_chapter_before_page(
        self, only_chapters_before_current_page_df: pd.DataFrame
    ) -> pd.DataFrame:
        chapter_corresponding_to_the_current_page = only_chapters_before_current_page_df.iloc[
            only_chapters_before_current_page_df["difference_between_page_and_chapters"].argmax()
        ]
        return chapter_corresponding_to_the_current_page

    def _get_only_chapters_before_current_page(
        self, page_number: int, table_of_contents: pd.DataFrame
    ) -> pd.DataFrame:
        tmp_column = "difference_between_page_and_chapters"
        table_of_contents = table_of_contents.assign(
            **{tmp_column: lambda df: df["page"] - page_number}
        )
        only_chapters_with_page_number_less_than_current_page_df = table_of_contents[
            table_of_contents[tmp_column] <= 0
        ]

        return only_chapters_with_page_number_less_than_current_page_df

    def _get_raw_table_of_contents(self) -> List[TableOfContentItem]:
        if table_of_content := self.reader.get_toc():  # type: ignore
            return [TableOfContentItem(*item) for item in table_of_content]

        raise DocumentNotProcessableError(
            f"Document: {self.document_name} does not have a table of contentsor it"
            " cannot be found."
        )

    @staticmethod
    def _get_table_of_contents_df(
        raw_table_of_content: List[TableOfContentItem],
    ) -> pd.DataFrame:
        table_of_contents = pd.DataFrame(raw_table_of_content, columns=["level", "title", "page"])
        return table_of_contents

    def _get_fitz_reader(self, document_path: Path) -> fitz.Document:
        return fitz.Document(document_path)


def get_page_number(document_content: DocumentContent, page: RawHighlightFile) -> int:
    """Get the page number of a page in the document.
    To do so, we need the content file of the document and the page id of the page
    in the content file, there is two list:
        - One with the page ids
        - One with the page numbers
    We need to find the index of the corresponding page id in the list of page ids
    to get the corresponding page number.

    Args:
        document_content: content document to get the two lists
        page: page to get the page id

    Returns:
        page number of the page
    """
    page_remarkable_index = document_content.remarkable_page_ids.index(page.page_id)
    page_number = document_content.page_numbers[page_remarkable_index]
    return page_number
