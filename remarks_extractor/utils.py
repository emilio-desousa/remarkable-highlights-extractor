from pathlib import Path


def get_document_id_from_path(file_path: str) -> str:
    if file_path.endswith(".json"):
        return Path(file_path).parent.stem
    return get_file_name_from_path(file_path)


def get_file_name_from_path(file_path: str) -> str:
    return Path(file_path).stem


def recursive_function_to_get_all_dicts(highlights: list):
    list_of_dict = []
    for dict_or_list in highlights:
        if isinstance(dict_or_list, dict):
            list_of_dict.append(dict_or_list)
        else:
            list_of_dict = list_of_dict + recursive_function_to_get_all_dicts(
                dict_or_list
            )

    return list_of_dict
