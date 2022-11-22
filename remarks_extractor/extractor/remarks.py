from typing import Generator

from remarks_extractor.config.cleaned_models import Document
from remarks_extractor.config.constants import FILE_TYPES_MANAGED
from remarks_extractor.config.exceptions import FieldsNotDefinedInFile
from remarks_extractor.repository.file_reader import XochitlFilesReader


def map_content_files_with_metadata_and_highlights(
    file_reader: XochitlFilesReader,
) -> Generator[Document, None, None]:
    documents_ids = file_reader.get_documents_ids()

    for document_id in documents_ids:
        try:
            aggregated_document = Document(
                document_id=document_id,
                highlights=file_reader.get_document_highlights(document_id),
                metadata=file_reader.get_document_metadata(document_id),
                content=file_reader.get_document_content_file(document_id),
            )
        except FieldsNotDefinedInFile:
            continue

        if not aggregated_document.is_applicable(FILE_TYPES_MANAGED):
            continue

        yield aggregated_document
