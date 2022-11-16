import streamlit as st

from highlights_extractor.models import (
    DocumentHighlights,
    DocumentMetadata,
    PageHighlights,
)
from highlights_extractor.repository.file_reader import LocalFileReader

local_fs = LocalFileReader()
metadata_files = local_fs.read_all_metadata_files(["visibleName"])
documents_metadata = [
    DocumentMetadata(metadata_file) for metadata_file in metadata_files
]

with st.sidebar:
    document = st.selectbox("document", list(documents_metadata))
if document:
    highlights_files = local_fs.read_document_highlights(document.document_id)
    all_highlights = []
    for highlight_file in highlights_files:
        page_highlights = PageHighlights(highlight_file)
        all_highlights.append(page_highlights)
        st.write(str(page_highlights))
        st.write(page_highlights.raw_file.file_path)
    doc_highlights = DocumentHighlights(all_highlights)
    st.write(str(doc_highlights))
