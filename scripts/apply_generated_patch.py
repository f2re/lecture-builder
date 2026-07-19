#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import io
import json
import os
import tarfile
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
PATCH_DIR = ROOT / ".patch"
MANIFEST_PATH = PATCH_DIR / "manifest.json"


def safe_relative(name: str) -> str:
    value = PurePosixPath(name)
    if value.is_absolute() or not value.parts or any(part in {"", ".", ".."} for part in value.parts):
        raise ValueError(f"unsafe archive path: {name!r}")
    return value.as_posix()


def main() -> int:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    expected_files = [safe_relative(str(item)) for item in manifest["files"]]
    if len(expected_files) != len(set(expected_files)):
        raise ValueError("manifest contains duplicate paths")

    chunk_paths = sorted(PATCH_DIR.glob("chunk-*.b64"))
    if len(chunk_paths) != int(manifest["chunks"]):
        raise ValueError(f"expected {manifest['chunks']} chunks, found {len(chunk_paths)}")
    encoded = b"".join(path.read_bytes() for path in chunk_paths)
    archive = base64.b64decode(encoded, validate=False)
    if len(archive) != int(manifest["archive_bytes"]):
        raise ValueError("archive size does not match manifest")
    digest = hashlib.sha256(archive).hexdigest()
    if digest != manifest["sha256"]:
        raise ValueError(f"archive hash mismatch: {digest}")

    with tarfile.open(fileobj=io.BytesIO(archive), mode="r:gz") as bundle:
        members = bundle.getmembers()
        actual_files: list[str] = []
        for member in members:
            path = safe_relative(member.name)
            if member.isdir():
                continue
            if not member.isfile():
                raise ValueError(f"only regular files are allowed: {path}")
            actual_files.append(path)
        if sorted(actual_files) != sorted(expected_files):
            missing = sorted(set(expected_files) - set(actual_files))
            unexpected = sorted(set(actual_files) - set(expected_files))
            raise ValueError(f"archive file set mismatch; missing={missing}, unexpected={unexpected}")

        for member in members:
            if not member.isfile():
                continue
            relative = safe_relative(member.name)
            target = ROOT / relative
            try:
                target.resolve().relative_to(ROOT.resolve())
            except ValueError as exc:
                raise ValueError(f"path escapes repository: {relative}") from exc
            source = bundle.extractfile(member)
            if source is None:
                raise ValueError(f"unable to read archive member: {relative}")
            payload = source.read()
            target.parent.mkdir(parents=True, exist_ok=True)
            temporary = target.with_name(f".{target.name}.generated-patch.tmp")
            temporary.write_bytes(payload)
            os.chmod(temporary, member.mode & 0o777 or 0o644)
            os.replace(temporary, target)

    print(f"Applied {len(expected_files)} verified files from generated patch")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
