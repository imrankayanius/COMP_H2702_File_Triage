# COMP H2702 – Scenario C: File Triage and Hash Analysis

## Project Description

This Python program analyses files to help identify known, unknown and duplicate files using SHA-256 hashes.

## Features

- Scans `.txt` and `.bin` files in a selected folder.
- Calculates SHA-256 hashes.
- Compares hashes against `hashes_reference.csv`.
- Classifies files as KNOWN or UNKNOWN.
- Detects duplicate files using matching hashes.
- Displays file sizes, extensions and last-modified dates.
- Saves investigation results to `triage_report.csv`.
- Handles common file and folder errors.

## Requirements

- Python 3
- No additional Python packages required.

## How to Run

Open a terminal in the project folder.

To analyse the sample files:

```text
python file_triage.py
```

To analyse a different folder:

```text
python file_triage.py "test_samples"
```

## Example Results

The supplied sample files produced:

- Total files analysed: 5
- Known files: 3
- Unknown files: 2
- Duplicate groups: 1

`sample_a.txt` and `sample_b.txt` were identified as duplicates because they have identical SHA-256 hashes.

## Output

The program creates `triage_report.csv`, containing the filename, extension, size, last-modified date, SHA-256 hash and classification for each analysed file.

The CSV report is saved in the project folder and overwritten on each successful run that produces results.

## Limitations

The program only scans `.txt` and `.bin` files in the selected folder. It does not scan subfolders.

A file marked UNKNOWN is not necessarily malicious. It only means its hash was not found in the reference CSV.

## Testing

The program was tested using:

1. The original five sample files.
2. An invalid folder path.
3. A separate folder containing two sample files.
4. An empty folder containing no files.
5. A missing reference CSV file.
6. A reference CSV with an invalid header.
7. File-reading error handling was checked in the code.
8. The original sample files were restored and tested again.

The tests produced the expected results.