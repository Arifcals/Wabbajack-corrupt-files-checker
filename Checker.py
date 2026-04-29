import os
import csv
import subprocess
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

DOWNLOADS_DIR = Path(r"modpack\downloads")     # Paste the modpack file path here

REPORT_FILE = DOWNLOADS_DIR / "check_report.csv"

MAX_WORKERS = 6 #if you have a hdd change this 2 or 3

SEVEN_ZIP_PATHS = [
    r"C:\Program Files\7-Zip\7z.exe",
    r"C:\Program Files (x86)\7-Zip\7z.exe"
]

ARCHIVE_EXTENSIONS = {
    ".zip",
    ".rar",
    ".7z"
}


def find_7zip():
    for path in SEVEN_ZIP_PATHS:
        if os.path.exists(path):
            return path
    raise Exception("7-Zip cannot find!")


def is_archive(file: Path):
    name = file.name.lower()

    if file.suffix.lower() in ARCHIVE_EXTENSIONS:
        return True

    if name.endswith(".part1.rar") or ".part" in name:
        return True

    return False


def test_archive(seven_zip, archive_path: Path):
    try:
        result = subprocess.run(
            [seven_zip, "t", str(archive_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            encoding="utf-8",
            errors="replace"
        )

        output = (result.stdout + result.stderr).lower()

        if result.returncode == 0:
            return (archive_path, "OK", "Valid")

        corrupt_keywords = [
            "data error",
            "crc failed",
            "headers error",
            "unexpected end",
            "can not open",
            "is not archive",
            "errors"
            "corrupt"
        ]

        if any(k in output for k in corrupt_keywords):
            return (archive_path, "CORRUPT", output[:500])

        return (archive_path, "ERROR", output[:500])

    except Exception as e:
        return (archive_path, "ERROR", str(e))


def main():
    seven_zip = find_7zip()

    archives = [
        f for f in DOWNLOADS_DIR.rglob("*")
        if f.is_file() and is_archive(f)
    ]

    print(f"Total Archive: {len(archives)}")
    print(f"{MAX_WORKERS} Starting with parallel processing...\n")

    results = []

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(test_archive, seven_zip, archive): archive
            for archive in archives
        }

        for i, future in enumerate(as_completed(futures), 1):
            archive, status, message = future.result()

            print(f"[{i}/{len(archives)}] {status} → {archive.name}")

            results.append((str(archive), status, message))

    with open(REPORT_FILE, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(["File", "Status", "Message"])
        writer.writerows(results)

    print("\n✅ Finish")
    print(f"📄 Report: {REPORT_FILE}")


if __name__ == "__main__":
    main()
