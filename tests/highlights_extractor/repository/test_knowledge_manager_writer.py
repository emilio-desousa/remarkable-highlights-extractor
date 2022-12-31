# pylint: disable=protected-access, redefined-outer-name
from pathlib import Path

import pytest

from highlights_extractor.models import Document
from highlights_extractor.repository.knowledge_manager_writer import ObsidianDocument


@pytest.fixture
def my_obsidian_extractor() -> ObsidianDocument:
    return ObsidianDocument(Path(__file__).parent, Path())


def test_add_metadata(my_obsidian_extractor: ObsidianDocument) -> None:
    assert (
        my_obsidian_extractor._add_metadata("DATE")
        == "\n> Timestamp: DATE\n> Status:\n> Tags:\n"
    )


def test_add_header_1(my_obsidian_extractor: ObsidianDocument) -> None:
    assert my_obsidian_extractor._add_header_1("H1") == "\n# H1"


def test_add_header_2(my_obsidian_extractor: ObsidianDocument) -> None:
    assert my_obsidian_extractor._add_header_2("H2") == "\n## H2"


def test_add_header_3(my_obsidian_extractor: ObsidianDocument) -> None:
    assert my_obsidian_extractor._add_header_3("H3") == "\n### H3"


def test_add_page_quotes(my_obsidian_extractor: ObsidianDocument) -> None:
    quote_admonition = "\n```ad-quote\nline1\nline2\n```"
    assert (
        my_obsidian_extractor._add_page_quotes(["line1", "line2"]) == quote_admonition
    )


def test_format_document(
    my_obsidian_extractor: ObsidianDocument,
    remarkable_document_with_2_page_highlights: Document,
) -> None:
    expected_formatted_document = (
        "\n### 1\n```ad-quote\npage_1_highlight_1\npage_1_highlight_2\n```"
        "\n### 2\n```ad-quote\npage_2_highlight_1\npage_2_highlight_2\n```"
    )

    actual_document_formatted_content = my_obsidian_extractor.format_document(
        remarkable_document_with_2_page_highlights
    )
    assert expected_formatted_document == actual_document_formatted_content
