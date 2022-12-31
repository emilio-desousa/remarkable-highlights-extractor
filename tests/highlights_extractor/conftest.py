# pylint: disable=protected-access, redefined-outer-name
from pathlib import Path
from typing import Callable

import pytest

from highlights_extractor.models import (
    Document,
    DocumentHighlights,
    DocumentMetadata,
    PageHighlights,
)
from highlights_extractor.repository.file_reader import RawFile, RawHighlightFile


@pytest.fixture
def make_page_highlights() -> Callable[[int], PageHighlights]:
    def _remarkable_page_highlights(page_id: int) -> PageHighlights:
        page = PageHighlights(make_raw_highlights(page_id))
        page = page.set_page_number(page_id)
        return page

    return _remarkable_page_highlights


@pytest.fixture
def make_remarkable_raw_highlights() -> Callable[[int], RawHighlightFile]:
    def _remarkable_raw_highlights(page_id: int) -> RawHighlightFile:
        return make_raw_highlights(page_id)

    return _remarkable_raw_highlights


def make_raw_highlights(page_id: int) -> RawHighlightFile:
    return RawHighlightFile(
        Path(f"doc_id.highlights/page_id_{page_id}.json"),
        [
            {"text": f"page_{page_id}_highlight_1"},
            {"text": f"page_{page_id}_highlight_2"},
        ],
    )


def remarkable_raw_content() -> RawFile:
    raw_highlight = RawFile(
        Path("doc_id.content"),
        {"pages": ["page_id_1", "page_id_2"], "redirectionPageMap": [1, 2]},
    )
    return raw_highlight


@pytest.fixture
def remarkable_document_with_2_page_highlights(
    make_remarkable_raw_highlights: Callable[[int], RawHighlightFile],
) -> Document:
    raw_highlights_1 = make_remarkable_raw_highlights(1)
    raw_highlights_2 = make_remarkable_raw_highlights(2)
    document_highlights = DocumentHighlights(
        [PageHighlights(raw_highlights_1), PageHighlights(raw_highlights_2)],
        document_id="doc_1",
    )
    document_metadata = DocumentMetadata(
        RawFile(Path("doc_id.metadata"), {"visibleName": "doc"})
    )
    return Document(document_highlights, document_metadata)
