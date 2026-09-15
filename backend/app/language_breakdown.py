import json
import shutil
import subprocess
from pathlib import Path


def get_language_breakdown(repo_path: Path) -> list[dict]:
    scc_bin = shutil.which("scc")
    if scc_bin is None:
        raise RuntimeError("scc binary not found on PATH")

    result = subprocess.run(
        [scc_bin, "--format", "json", str(repo_path)],
        capture_output=True,
        text=True,
        timeout=60,
    )
    if result.returncode != 0:
        raise RuntimeError(f"scc failed: {result.stderr.strip()}")

    raw = json.loads(result.stdout)
    breakdown = [
        {
            "language": entry["Name"],
            "files": entry["Count"],
            "lines": entry["Code"],
        }
        for entry in raw
    ]
    breakdown.sort(key=lambda e: e["lines"], reverse=True)
    return breakdown
