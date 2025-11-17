#!/usr/bin/env python3
import os
import struct
import threading
import concurrent.futures
from pathlib import Path
from queue import Queue

# ---------------------------------------------------------------
# MAGIC MAP (expanded)
# ---------------------------------------------------------------
MAGIC_MAP = {
    b"\xFF\xD8\xFF": "jpg",
    b"\x89PNG": "png",
    b"GIF87a": "gif",
    b"GIF89a": "gif",
    b"BM": "bmp",
    b"\x00\x00\x01\x00": "ico",
    b"II*\x00": "tif",
    b"MM\x00*": "tif",
    b"IIRO": "cr2",
    b"\x49\x49\xBC": "rw2",
    b"FUJIFILMCCD": "raf",
    b"\x00\x00\x00\x0CjP  ": "jp2",

    b"ID3": "mp3",
    b"\xFF\xF1": "aac",
    b"\xFF\xF9": "aac",
    b"fLaC": "flac",
    b"OggS": "ogg",
    b"RIFF": "riff",
    b"\x4D\x54\x68\x64": "mid",

    b"\x1A\x45\xDF\xA3": "mkv",
    b"\x00\x00\x01\xBA": "mpg",
    b"\x00\x00\x01\xB3": "mpg",

    b"%PDF": "pdf",
    b"{\\rtf": "rtf",
    b"D0CF11E0": "ole",
    b"PK\x03\x04": "zip",

    b"\x1F\x8B\x08": "gz",
    b"BZh": "bz2",
    b"7z\xBC\xAF'\x1C": "7z",
    b"Rar!\x1A\x07\x00": "rar",
    b"Rar!\x1A\x07\x01\x00": "rar",

    b"CD001": "iso",
    b"ITSF": "chm",

    b"OTTO": "otf",
    b"\x00\x01\x00\x00": "ttf",
    b"wOFF": "woff",
    b"wOF2": "woff2",
}

# ---------------------------------------------------------------
# BRAND MAP – MP4, MOV, HEIC, HEIF, AVIF, etc.
# ---------------------------------------------------------------
BRAND_MAP = {
    b"isom": "mp4",
    b"iso2": "mp4",
    b"iso3": "mp4",
    b"avc1": "mp4",
    b"mp41": "mp4",
    b"mp42": "mp4",
    b"MSNV": "mp4",
    b"mmp4": "mp4",
    b"dash": "mp4",

    b"qt  ": "mov",
    b"moov": "mov",

    b"M4V ": "m4v",
    b"M4A ": "m4a",
    b"f4v ": "f4v",
    b"f4a ": "f4a",

    b"heic": "heic",
    b"heix": "heic",
    b"hevc": "heic",
    b"hevx": "heic",
    b"mif1": "heif",
    b"msf1": "heif",

    b"avif": "avif",
    b"avis": "avif",
}

# ---------------------------------------------------------------
# Read signatures
# ---------------------------------------------------------------

def detect_by_magic(data):
    for magic, ext in MAGIC_MAP.items():
        if data.startswith(magic):
            return ext
    return None


def detect_by_brand(data):
    # ISO BMFF starts with: size(4) + 'ftyp' + brand(4)
    if len(data) < 12:
        return None
    if data[4:8] != b"ftyp":
        return None
    brand = data[8:12]
    return BRAND_MAP.get(brand, None)

# ---------------------------------------------------------------
# Worker function
# ---------------------------------------------------------------

def process_file(path: Path):
    try:
        with open(path, "rb") as f:
            header = f.read(64)
    except:
        return None

    ext = detect_by_magic(header)
    if not ext:
        ext = detect_by_brand(header)

    if not ext:
        return None

    new_name = f"{path.stem}.{ext}"
    new_path = path.with_name(new_name)

    if path != new_path:
        try:
            os.rename(path, new_path)
            return (str(path), str(new_path))
        except:
            return None

    return None

# ---------------------------------------------------------------
# Recursive scanning + ThreadPool
# ---------------------------------------------------------------

def walk_all_files(root: Path):
    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            yield Path(dirpath) / filename

# ---------------------------------------------------------------
# Main
# ---------------------------------------------------------------

def main():
    root = Path(os.getcwd())
    log_path = root / "File Rename Log.txt"

    files = list(walk_all_files(root))
    total = len(files)
    remaining = total

    print(f"Total files: {total}")

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        futures = {executor.submit(process_file, f): f for f in files}

        with open(log_path, "a", encoding="utf-8") as log:
            for future in concurrent.futures.as_completed(futures):
                remaining -= 1
                result = future.result()
                if result:
                    old, new = result
                    log.write(f"RENAMED: {old} -> {new}\n")

                print(f"Remaining: {remaining}", end="\r")

    print("\nDone.")


if __name__ == "__main__":
    main()

