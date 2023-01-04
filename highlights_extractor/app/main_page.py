# %%
from pathlib import Path

import streamlit as st

from highlights_extractor.model_utils import get_document_highlights
from highlights_extractor.models import Document, DocumentMetadata
from highlights_extractor.repository.file_reader import LocalFileReader
from highlights_extractor.repository.knowledge_manager_writer import ObsidianDocument

local_fs = LocalFileReader()
metadata_files = local_fs.read_all_metadata_files(["visibleName"])
documents_metadata = [DocumentMetadata(metadata_file) for metadata_file in metadata_files]
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

    document_highlights = get_document_highlights(local_fs, document_metadata, is_saving_images)

    for chapter_highlights in document_highlights:
        st.header(chapter_highlights.chapter)
        for page in chapter_highlights:
            if page.image:
                st.image(page.image)
            for highlight in page.highlights:
                st.caption(highlight)

    final_document = Document(document_highlights, document_metadata)
    obsidian_extractor = ObsidianDocument(
        vault_path=destination_path,
        image_path=images_destination_path,
        is_saving_images=is_saving_images,
    )
    if extracting_document:
        obsidian_extractor.extract_document(final_document)
