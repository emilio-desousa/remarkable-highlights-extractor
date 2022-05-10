# %%
from dataclasses import dataclass
from config import constants as cst
from pathlib import Path

import glob
import json


@dataclass
class Content:
    file_name: str
    content: dict


files_to_process = []
for content_file in glob.glob(str(cst.DATA_FOLDER / "*.content")):
    with open(content_file, "r") as f:
        data = json.load(f)
        if cst.CONTENT_FIELD_FILE_TYPE in data:
            if data[cst.CONTENT_FIELD_FILE_TYPE] in cst.FILE_TYPES_MANAGED:
                files_to_process.append(Content(Path(content_file).stem, data))


# %%
for highlight_file in glob.glob(
    str(cst.DATA_FOLDER / f"{files_to_process[0]}.highlights/*.json")
):
    with open(highlight_file, "r") as f:
        data = json.load(f)
        for highlights in data["highlights"]:
            for highlight in highlights:
                print(highlight["text"])


# %%
