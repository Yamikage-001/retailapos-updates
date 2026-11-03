#!/usr/bin/env python3
"""Publish signed installers and atomically advance the public update manifest."""

import argparse
import hashlib
import json
import shutil
import subprocess
import tempfile
from pathlib import Path

REPO = "Yamikage-001/retailapos-updates"
NAMES = {"android": "apk", "windows": "exe", "macos": "dmg"}


def run(*args: str) -> None:
    subprocess.run(args, check=True)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("version")
    parser.add_argument("build", type=int)
    parser.add_argument("--notes", required=True)
    for platform in NAMES:
        parser.add_argument(f"--{platform}", type=Path)
    options = parser.parse_args()
    if len(options.version.split(".")) != 3 or not all(
        part.isdigit() for part in options.version.split(".")
    ) or options.build < 1:
        parser.error("version must be major.minor.patch and build must be positive")

    assets = {platform: getattr(options, platform) for platform in NAMES
              if getattr(options, platform) is not None}
    if not assets:
        parser.error("supply at least one signed installer")
    for platform, path in assets.items():
        if not path.is_file() or path.suffix.lower() != f".{NAMES[platform]}":
            parser.error(f"{platform} must be an existing .{NAMES[platform]} file")

    current = json.loads(Path("latest.json").read_text())
    if (tuple(map(int, options.version.split("."))), options.build) <= (
        tuple(map(int, current["version"].split("."))), current["build"]
    ):
        parser.error("release must be newer than latest.json")

    tag = f"v{options.version}+{options.build}"
    with tempfile.TemporaryDirectory() as temporary:
        uploaded = []
        platforms = {}
        for platform, path in assets.items():
            name = f"RetailaPOS-{tag}-{platform}.{NAMES[platform]}"
            destination = Path(temporary) / name
            shutil.copy2(path, destination)
            digest = hashlib.file_digest(destination.open("rb"), "sha256").hexdigest()
            platforms[platform] = {
                "url": f"https://github.com/{REPO}/releases/download/{tag}/{name}",
                "sha256": digest,
            }
            uploaded.append(str(destination))
        run("gh", "release", "create", tag, *uploaded, "--repo", REPO,
            "--title", f"RetailaPOS {options.version}", "--notes", options.notes)

    manifest = {"version": options.version, "build": options.build,
                "notes": options.notes, "platforms": platforms}
    Path("latest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    run("git", "add", "latest.json")
    run("git", "commit", "-m", f"Publish {tag} update manifest")
    run("git", "push", "origin", "HEAD:main")


if __name__ == "__main__":
    main()
