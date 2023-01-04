from typing import Dict, Generator, Iterator

from highlights_extractor.constants import DATA_FOLDER
from highlights_extractor.models import (
    ChapterHighlights,
    DocumentContent,
    DocumentHighlights,
    DocumentMetadata,
    PageHighlights,
)
from highlights_extractor.process_documents import PDFExtractor
from highlights_extractor.repository.file_reader import FileReader, RawHighlightFile


def sort_page_highlights(
    page_highlights: Iterator[PageHighlights],
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


def get_highlights_per_chapter(
    raw_highlight_files: list[RawHighlightFile],
    is_saving_images: bool,
    document_content: DocumentContent,
    pdf_reader: PDFExtractor,
) -> list[ChapterHighlights]:
    all_highlights = sort_page_highlights(
        create_highlights(raw_highlight_files, is_saving_images, document_content, pdf_reader)
    )
    highlights_per_chapter = create_chapter_highlights(all_highlights)
    return highlights_per_chapter


def create_highlights(
    raw_highlight_files: list[RawHighlightFile],
    is_saving_images: bool,
    document_content: DocumentContent,
    pdf_reader: PDFExtractor,
) -> Generator[PageHighlights, None, None]:
    for highlight_file in raw_highlight_files:
        page_number = get_page_number(document_content, highlight_file)
        image = (
            pdf_reader.get_page_image(page_number, highlight_file) if is_saving_images else None
        )
        yield PageHighlights(
            raw_file=highlight_file,
            page_number=page_number,
            chapter=pdf_reader.get_chapter_title(page_number),
            image=image,
        )


def get_document_highlights(
    local_fs: FileReader, document_metadata: DocumentMetadata, is_saving_images: bool
) -> DocumentHighlights:
    document_content = DocumentContent(
        local_fs.read_document_content(document_id=document_metadata.document_id)
    )
    highlights_files = local_fs.read_document_highlights(document_metadata.document_id)
    pdf_reader = PDFExtractor(
        DATA_FOLDER / f"{document_metadata.document_id}.pdf",
        document_name=document_metadata.document_name,
    )
    chapter_highlights = get_highlights_per_chapter(
        highlights_files,
        is_saving_images,
        document_content,
        pdf_reader,
    )
    return DocumentHighlights(chapter_highlights, document_metadata.document_id)


def get_page_number(document_content: DocumentContent, page: RawHighlightFile) -> int:
    """Get the page number of a page in the document.
    To do so, we need the content file of the document and the page id of the page
    in the content file, there is two list:
        - One with the page ids
        - One with the page numbers
    We need to find the index of the corresponding page id in the list of page ids
    to get the corresponding page number.

    Args:
        document_content: content document to get the two lists
        page: page to get the page id

    Returns:
        page number of the page
    """
    page_remarkable_index = document_content.remarkable_page_ids.index(page.page_id)
    page_number = document_content.page_numbers[page_remarkable_index]
    return page_number
