## READ ALL FILES
##  - read all content files
##  - create Content objects
##  - read all metadata files for wanted files (pdf??)
##      - get only visible name from it
from typing import List

import pandas as pd
from config.constants import DATA_FOLDER


def read_metadata_files() -> None:
    pass


def read_content_files(xochitl_folder: str) -> None:

    data = pd.read_json(DATA_FOLDER / "282f0e0e-e384-4835-8b51-5c62eac250aa.content")
    pass


def read_highlights_files() -> None:
    pass
