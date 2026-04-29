# Wabbajack-corrupt-files-checker
A fast, parallel Python tool to verify the integrity of large modpack archives (ZIP, RAR, 7Z) especially useful for Wabbajack downloads.


Why This Exists
When downloading large modpacks via Wabbajack, some archives may become corrupted or incomplete.
Wabbajack detects them one by one, which can be slow and inefficient.

This tool speeds up the process by:

Scanning all archives in a folder
Testing them using zips
Running checks in parallel (multi-threaded)
Generating a clear report of valid vs corrupt files

Features
-Supports .zip, .rar, .7z
-Multi-threaded (parallel processing)
-Uses 7z t (no extraction, fast validation)
-Detects:
--CRC errors
--Data corruption
--Broken/incomplete archives
-CSV report output
-Handles large modpacks efficiently
-Performance

Default: 6 parallel workers.
Recommended tuning:
SSD/NVMe → 6
HDD → 3–4
📂 Usage

Install 7-Zip,WinRAR
Update the folder path in the script:
DOWNLOADS_DIR = Path(r"Modpack\downloads")
Run:
python script.py
📄 Output

A CSV report is generated:

archive_check_report.csv
File	Status	Message
file1.zip	OK	Valid
file2.rar	CORRUPT	CRC failed
file3.7z	ERROR	Unexpected issue
