
from pathlib import Path
from datetime import datetime
import hashlib
import csv
import sys


# Calculate SHA-256 hash
def calculate_hash(file):
    sha256 = hashlib.sha256()

    with open(file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            sha256.update(chunk)

    return sha256.hexdigest()


# Load known hashes from CSV
def load_reference(filename):
    known_hashes = set()

    with open(filename, "r", newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)

        if not reader.fieldnames:
            raise ValueError("Reference CSV is empty")

        hash_column = next(
            (name for name in reader.fieldnames
             if name.strip().lower() in ("sha256", "sha256_hash", "hash")),
            None
        )

        if hash_column is None:
            raise ValueError("No SHA-256 column found in CSV")

        for row in reader:
            value = (row.get(hash_column) or "").strip().lower()

            if len(value) == 64 and all(
                c in "0123456789abcdef" for c in value
            ):
                known_hashes.add(value)
            elif value:
                print("Warning: Invalid reference hash skipped")

    return known_hashes


# Save results to CSV
def save_report(results, filename):
    if not results:
        print("No results to save.")
        return

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=results[0].keys()
        )
        writer.writeheader()
        writer.writerows(results)

    print("\nReport saved:", filename)


# Main program
def main():
    project_folder = Path(__file__).resolve().parent
    reference_file = project_folder / "hashes_reference.csv"

    # Select folder to analyse
    if len(sys.argv) > 1:
        folder = Path(sys.argv[1]).expanduser().resolve()
    else:
        folder = project_folder

    print("File Triage Project")
    print("-------------------")
    print("Analysing folder:", folder)

    # Check folder
    if not folder.is_dir():
        print("Error: Folder does not exist:", folder)
        return

    # Load reference hashes
    try:
        known_hashes = load_reference(reference_file)
    except (OSError, ValueError, csv.Error) as error:
        print("Error loading reference file:", error)
        return

    print("Reference hashes loaded:", len(known_hashes))

    duplicates = {}
    results = []

    # Read files
    try:
        files = sorted(folder.iterdir())
    except OSError as error:
        print("Error opening folder:", error)
        return

    for file in files:
        try:
            if not file.is_file():
                continue

            if file.suffix.lower() not in [".txt", ".bin"]:
                continue

            if file.name.lower() == "readme.txt":
                continue

            # Calculate SHA-256
            file_hash = calculate_hash(file)

            # Get file information
            file_info = file.stat()
            file_size = file_info.st_size
            file_extension = file.suffix

            modified_date = datetime.fromtimestamp(
                file_info.st_mtime
            ).strftime("%Y-%m-%d %H:%M:%S")

            # Classify file
            if file_hash in known_hashes:
                status = "KNOWN"
            else:
                status = "UNKNOWN"

            # Store duplicate information
            if file_hash not in duplicates:
                duplicates[file_hash] = []

            duplicates[file_hash].append(file.name)

            # Store results
            results.append({
                "Filename": file.name,
                "Extension": file_extension,
                "Size (bytes)": file_size,
                "Last Modified": modified_date,
                "SHA-256": file_hash,
                "Status": status
            })

            # Display results
            print("\nFile:", file.name)
            print("Extension:", file_extension)
            print("Size:", file_size, "bytes")
            print("Last Modified:", modified_date)
            print("SHA-256:", file_hash)
            print("Status:", status)

        except (OSError, ValueError) as error:
            print("Error reading", file.name, ":", error)

    # Duplicate summary
    print("\n--- Duplicate File Summary ---")

    duplicate_groups = 0

    for file_hash, filenames in duplicates.items():
        if len(filenames) > 1:
            duplicate_groups += 1
            print("Duplicate files:", ", ".join(filenames))

    if duplicate_groups == 0:
        print("No duplicate files found.")
    else:
        print("Duplicate groups found:", duplicate_groups)

    # Investigation summary
    known_count = sum(
        1 for result in results
        if result["Status"] == "KNOWN"
    )

    unknown_count = sum(
        1 for result in results
        if result["Status"] == "UNKNOWN"
    )

    print("\n--- Investigation Summary ---")
    print("Total files analysed:", len(results))
    print("Known files:", known_count)
    print("Unknown files:", unknown_count)
    print("Duplicate groups:", duplicate_groups)

    # Save report in the project folder
    report_file = project_folder / "triage_report.csv"

    try:
        save_report(results, report_file)
    except (OSError, csv.Error) as error:
        print("Error saving report:", error)


if __name__ == "__main__":
    main()
