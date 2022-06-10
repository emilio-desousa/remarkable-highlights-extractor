# %%
import glob
import json
from dataclasses import dataclass
from pathlib import Path

from config import constants as cst

# %%


@dataclass
class document:
    file_name: str
    internal_file_name: str
    path: str


@dataclass
class Content:
    file_name: str
    content: dict

    def __str__(self) -> str:
        return f"{self.file_name}: {self.content}"


files_to_process = []
for content_file in glob.glob(str(cst.DATA_FOLDER / "*.content")):
    with open(content_file, "r") as f:
        data = json.load(f)
        if cst.CONTENT_FIELD_FILE_TYPE in data:
            if data[cst.CONTENT_FIELD_FILE_TYPE] in cst.FILE_TYPES_MANAGED:
                files_to_process.append(Content(Path(content_file).stem, data))


# %%
try:
    for highlight_file in glob.glob(
        str(cst.DATA_FOLDER / f"{files_to_process[0].file_name}.highlights/*.json")
    ):
        with open(highlight_file, "r") as f:
            data = json.load(f)
            for highlights in data["highlights"]:
                for highlight in highlights:
                    print(highlight["text"])
except Exception as ex:
    print()
    print(ex)


# %%
import pandas as pd

data = pd.read_json(cst.DATA_FOLDER / "282f0e0e-e384-4835-8b51-5c62eac250aa.content")
# %%
