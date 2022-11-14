import streamlit as st

from highlights_extractor.file_reader import LocalFileReader
from highlights_extractor.models import DocumentMetadata

local_fs = LocalFileReader()
metadata_files = local_fs.read_all_metadata_files(["visibleName"])
documents_metadata = [
    DocumentMetadata(metadata_file) for metadata_file in metadata_files
]

with st.sidebar:
    st.selectbox(
        "document",
        [document_metadata.document_name for document_metadata in documents_metadata],
    )
