class NoHighlightsFoundsForDocumentException(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class FieldsNotDefinedInFile(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
