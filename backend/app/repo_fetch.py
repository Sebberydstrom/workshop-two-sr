import re
import shutil
import subprocess
import tempfile
from contextlib import contextmanager
from pathlib import Path

GITHUB_URL_RE = re.compile(
    r"^https?://github\.com/(?P<owner>[\w.-]+)/(?P<repo>[\w.-]+?)(\.git)?/?$"
)


def parse_github_url(url: str) -> tuple[str, str]:
    match = GITHUB_URL_RE.match(url.strip())
    if not match:
        raise ValueError(f"Not a valid GitHub repo URL: {url}")
    return match.group("owner"), match.group("repo")


@contextmanager
def clone_repo(url: str):
    owner, repo = parse_github_url(url)
    clone_url = f"https://github.com/{owner}/{repo}.git"
    tmp_dir = tempfile.mkdtemp(prefix="repo-visualizer-")
    try:
        result = subprocess.run(
            ["git", "clone", "--depth", "1", clone_url, tmp_dir],
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode != 0:
            raise ValueError(f"Could not clone repo {owner}/{repo}: {result.stderr.strip()}")
        yield Path(tmp_dir)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
