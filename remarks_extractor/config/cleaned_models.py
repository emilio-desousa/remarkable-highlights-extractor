from dataclasses import dataclass

from remarks_extractor.config.models import RawContent, RawMetadata, RawPageHighlights
from remarks_extractor.config.types import FileTypes


@dataclass
class Document:
    """Trying to implement the builder pattern (GoF)"""

    document_id: str
    highlights: list[RawPageHighlights]
    content: RawContent
    metadata: RawMetadata

    def is_applicable(self, applicable_file_types: FileTypes) -> bool:
        return self.content.fileType in (applicable_file_types)

    def __repr__(self) -> str:
        return f"{self.metadata.visibleName}"

    def __str__(self) -> str:
        return f"{self.metadata.visibleName}"
