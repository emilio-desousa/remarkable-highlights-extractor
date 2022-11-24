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
