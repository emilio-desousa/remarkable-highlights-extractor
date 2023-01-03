from typing import Callable

from highlights_extractor.models import PageHighlights, sort_page_highlights


def test_sorting_page_highlights_without_already_sorted_list(
    make_page_highlights: Callable[[int], PageHighlights],
) -> None:
    page_0_highlights = make_page_highlights(0)
    page_1_highlights = make_page_highlights(1)
    pages = [page_1_highlights, page_0_highlights]
    sorted_pages = sort_page_highlights(pages)
    assert sorted_pages == [page_0_highlights, page_1_highlights]


def test_sorting_page_highlights(make_page_highlights: Callable[[int], PageHighlights]) -> None:
    page_0_highlights = make_page_highlights(0)
    page_1_highlights = make_page_highlights(1)
    pages = [page_0_highlights, page_1_highlights]
    sorted_pages = sort_page_highlights(pages)
    assert sorted_pages == [page_0_highlights, page_1_highlights]
