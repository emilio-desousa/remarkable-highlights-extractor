from pathlib import Path


def extract_document_id_from_path(path: Path) -> str:
    match path.suffix:
        case ".json":
            return path.parent.stem
        case ".content" | ".epub" | ".epubindex" | ".metadata" | ".pagedata" | ".pdf":
            return path.stem
        case _:
            raise ValueError(
                f"""{path} is not an expected Xochitl file
            Expected format: Highlights, Content, Metadata, PDF, EPUB"""
            )


def extract_page_id_from_path(path: Path) -> str:
    match path.suffix:
        case ".json":
            return path.stem
        case _:
            raise ValueError(f"{path} is not an expected Xochitl page file")


def recursive_function_to_get_all_dicts(highlights: list) -> list:
    list_of_dict = []
    for dict_or_list in highlights:
        if isinstance(dict_or_list, dict):
            list_of_dict.append(dict_or_list)
        else:
            list_of_dict = list_of_dict + recursive_function_to_get_all_dicts(dict_or_list)

    return list_of_dict
