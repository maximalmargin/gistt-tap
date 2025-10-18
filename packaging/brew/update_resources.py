#!/usr/bin/env python3
"""
Fetch PyPI metadata for dependencies and emit Homebrew resource blocks.

Usage:
  python packaging/brew/update_resources.py > /tmp/resources.rb

For packages that need source distributions (e.g. to avoid arch-specific wheels),
add their canonicalised names to `PREFER_SDIST`.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import textwrap
import urllib.request
from pathlib import Path
from typing import Iterable

PREFER_SDIST = {"pydantic-core", "websockets"}


def parse_requirements(path: Path) -> list[tuple[str, str]]:
    pairs: list[tuple[str, str]] = []
    for raw_line in path.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "==" not in line:
            raise ValueError(f"Unsupported requirement format: {raw_line!r}")
        name, version = line.split("==", 1)
        pairs.append((name.strip(), version.strip()))
    return pairs


def normalize_name(name: str) -> str:
    return re.sub(r"[-_.]+", "-", name).lower()


def load_release(name: str, version: str) -> dict:
    url = f"https://pypi.org/pypi/{name}/{version}/json"
    with urllib.request.urlopen(url, timeout=30) as resp:  # nosec B310
        return json.load(resp)


def choose_url(name: str, version: str, entries: Iterable[dict]) -> dict:
    canonical = normalize_name(name)
    prefer_sdist = canonical in PREFER_SDIST
    candidates = list(entries)
    if not candidates:
        raise RuntimeError(f"No releases listed for {name}=={version}")

    for entry in candidates:
        if entry.get("packagetype") == "sdist":
            return entry

    for entry in candidates:
        filename = entry.get("filename", "")
        if filename.endswith("py3-none-any.whl"):
            return entry

    for entry in candidates:
        if entry.get("packagetype") == "bdist_wheel":
            return entry

    return candidates[0]


def emit_resources(requirements: Path) -> str:
    blocks: list[str] = []
    for raw_name, version in parse_requirements(requirements):
        canonical = normalize_name(raw_name)
        release = load_release(raw_name, version)
        url_entry = choose_url(raw_name, version, release.get("urls", ()))
        url = url_entry["url"]
        sha256 = url_entry["digests"]["sha256"]
        block = textwrap.dedent(
            f"""
            resource "{canonical}" do
              url "{url}"
              sha256 "{sha256}"
            end
            """
        ).strip()
        blocks.append(block)
    return "\n\n".join(blocks) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--requirements",
        type=Path,
        default=Path("packaging/brew/requirements.lock"),
        help="Path to the pinned requirements file.",
    )
    args = parser.parse_args()

    try:
        sys.stdout.write(emit_resources(args.requirements))
    except Exception as exc:  # noqa: BLE001
        print(f"error: {exc}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
