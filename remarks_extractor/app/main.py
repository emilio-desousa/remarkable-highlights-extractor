# %%
import streamlit as st

from remarks_extractor.config.cleaned_models import Document
from remarks_extractor.extractor.remarks import (
    map_content_files_with_metadata_and_highlights,
)
from remarks_extractor.repository.file_reader import XochitlFilesReader

all_documents = map_content_files_with_metadata_and_highlights(XochitlFilesReader())
# %%
selected_document: Document | None = st.sidebar.selectbox("select one", all_documents)
# %%
if selected_document:
    st.write(selected_document.highlights)
