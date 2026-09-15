from app.extractors.base import LanguageExtractor
from app.extractors.python_extractor import PythonExtractor

EXTRACTORS: dict[str, LanguageExtractor] = {
    extractor.language: extractor for extractor in [PythonExtractor()]
}


def get_extractor(primary_language: str) -> LanguageExtractor | None:
    return EXTRACTORS.get(primary_language)
