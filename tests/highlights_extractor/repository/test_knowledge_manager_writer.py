# pylint: disable=protected-access, redefined-outer-name
from pathlib import Path

import pytest

from highlights_extractor.repository.knowledge_manager_writer import ObsidianDocument


@pytest.fixture
def my_obsidian_extractor() -> ObsidianDocument:
    return ObsidianDocument(Path(__file__).parent)


def test_add_metadata(my_obsidian_extractor: ObsidianDocument) -> None:
    assert (
        my_obsidian_extractor._add_metadata("DATE")
        == "\n> Timestamp: DATE\n> Status:\n> Tags:\n"
    )


def test_add_header_1(my_obsidian_extractor: ObsidianDocument) -> None:
    assert my_obsidian_extractor._add_header_1("H1") == "\n# H1\n"


def test_add_header_2(my_obsidian_extractor: ObsidianDocument) -> None:
    assert my_obsidian_extractor._add_header_2("H2") == "\n## H2\n"


def test_add_header_3(my_obsidian_extractor: ObsidianDocument) -> None:
    assert my_obsidian_extractor._add_header_3("H3") == "\n### H3\n"


def test_add_page_quotes(my_obsidian_extractor: ObsidianDocument) -> None:
    quote_admonition = "\n```ad-quote\nline1\nline2\n```"
    assert (
        my_obsidian_extractor._add_page_quotes(["line1", "line2"]) == quote_admonition
    )
