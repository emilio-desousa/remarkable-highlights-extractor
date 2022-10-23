from pathlib import Path

from remarks_extractor.config.models import RawPageHighlights

DUMMY_INT_VALUE = 0


def test_generate_empty_highlights():
    raw_highlights = {"highlights": []}
    page_highlights = RawPageHighlights(
        "doc_id", "page_id", raw_highlights, Path("bla")
    )
    expected_raw_page_highlights = []
    assert page_highlights.highlights == expected_raw_page_highlights


def test_generate_empty_dict():
    raw_highlights = {}
    page_highlights = RawPageHighlights(
        "doc_id", "page_id", raw_highlights, Path("bla")
    )
    expected_raw_page_highlights = []
    assert page_highlights.highlights == expected_raw_page_highlights


def test_generate_highlights():
    raw_highlights = {
        "highlights": [
            [
                {
                    "color": DUMMY_INT_VALUE,
                    "length": DUMMY_INT_VALUE,
                    "rects": [
                        {
                            "height": DUMMY_INT_VALUE,
                            "width": DUMMY_INT_VALUE,
                            "x": DUMMY_INT_VALUE,
                            "y": DUMMY_INT_VALUE,
                        }
                    ],
                    "start": DUMMY_INT_VALUE,
                    "text": "highlight_test",
                }
            ]
        ]
    }

    page_highlights = RawPageHighlights(
        "doc_id", "page_id", raw_highlights, Path("bla")
    )
    expected_raw_page_highlights = [
        {
            "color": DUMMY_INT_VALUE,
            "length": DUMMY_INT_VALUE,
            "rects": [
                {
                    "height": DUMMY_INT_VALUE,
                    "width": DUMMY_INT_VALUE,
                    "x": DUMMY_INT_VALUE,
                    "y": DUMMY_INT_VALUE,
                }
            ],
            "start": DUMMY_INT_VALUE,
            "text": "highlight_test",
        }
    ]
    assert page_highlights.highlights == expected_raw_page_highlights


def test_generate_highlights_with_two_highlights_at_the_first_level():
    raw_highlights = {
        "highlights": [
            [
                {
                    "color": DUMMY_INT_VALUE,
                    "length": DUMMY_INT_VALUE,
                    "rects": [
                        {
                            "height": DUMMY_INT_VALUE,
                            "width": DUMMY_INT_VALUE,
                            "x": DUMMY_INT_VALUE,
                            "y": DUMMY_INT_VALUE,
                        }
                    ],
                    "start": DUMMY_INT_VALUE,
                    "text": "highlight_test",
                }
            ],
            [
                {
                    "color": DUMMY_INT_VALUE,
                    "length": DUMMY_INT_VALUE,
                    "rects": [
                        {
                            "height": DUMMY_INT_VALUE,
                            "width": DUMMY_INT_VALUE,
                            "x": DUMMY_INT_VALUE,
                            "y": DUMMY_INT_VALUE,
                        }
                    ],
                    "start": DUMMY_INT_VALUE,
                    "text": "highlight_test",
                }
            ],
        ]
    }

    page_highlights = RawPageHighlights(
        "doc_id", "page_id", raw_highlights, Path("bla")
    )
    expected_raw_page_highlights = [
        {
            "color": DUMMY_INT_VALUE,
            "length": DUMMY_INT_VALUE,
            "rects": [
                {
                    "height": DUMMY_INT_VALUE,
                    "width": DUMMY_INT_VALUE,
                    "x": DUMMY_INT_VALUE,
                    "y": DUMMY_INT_VALUE,
                }
            ],
            "start": DUMMY_INT_VALUE,
            "text": "highlight_test",
        },
        {
            "color": DUMMY_INT_VALUE,
            "length": DUMMY_INT_VALUE,
            "rects": [
                {
                    "height": DUMMY_INT_VALUE,
                    "width": DUMMY_INT_VALUE,
                    "x": DUMMY_INT_VALUE,
                    "y": DUMMY_INT_VALUE,
                }
            ],
            "start": DUMMY_INT_VALUE,
            "text": "highlight_test",
        },
    ]
    assert page_highlights.highlights == expected_raw_page_highlights
