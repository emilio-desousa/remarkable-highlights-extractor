from pathlib import Path

from remarks_extractor.config.types import FileTypes

ROOT_FOLDER = Path(__file__).parent.parent.parent
DATA_FOLDER = ROOT_FOLDER / "data/xochitl"

CONTENT_FIELD_FILE_TYPE = "fileType"


FILE_TYPES_MANAGED: FileTypes = ["pdf", "epub"]
