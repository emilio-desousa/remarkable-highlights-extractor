# %%
from pathlib import Path

import streamlit as st

from highlights_extractor.models import (
    Document,
    DocumentContent,
    DocumentHighlights,
    DocumentMetadata,
    PageHighlights,
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
    document_metadata = st.selectbox("document", list(documents_metadata))
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

if document_metadata:
    st.header(document_metadata.document_name)
    extracting_document = st.button("Extract Document")
    highlights_files = local_fs.read_document_highlights(document_metadata.document_id)
    all_highlights = []
    document_content = DocumentContent(
        local_fs.read_document_content(document_id=document_metadata.document_id)
    )
    pdf_reader = PDFReader(DATA_FOLDER / f"{document_metadata.document_id}.pdf")
    for highlight_file in highlights_files:
        page_highlights = PageHighlights(highlight_file)
        page_number = get_page_number(document_content, page_highlights)
        page_highlights.set_page_number(page_number)
        if pdf_reader:
            page_image = pdf_reader.get_page_image(page_number)
            page_highlights.set_page_image(page_image)
        all_highlights.append(page_highlights)
    doc_highlights = DocumentHighlights(
        all_highlights, document_id=document_metadata.document_id
    )
    for page_highlights in doc_highlights.page_highlights:
        st.header(page_highlights.page_number)
        if page_highlights.image:
            st.image(page_highlights.image)
        st.write(page_highlights.highlights)

    final_document = Document(doc_highlights, document_metadata)
    obsidian_extractor = ObsidianDocument(
        vault_path=destination_path, image_path=images_destination_path
    )
    if extracting_document:
        obsidian_extractor.extract_document(final_document)
