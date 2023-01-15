# pylint: disable=protected-access
import pytest

from highlights_extractor.config.exceptions import DocumentNotProcessableError
from highlights_extractor.process_documents import PDFExtractor, TableOfContentItem
from tests.constants import DATA_FOLDER


@pytest.fixture(name="pdf_reader")
def get_pdf_reader() -> PDFExtractor:
    reader = PDFExtractor(DATA_FOLDER / "software-craft.pdf", "software-craft")
    return reader


@pytest.mark.parametrize(
    "table_of_content,page_number, expected_chapter_title",
    [
        (
            [
                TableOfContentItem(0, "toc_1", 0),
                TableOfContentItem(0, "toc_2", 1),
                TableOfContentItem(0, "toc_3", 10),
            ],
            4,
            "toc_2",
        ),
        (
            [
                TableOfContentItem(0, "toc_1", 0),
            ],
            0,
            "toc_1",
        ),
    ],
    ids=[
        "page number in the middle of a chapter",
        "page number at the beginning of a chapter",
    ],
)
def test_get_chapter_title(
    table_of_content: list[TableOfContentItem],
    page_number: int,
    expected_chapter_title: str,
    pdf_reader: PDFExtractor,
) -> None:
    pdf_reader._get_raw_table_of_contents = lambda: table_of_content
    chapter_title = pdf_reader.get_chapter_title(page_number)
    assert chapter_title == expected_chapter_title


def test_get_chapter_title_from_a_invalid_pdf() -> None:
    pdf_reader = PDFExtractor(DATA_FOLDER / "not_a_book.pdf", "not_a_book")
    dummy_page_number = 0
    with pytest.raises(DocumentNotProcessableError):
        pdf_reader.get_chapter_title(dummy_page_number)


def test_get_chapter_title_from_a_page_not_in_the_table_of_content(
    pdf_reader: PDFExtractor,
) -> None:
    pdf_reader._get_raw_table_of_contents = lambda: [TableOfContentItem(0, "toc_1", 0)]
    page_number_not_in_the_table_of_content = -1
    with pytest.raises(DocumentNotProcessableError):
        pdf_reader.get_chapter_title(page_number_not_in_the_table_of_content)
