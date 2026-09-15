import shutil
import subprocess
import tempfile
from pathlib import Path

from app.extractors.base import LanguageExtractor


NON_SOURCE_DIR_NAMES = {
    "tests",
    "test",
    "docs",
    "doc",
    "examples",
    "example",
    "scripts",
    "build",
    "dist",
    "venv",
    ".venv",
    "node_modules",
}


def _packages_in(directory: Path) -> list[str]:
    return [
        p.name
        for p in directory.iterdir()
        if p.is_dir() and p.name not in NON_SOURCE_DIR_NAMES and (p / "__init__.py").exists()
    ]


def _discover_targets(repo_path: Path) -> list[str]:
    """Find what to point pyreverse at: a src/ layout, else top-level packages, else loose .py files."""
    src_dir = repo_path / "src"
    if src_dir.is_dir():
        src_packages = _packages_in(src_dir)
        if src_packages:
            return src_packages

    packages = _packages_in(repo_path)
    if packages:
        return packages

    top_level_files = [p.name for p in repo_path.glob("*.py")]
    return top_level_files


class PythonExtractor(LanguageExtractor):
    language = "Python"

    def extract(self, repo_path: Path) -> str:
        pyreverse_bin = shutil.which("pyreverse")
        if pyreverse_bin is None:
            raise RuntimeError("pyreverse binary not found on PATH (install pylint)")

        targets = _discover_targets(repo_path)
        if not targets:
            raise ValueError("No Python packages or modules found to analyze")

        search_root = repo_path
        if (repo_path / "src").is_dir() and all(
            (repo_path / "src" / t / "__init__.py").exists() for t in targets
        ):
            search_root = repo_path / "src"

        with tempfile.TemporaryDirectory() as out_dir:
            result = subprocess.run(
                [pyreverse_bin, "-o", "mmd", "-p", "repo", "-d", out_dir, *targets],
                cwd=search_root,
                capture_output=True,
                text=True,
                timeout=60,
            )
            classes_file = Path(out_dir) / "classes_repo.mmd"
            if not classes_file.exists():
                raise RuntimeError(f"pyreverse produced no diagram: {result.stderr.strip()}")

            diagram = classes_file.read_text()

        if diagram.strip() == "classDiagram":
            raise ValueError("No classes found in this repo's Python code")

        return diagram
