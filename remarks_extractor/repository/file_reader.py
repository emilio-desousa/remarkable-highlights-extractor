import glob
import json
from pathlib import Path

from remarks_extractor.config import constants as cst
from remarks_extractor.config.models import RawContent, RawMetadata, RawPageHighlights
from remarks_extractor.config.types import FilesAccessibilityMode, PathHighlightsMapping
from remarks_extractor.utils import get_document_id_from_path, get_file_name_from_path


class XochitlFilesReader:
    def __init__(
        self,
        mode: FilesAccessibilityMode = "local",
        xochitl_folder: Path = cst.DATA_FOLDER,
    ) -> None:
        self.mode = mode
        self.xochitl_folder = xochitl_folder

    def get_document_highlights(self, document_id: str) -> list[RawPageHighlights]:
        highlights_files_paths = self._get_files_paths_with_glob(
            create_highlights_glob_expression(document_id)
        )
        list_of_path_highlights_content_mapping = []
        for highlights_file_path in highlights_files_paths:
            page_id_with_highlights_mapping = self._read_highlights_file(
                highlights_file_path
            )
            image_path = (
                self.xochitl_folder
                / f"{document_id}.thumbnails"
                / f'{page_id_with_highlights_mapping["page_id"]}.jpg'
            )
            raw_page_highlights = RawPageHighlights(
                document_id,
                page_id_with_highlights_mapping["page_id"],
                highlights=page_id_with_highlights_mapping["highlights"],
                image_path=image_path,
            )
            list_of_path_highlights_content_mapping.append(raw_page_highlights)
        return list_of_path_highlights_content_mapping

    def _get_files_paths_with_glob(self, glob_expression: str) -> list[str]:
        return glob.glob(str(self.xochitl_folder / glob_expression))

    @staticmethod
    def _read_highlights_file(highlights_file_path: str) -> PathHighlightsMapping:
        with open(highlights_file_path, "r", encoding="utf-8") as highlight_file_object:
            page_id_and_path_mapping = PathHighlightsMapping(
                page_id=get_file_name_from_path(highlights_file_path),
                highlights=json.load(highlight_file_object),
            )
            return page_id_and_path_mapping

    def get_document_metadata(self, document_id: str) -> RawMetadata:
        metadata_files_path = f"{self.xochitl_folder / document_id}.metadata"
        metadata_object = self._read_metadata_file(metadata_files_path)
        return RawMetadata.from_dict({"document_id": document_id, **metadata_object})

    @staticmethod
    def _read_metadata_file(
        metadata_file_path: str,
    ) -> dict:
        with open(metadata_file_path, "r", encoding="utf-8") as metadata_file_object:
            return json.load(metadata_file_object)

    def get_documents_ids(self) -> list[str]:
        content_files_paths = self._get_files_paths_with_glob(
            create_content_glob_expressions()
        )
        document_ids = [
            get_document_id_from_path(content_file_path)
            for content_file_path in content_files_paths
        ]
        return list(set(document_ids))

    def get_document_content_file(self, document_id: str) -> RawContent:
        content_file_path = f"{self.xochitl_folder / document_id}.content"
        metadata_object = self._read_content_file(content_file_path)

        return RawContent.from_dict({"document_id": document_id, **metadata_object})

    @staticmethod
    def _read_content_file(content_file_path: str) -> dict:
        with open(content_file_path, "r", encoding="utf-8") as content_file:
            return json.load(content_file)


def create_highlights_glob_expression(document_id: str) -> str:
    return f"{document_id}.highlights/*.json"


def create_metadata_glob_expressions() -> str:
    return ".metadata"


def create_content_glob_expressions() -> str:
    return "*.content"
