# FIXIT – File Identification & eXtension Inference Tool

`fixit` is a high-accuracy, signature-based file repair utility. It recursively scans folders, detects file types using magic bytes and ISO BMFF brands, and corrects missing or incorrect extensions at scale.

Runs on Windows 11 (and any OS with Python 3). No dependencies.

---

## Features

* Signature-based detection (magic bytes + ISO BMFF brands)
* Corrects:

  * Wrong extensions
  * Missing extensions
  * `.0` placeholder extensions
* Supports images, videos, audio, documents, RAW formats, archives, fonts, and more
* Fully recursive directory scanning
* Multithreaded for high performance
* Writes all changes to `renamer_log.txt`
* Safe: renames only when detection is unambiguous
* Pure Python, zero external libraries

---

## Supported File Types

### Images

JPG, PNG, GIF, BMP, TIFF, ICO, JP2, HEIC, HEIF, AVIF, CR2, RW2, RAF, WebP

### Video

MP4, MOV, M4V, MKV, WebM, AVI, MPEG/MPG, F4V

### Audio

MP3, AAC, FLAC, OGG, WAV (RIFF), MIDI

### Documents

PDF, RTF, DOC/XLS/PPT (OLE), DOCX/XLSX/PPTX (ZIP), EPUB

### Archives

ZIP, RAR/RAR5, 7z, GZ, BZ2, ISO

### Fonts

TTF, OTF, WOFF, WOFF2

(Detection is driven by clear, deterministic signatures to avoid false positives.)

---

## Usage

Place `fixit.py` in the directory you want to process, or run it from any path.

### Command Line

```sh
python fixit.py
```

The script will:

1. Scan the current folder and all subdirectories
2. Detect each file’s real type via header analysis
3. Rename with the correct extension
4. Log every change to `renamer_log.txt`

---

## How It Works

FIXIT reads the first 64 bytes of each file and:

1. Attempts a magic-byte match (fast, deterministic)
2. If no match, attempts ISO BMFF brand detection (for MP4/HEIC/HEIF/AVIF)
3. Renames the file safely
4. Uses an 8-thread executor for parallel processing
5. Avoids ambiguous or risky matches

---

## Logging

All rename operations are appended to:

```
renamer_log.txt
```

Format:

```
RENAMED: <old_path> -> <new_path>
```

---

## Why FIXIT Exists

Bulk exports (forensic extractions, NAS dumps, large media libraries, mixed-device datasets) often contain files with:

* missing extensions
* incorrect or misleading extensions
* placeholder `.0` extensions
* mixed, unlabelled formats

FIXIT solves this by trusting **file content**, not filenames.

---

## License

MIT License.

---

## Project Name Meaning

**FIXIT** — *File Identification & eXtension Inference Tool*.

Short, memorable, and fast to type on the command line.
