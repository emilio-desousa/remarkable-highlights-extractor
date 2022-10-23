# %%
# pylint: disable=invalid-name, too-many-instance-attributes
import abc
import inspect
from dataclasses import dataclass
from pathlib import Path
from typing import List, Literal, Optional, TypedDict, Union

from remarks_extractor.config.exceptions import FieldsNotDefinedInFile
from remarks_extractor.utils import recursive_function_to_get_all_dicts


@dataclass
class XochitlFile(metaclass=abc.ABCMeta):
    document_id: str

    @classmethod
    def from_dict(cls, env: dict) -> "XochitlFile":
        try:
            return cls(
                **{
                    k: v
                    for k, v in env.items()
                    if k in inspect.signature(cls).parameters
                }
            )
        except TypeError as exc:
            raise FieldsNotDefinedInFile(str(exc)) from exc


@dataclass
class RawContent(XochitlFile):
    coverPageNumber: int
    documentMetadata: dict
    dummyDocument: bool
    extraMetadata: dict
    fileType: Union[Literal["notebook"], Literal["pdf"], Literal["epub"]]
    fontName: str
    lineHeight: int
    margins: int
    orientation: str
    originalPageCount: int
    pageCount: int
    pages: List[str]
    sizeInBytes: str
    textAlignment: str
    textScale: int
    lastOpenedPage: Optional[int] = None
    formatVersion: Optional[str] = None
    redirectionPageMap: Optional[list] = None

    def __str__(self) -> str:
        return f"{self.document_id}: {self.fileType}"

    def __repr__(self) -> str:
        return f"{self.document_id}: {self.fileType}"

    # def __post_init__(self):
    #     if self.redirectionPageMap and len(self.pages) == len(self.redirectionPageMap):
    #         self.pages = [
    #             Page(document_id=self.id, page_id=page_id, page_number=page_number)
    #             for page_id, page_number in zip(self.pages, self.redirectionPageMap)
    # ]


@dataclass
class RawMetadata(XochitlFile):
    deleted: bool
    lastModified: str
    metadatamodified: bool
    modified: bool
    parent: str
    pinned: bool
    synced: bool
    type: Union[Literal["DocumentType"], Literal["CollectionType"]]
    version: int
    visibleName: str
    lastOpened: Optional[str] = ""
    lastOpenedPage: Optional[int] = 0


class RawHighlights(TypedDict):
    text: str
    color: int
    length: int
    start: int
    rects: List[dict]


class RawPageHighlights(XochitlFile):
    def __init__(
        self, document_id: str, page_id: str, highlights: dict, image_path: Path
    ) -> None:
        self.document_id = document_id
        self.page_id = page_id
        self.highlights = recursive_function_to_get_all_dicts(
            highlights.get("highlights", [])
        )
        self.image_path = image_path

    def __repr__(self) -> str:
        string = str(self.image_path)
        return string + str([highlight["text"] for highlight in self.highlights])

    def __str__(self) -> str:
        string = str(self.image_path)
        return string + str([highlight["text"] for highlight in self.highlights])
