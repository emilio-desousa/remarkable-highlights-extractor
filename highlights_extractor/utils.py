from pathlib import Path
from typing import Dict

from highlights_extractor.models import ChapterHighlights, PageHighlights


def extract_document_id_from_path(path: Path) -> str:
    match path.suffix:
        case ".json":
            return path.parent.stem
        case ".content" | ".epub" | ".epubindex" | ".metadata" | ".pagedata" | ".pdf":
            return path.stem
        case _:
            raise ValueError(
                f"""{path} is not an expected Xochitl file
            Expected format: Highlights, Content, Metadata, PDF, EPUB"""
            )


def extract_page_id_from_path(path: Path) -> str:
    match path.suffix:
        case ".json":
            return path.stem
        case _:
            raise ValueError(f"{path} is not an expected Xochitl page file")


def recursive_function_to_get_all_dicts(highlights: list) -> list:
    list_of_dict = []
    for dict_or_list in highlights:
        if isinstance(dict_or_list, dict):
            list_of_dict.append(dict_or_list)
        else:
            list_of_dict = list_of_dict + recursive_function_to_get_all_dicts(dict_or_list)

    return list_of_dict


def sort_page_highlights(
    page_highlights: list[PageHighlights],
) -> list[PageHighlights]:
    return sorted(page_highlights, key=lambda x: x.page_number)


def create_chapter_highlights(
    pages_highlights: list[PageHighlights],
) -> list[ChapterHighlights]:
    pages_per_chapter: Dict[str, list[PageHighlights]] = {}
    for page in pages_highlights:
        pages_per_chapter[page.chapter] = pages_per_chapter.get(page.chapter, []) + [page]
    highlights_per_chapter = [
        ChapterHighlights(chapter, pages) for chapter, pages in pages_per_chapter.items()
    ]
    return highlights_per_chapter
