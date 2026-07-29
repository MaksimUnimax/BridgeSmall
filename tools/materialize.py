#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import tarfile
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "artifacts" / "MANIFEST.json").read_text(encoding="utf-8"))


def decode(name: str, target: Path) -> Path:
    info = MANIFEST[name]
    parts = sorted((ROOT / "artifacts" / name).glob("*.part"))
    if len(parts) != int(info["parts"]):
        raise SystemExit(f'{name}: expected {info["parts"]} parts, found {len(parts)}')
    encoded = "".join(part.read_text(encoding="ascii").strip() for part in parts)
    data = base64.b64decode(encoded, validate=True)
    digest = hashlib.sha256(data).hexdigest()
    if digest != info["sha256"]:
        raise SystemExit(f"{name}: SHA-256 mismatch: {digest}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(data)
    print(f"{name}: wrote {target} ({len(data)} bytes, sha256={digest})")
    return target


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--extension", action="store_true")
    parser.add_argument("--server", action="store_true")
    parser.add_argument("--all", action="store_true")
    args = parser.parse_args()
    if not (args.extension or args.server or args.all):
        args.all = True

    if args.extension or args.all:
        info = MANIFEST["extension"]
        archive = decode("extension", ROOT / "extension" / "release" / info["output_name"])
        destination = ROOT / "extension" / "unpacked"
        destination.mkdir(parents=True, exist_ok=True)
        with zipfile.ZipFile(archive) as package:
            for member in package.infolist():
                path = (destination / member.filename).resolve()
                if not str(path).startswith(str(destination.resolve())):
                    raise SystemExit(f"unsafe ZIP member: {member.filename}")
            package.extractall(destination)
        print(f"extension: unpacked to {destination}")

    if args.server or args.all:
        info = MANIFEST["server"]
        archive = decode("server", ROOT / "artifacts" / info["output_name"])
        destination = ROOT / "server"
        with tarfile.open(archive, "r:gz") as package:
            base = destination.resolve()
            for member in package.getmembers():
                path = (destination / member.name).resolve()
                if not (path == base or str(path).startswith(str(base) + str(Path("/")))):
                    raise SystemExit(f"unsafe TAR member: {member.name}")
                if member.issym() or member.islnk():
                    raise SystemExit(f"link member rejected: {member.name}")
            package.extractall(destination)
        print(f"server: unpacked to {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
