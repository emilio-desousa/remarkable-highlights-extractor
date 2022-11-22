from pathlib import Path

import pytest

from highlights_extractor.utils import extract_document_id_from_path


def test_extract_document_id_from_path() -> None:
    expected_document_id = "84cb2541-e92c-4ad1-ab74-2cf22bac8615"
    actual_document_id = extract_document_id_from_path(
        Path("Users/a/b/data/xochitl/84cb2541-e92c-4ad1-ab74-2cf22bac8615.content")
    )
    assert actual_document_id == expected_document_id


def test_extract_document_id_from_path_from_highlight_file() -> None:
    expected_document_id = "1ef483b1-a177-488b-b942-c049adaed58c"
    actual_document_id = extract_document_id_from_path(
        Path(
            "/xochitl/1ef483b1-a177-488b-b942-c049adaed58c.highlights/0f65c700-8d22-48b2-a918-977f0f45826a.json"
        )
    )
    assert actual_document_id == expected_document_id


def test_extract_document_id_from_path_should_raise_value_error_with_not_expected_file() -> (
    None
):
    path = Path(
        "/xochitl/1ef483b1-a177-488b-b942-c049adaed58c/0f65c700-8d22-48b2-a918-977f0f45826a.rm"
    )
    with pytest.raises(ValueError):
        extract_document_id_from_path(path)
