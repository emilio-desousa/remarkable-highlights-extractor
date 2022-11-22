import abc
from pathlib import Path

from highlights_extractor.models import Document


class MarkdownWriter:
    # pylint: disable=too-few-public-methods
    @staticmethod
    def _is_correct_markdown_file(file_path: Path) -> bool:
        return file_path.suffix == ".md"

    def write_file(self, file_path: Path, data: str) -> None:
        document_path = (
            str(file_path)
            if self._is_correct_markdown_file(file_path)
            else f"{file_path}.md"
        )
        with open(document_path, "w", encoding="utf-8") as file:
            file.write(data)


class KnowLedgeManagerWriter(abc.ABC):
    @abc.abstractmethod
    def create_document(self) -> None:
        pass

    @abc.abstractmethod
    def export(self) -> None:
        pass


class ObsidianDocument(MarkdownWriter):
    def __init__(self, vault_path: Path) -> None:
        self.vault_path = vault_path

    def format_document(self, remarkable_document: Document) -> str:
        obsidian_document_content = ""
        document_highlights = remarkable_document.document_highlights.page_highlights
        for page_highlights in document_highlights:
            obsidian_document_content += self._add_header_3(
                str(page_highlights.raw_file.file_path)
            )
            obsidian_document_content += self._add_page_quotes(
                page_highlights.highlights
            )
        return obsidian_document_content

    def _add_header_1(self, text: str) -> str:
        title = f"\n# {text}\n"
        return title

    def _add_header_2(self, text: str) -> str:
        title = f"\n## {text}\n"
        return title

    def _add_header_3(self, text: str) -> str:
        title = f"\n### {text}\n"
        return title

    def _add_metadata(self, current_date: str) -> str:
        metadata = f"\n> Timestamp: {current_date}\n> Status:\n> Tags:\n"
        return metadata

    def _add_page_quotes(self, page_quotes: list[str]) -> str:
        formatted_quote = "\n```ad-quote\n"
        for quote in page_quotes:
            formatted_quote += f"{quote}\n"
        formatted_quote = f"{formatted_quote}```"
        return formatted_quote

    def export(self, document_name: str, content: str) -> None:
        self.write_file(self.vault_path / document_name, content)
