from abc import ABC, abstractmethod
from pathlib import Path


class LanguageExtractor(ABC):
    """Produces a class/module diagram (as Mermaid classDiagram syntax) for one language."""

    language: str

    @abstractmethod
    def extract(self, repo_path: Path) -> str:
        """Return Mermaid `classDiagram` source describing the repo's classes/relationships."""
        raise NotImplementedError
