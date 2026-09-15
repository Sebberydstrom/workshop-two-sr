import os
import re
import shutil
import subprocess
import tempfile
import urllib.error
import urllib.request
from contextlib import contextmanager
from pathlib import Path

GITHUB_URL_RE = re.compile(
    r"^https?://github\.com/(?P<owner>[\w.-]+)/(?P<repo>[\w.-]+?)(\.git)?/?$"
)


class RepoNotFoundError(Exception):
    """Raised when a repo URL parses fine but GitHub has no public repo at that path."""


def parse_github_url(url: str) -> tuple[str, str]:
    match = GITHUB_URL_RE.match(url.strip())
    if not match:
        raise ValueError(f"Not a valid GitHub repo URL: {url}")
    return match.group("owner"), match.group("repo")


def _check_repo_exists(owner: str, repo: str) -> None:
    api_url = f"https://api.github.com/repos/{owner}/{repo}"
    request = urllib.request.Request(api_url, headers={"Accept": "application/vnd.github+json"})
    try:
        urllib.request.urlopen(request, timeout=10)
    except urllib.error.HTTPError as exc:
        if exc.code == 404:
            raise RepoNotFoundError(f"No public repo found at {owner}/{repo}") from exc
        raise RuntimeError(f"GitHub API error checking {owner}/{repo}: HTTP {exc.code}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(f"Could not reach GitHub API: {exc.reason}") from exc


@contextmanager
def clone_repo(url: str):
    owner, repo = parse_github_url(url)
    _check_repo_exists(owner, repo)

    clone_url = f"https://github.com/{owner}/{repo}.git"
    tmp_dir = tempfile.mkdtemp(prefix="repo-visualizer-")
    try:
        result = subprocess.run(
            [
                "git",
                "-c",
                "credential.helper=",
                "clone",
                "--depth",
                "1",
                clone_url,
                tmp_dir,
            ],
            capture_output=True,
            text=True,
            timeout=60,
            env={**os.environ, "GIT_TERMINAL_PROMPT": "0"},
        )
        if result.returncode != 0:
            raise RuntimeError(f"Could not fetch repo {owner}/{repo}: clone failed")
        yield Path(tmp_dir)
    finally:
        shutil.rmtree(tmp_dir, ignore_errors=True)
