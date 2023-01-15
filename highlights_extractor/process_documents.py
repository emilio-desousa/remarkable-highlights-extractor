import io
from dataclasses import dataclass
from pathlib import Path
from typing import List

import fitz
import pandas as pd
from PIL import Image

from highlights_extractor.config.exceptions import DocumentNotProcessableError
from highlights_extractor.repository.file_reader import RawHighlightFile

REMARKABLE_HEIGHT = 1872
REMARKABLE_WIDTH = 1300


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

    def _get_fitz_reader(self, document_path: Path) -> fitz.Document:
        return fitz.Document(document_path)

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

    def _get_most_closest_chapter_before_page(
        self, only_chapters_before_current_page_df: pd.DataFrame
    ) -> pd.DataFrame:
        chapter_corresponding_to_the_current_page = only_chapters_before_current_page_df.iloc[
            only_chapters_before_current_page_df["difference_between_page_and_chapters"].argmax()
        ]
        return chapter_corresponding_to_the_current_page

    def get_page_image(
        self, page_number: int, highlight_file: RawHighlightFile, image_zoom: int = 1
    ) -> Image.Image:
        """Get the image of a page with the highlights on it. The highlights are
        extracted from the highlight file.
        But the scale of the pdf and the highlights are not the same, so we need to
        scale the highlights to the pdf scale.

        Args:
            page_number: page number of the highlight
            highlight_file: raw highlight file that contains all the highlights boxes
            image_zoom: zoom to show and store the image. For example, a zoom of 2 means a better
                quality of the image but it will be bigger in memory. Defaults to 1.

        Returns:
            image of the page with the highlights on it
        """
        pdf_page = self.reader.load_page(page_number)
        highlights_boxes = self._get_highlights_boxes(highlight_file.content, pdf_page)
        pdf_page.add_highlight_annot(highlights_boxes, clip=True)
        image = self._create_image_python_object(image_zoom, pdf_page)
        return image

    def _get_highlights_boxes(
        self, highlight_contents: list[dict], pdf_page: fitz.Page
    ) -> list[fitz.Quad]:
        pdf_height = pdf_page.rect.height
        pdf_width = pdf_page.rect.width
        scale_width = pdf_width / REMARKABLE_WIDTH
        scale_height = pdf_height / REMARKABLE_HEIGHT
        highlights_boxes = []

        for content in highlight_contents:
            for rect in content["rects"]:
                x1_highlight_in_pdf = rect["x"] * scale_width
                x2_highlight_in_pdf = x1_highlight_in_pdf + (rect["width"] * scale_width)
                y1_highlight_in_pdf = rect["y"] * scale_height
                y2_highlight_in_pdf = y1_highlight_in_pdf + (rect["height"] * scale_height)
                quad = self._create_quad(
                    x1_highlight_in_pdf,
                    x2_highlight_in_pdf,
                    y1_highlight_in_pdf,
                    y2_highlight_in_pdf,
                )
                highlights_boxes.append(quad)
        return highlights_boxes

    def _create_quad(
        self,
        x1_highlight_in_pdf: float,
        x2_highlight_in_pdf: float,
        y1_highlight_in_pdf: float,
        y2_highlight_in_pdf: float,
    ) -> fitz.Quad:
        point_1_top_left = fitz.Point(x1_highlight_in_pdf, y1_highlight_in_pdf)
        point_2_top_right = fitz.Point(x2_highlight_in_pdf, y1_highlight_in_pdf)
        point_3_bottom_left = fitz.Point(x1_highlight_in_pdf, y2_highlight_in_pdf)
        point_4_bottom_right = fitz.Point(x2_highlight_in_pdf, y2_highlight_in_pdf)
        return fitz.Quad(
            point_1_top_left, point_2_top_right, point_3_bottom_left, point_4_bottom_right
        )

    def _create_image_python_object(self, image_zoom: int, pdf_page: fitz.Page) -> Image.Image:
        pix = pdf_page.get_pixmap(matrix=fitz.Matrix(image_zoom, image_zoom))  # type: ignore
        image = Image.open(io.BytesIO(pix.pil_tobytes(format="jpeg")))
        return image
