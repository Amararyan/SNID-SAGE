## Batch Import Templates

Use the Manage Templates tab and click "Batch Import…" to create many templates at once.

Input file: CSV/TSV with columns (case-insensitive):
- object_name, spectrum_file_path, age, redshift, type, subtype, sim_flag

Notes:
- Relative paths are resolved relative to the CSV file location.
- Multiple rows with the same object_name create a single multi-epoch template.
- Choose a destination templates folder or use your configured User Templates folder.
- An error report file is written next to the CSV if any rows fail.


