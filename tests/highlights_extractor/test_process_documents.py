# pylint: disable=protected-access
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from highlights_extractor.config.exceptions import DocumentNotProcessableError
from highlights_extractor.process_documents import (
    PDFExtractor,
    TableOfContentItem,
    clean_table_content_item_text,
)
from tests.constants import DATA_FOLDER


@pytest.fixture(name="pdf_reader")
def get_pdf_reader() -> PDFExtractor:
    reader = PDFExtractor(DATA_FOLDER / "software-craft.pdf", "software-craft")
    return reader


@pytest.mark.parametrize(
    "table_of_contents, expected_table_of_contents",
    [
        (None, None),
        (
            [
                TableOfContentItem(*[0, "1.4\u2002Anatomie d’un test", 0]),
                TableOfContentItem(*[1, "2 3\u2002\x07Règles des 3 étapes", 1]),
            ],
            [[0, "Anatomie dun test", 0], [1, "Rgles des 3 tapes", 1]],
        ),
    ],
    ids=["empty", "with_content_to_clean"],
)
def test_get_page_text(
    table_of_contents: list[TableOfContentItem],
    expected_table_of_contents: pd.DataFrame,
    pdf_reader: PDFExtractor,
) -> None:
    table_of_contents_df = pdf_reader._get_table_of_contents_df(table_of_contents)

    expected_table_of_contents_df = pd.DataFrame(
        expected_table_of_contents, columns=["level", "title", "page"]
    )
    assert_frame_equal(expected_table_of_contents_df, table_of_contents_df)


@pytest.mark.parametrize(
    "table_content_item_text, expected_text_without_unicode_and_chapter_number",
    [
        ("1.4\u2002Anatomie d’un test", "Anatomie dun test"),
        ("2 3\u2002\x07Règles des 3 étapes", "Rgles des 3 tapes"),
        ("", ""),
    ],
    ids=[
        "unicode with chapter number",
        "unicode and hexa code with chapter number",
        "empty_string",
    ],
)
def test_extract_table_content_item_text(
    table_content_item_text: str, expected_text_without_unicode_and_chapter_number: str
) -> None:
    actual_text = clean_table_content_item_text(table_content_item_text)
    assert expected_text_without_unicode_and_chapter_number == actual_text


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
