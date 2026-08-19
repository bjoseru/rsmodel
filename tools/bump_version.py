#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Bump the version everywhere it is written down, in one shot.

    uv run tools/bump_version.py 0.1.1          # edit the files
    uv run tools/bump_version.py 0.1.1 --tag    # ...and make the annotated tag

`rsmodel/rsmodel/__init__.py` is the single source of truth that hatchling reads;
CITATION.cff and CHANGELOG.md have to agree with it, and release.yml refuses to
publish when the git tag does not. Keeping the four in step by hand is exactly
the sort of thing that fails at 23:00 before a submission deadline.
"""

from __future__ import annotations

import argparse
import datetime
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INIT = ROOT / "rsmodel" / "rsmodel" / "__init__.py"
CFF = ROOT / "CITATION.cff"
CHANGELOG = ROOT / "CHANGELOG.md"

SEMVER = re.compile(r"^\d+\.\d+\.\d+([-+].+)?$")


def fail(msg: str) -> None:
    sys.exit(f"error: {msg}")


def current() -> str:
    m = re.search(r'^__version__ = "(.+?)"$', INIT.read_text(encoding="utf-8"), re.M)
    if not m:
        fail(f"no __version__ in {INIT}")
    return m.group(1)


def as_tuple(v: str) -> tuple[int, ...]:
    return tuple(int(p) for p in v.split("-")[0].split("+")[0].split("."))


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("version", help="new version, e.g. 0.1.1")
    p.add_argument("--tag", action="store_true", help="also create the annotated git tag")
    p.add_argument("--date", help="release date, ISO (default: today)")
    args = p.parse_args()

    new = args.version.lstrip("v")
    if not SEMVER.match(new):
        fail(f"{new!r} is not a semantic version")

    old = current()
    if as_tuple(new) <= as_tuple(old):
        fail(f"{new} does not come after the current {old} — PyPI uploads are immutable")

    date = args.date or datetime.date.today().isoformat()

    # 1. the source of truth
    t = INIT.read_text(encoding="utf-8")
    INIT.write_text(
        re.sub(r'^__version__ = ".+?"$', f'__version__ = "{new}"', t, count=1, flags=re.M),
        encoding="utf-8",
    )

    # 2. citation metadata
    t = CFF.read_text(encoding="utf-8")
    t = re.sub(r"^version: .+$", f"version: {new}", t, count=1, flags=re.M)
    t = re.sub(r'^date-released: .+$', f'date-released: "{date}"', t, count=1, flags=re.M)
    CFF.write_text(t, encoding="utf-8")

    # 3. changelog: open a new section, leave Unreleased empty, fix the link refs
    t = CHANGELOG.read_text(encoding="utf-8")
    if f"## [{new}]" in t:
        fail(f"CHANGELOG.md already has a section for {new}")
    t = t.replace(
        "## [Unreleased]\n",
        f"## [Unreleased]\n\n## [{new}] — {date}\n\n### Changed\n\n- _describe this release_\n",
        1,
    )
    t = t.replace(
        f"[Unreleased]: https://github.com/bjoseru/rsmodel/compare/v{old}...HEAD",
        f"[Unreleased]: https://github.com/bjoseru/rsmodel/compare/v{new}...HEAD\n"
        f"[{new}]: https://github.com/bjoseru/rsmodel/compare/v{old}...v{new}",
    )
    CHANGELOG.write_text(t, encoding="utf-8")

    print(f"{old} -> {new}")
    for f in (INIT, CFF, CHANGELOG):
        print(f"  {f.relative_to(ROOT)}")
    print("\nwrite the changelog entry, then:")
    print(f"  git commit -am 'release {new}'")
    print(f"  git tag -a v{new} -m 'rsmodel {new}'" if not args.tag else "")
    print(f"  git push origin main v{new}")

    if args.tag:
        subprocess.run(["git", "tag", "-a", f"v{new}", "-m", f"rsmodel {new}"], check=True)
        print(f"\ntagged v{new} (commit first if you had not — the tag points at HEAD)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
