from typing import Literal, TypedDict


class PathHighlightsMapping(TypedDict):
    page_id: str
    highlights: dict[str, list[dict]]


class DocumentIDandDocumentNameMapping(TypedDict):
    document_id: str
    metadata: dict


FilesAccessibilityMode = Literal["cloud", "ssh", "local"]
FileTypes = list[Literal["pdf", "epub", "notebook"]]
