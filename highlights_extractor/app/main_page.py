# %%
from pathlib import Path

import streamlit as st

from highlights_extractor.models import (
    Document,
    DocumentContent,
    DocumentHighlights,
    DocumentMetadata,
    PageHighlights,
    create_chapter_highlights,
    sort_page_highlights,
)
from highlights_extractor.process_documents import PDFReader, get_page_number
from highlights_extractor.repository.file_reader import LocalFileReader
from highlights_extractor.repository.knowledge_manager_writer import ObsidianDocument
from remarks_extractor.config.constants import DATA_FOLDER

local_fs = LocalFileReader()
metadata_files = local_fs.read_all_metadata_files(["visibleName"])
documents_metadata = [
    DocumentMetadata(metadata_file) for metadata_file in metadata_files
]
with st.sidebar:
    document_metadata = st.selectbox("document", list(documents_metadata), index=28)
    destination_path = Path(
        st.text_input(
            "Obsidian path",
            value="/Users/emiliodesousa/ghq/github.com/emilio-desousa/obsidian-vault/",
        )
    )
    images_destination_path = Path(
        st.text_input(
            "Obsidian path",
            value="/Users/emiliodesousa/ghq/github.com/emilio-desousa/obsidian-vault/07_FILES",
        )
    )
    is_saving_images = st.checkbox("Load and export page images?")

if document_metadata:
    st.header(document_metadata.document_name)
    extracting_document = st.button("Extract Document")
    highlights_files = local_fs.read_document_highlights(document_metadata.document_id)
    all_highlights = []
    document_content = DocumentContent(
        local_fs.read_document_content(document_id=document_metadata.document_id)
    )
    pdf_reader = PDFReader(
        DATA_FOLDER / f"{document_metadata.document_id}.pdf",
        document_name=document_metadata.document_name,
    )
    for highlight_file in highlights_files:
        page_number = get_page_number(document_content, highlight_file)
        image = pdf_reader.get_page_image(page_number) if is_saving_images else None
        page_highlights = PageHighlights(
            highlight_file,
            page_number,
            chapter=pdf_reader.get_chapter_title(page_number),
            image=image,
        )
        all_highlights.append(page_highlights)

    all_highlights = sort_page_highlights(all_highlights)
    highlights_per_chapter = create_chapter_highlights(all_highlights)
    doc_highlights = DocumentHighlights(
        highlights_per_chapter, document_id=document_metadata.document_id
    )
    for chapter_highlights in doc_highlights.chapters_highlights:
        st.header(chapter_highlights.chapter)
        for page in chapter_highlights.page_highlights:
            if page.image:
                st.image(page.image, width=200)
            for highlight in page.highlights:
                st.caption(highlight)

    final_document = Document(doc_highlights, document_metadata)
    obsidian_extractor = ObsidianDocument(
        vault_path=destination_path,
        image_path=images_destination_path,
        is_saving_images=is_saving_images,
    )
    if extracting_document:
        obsidian_extractor.extract_document(final_document)
