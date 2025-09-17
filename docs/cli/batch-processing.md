# Batch Processing

Efficiently process many spectra with the CLI `batch` command.

## Command

```powershell
# Process multiple spectra; write outputs under results/
sage batch "data/*.dat" --output-dir results/
```

### List-based input (CSV)

```powershell
# Use a CSV listing spectra with optional per-row redshift
sage batch --list-csv "data/spectra_list.csv" --output-dir results/

# If your CSV uses different column names
sage batch --list-csv input.csv --path-column "Spectrum Path" --redshift-column "Host Redshift" --output-dir results/
```

Notes:
- The CSV must include a path column; redshift is optional.
- Relative paths in the CSV are resolved relative to the CSV file's directory.
- When a row has a redshift value, analysis is performed at that fixed redshift for that spectrum; otherwise the global search range is used.

## Modes

| Mode | Description |
|---|---|
| Default | Main outputs per spectrum plus a summary |
| `--minimal` | Summary only (fastest, least disk) |
| `--complete` | Full outputs and plots (largest disk) |

## Common options

| Option | Description |
|---|---|
| `--zmin FLOAT` / `--zmax FLOAT` | Redshift search range (default: -0.01 to 1.0) |
| `--forced-redshift FLOAT` | Force a fixed redshift for all spectra |
| `--type-filter TYPE...` | Restrict templates by type (e.g., Ia Ib Ic) |
| `--template-filter NAME...` | Only use specific templates by name |
| `--rlapmin FLOAT` / `--lapmin FLOAT` | Quality/overlap thresholds (defaults: 4.0 / 0.3) |
| `--rlap-ccc-threshold FLOAT` | Clustering quality threshold (default: 1.8) |
| `--output-dir DIR` | Output directory for results |
| `--stop-on-error` | Stop processing upon first error |
| `--verbose` | Verbose console output |
| `--brief` / `--full` | Toggle concise vs detailed console output |
| `--no-progress` | Disable progress output |

```powershell
# Redshift search range
sage batch "data/*.dat" --zmin 0.0 --zmax 0.5 --output-dir results/

# Force a fixed redshift for all spectra
sage batch "data/*.dat" --forced-redshift 0.023 --output-dir results/

# Force per-row redshift from a CSV list (only where present)
sage batch --list-csv "path/to/list.csv" --output-dir results/

# Restrict to specific types
sage batch "data/*.dat" --type-filter Ia Ib Ic --output-dir results/

# Stop on first error; increase verbosity
sage batch "data/*.dat" --stop-on-error --verbose --output-dir results/
```

## Output structure (default)

| Per spectrum | Summary |
|---|---|
| `.output`, `.fluxed`, `.flattened` | `batch_summary.txt` (includes a `zFixed` column) |

With `--complete`, additional plots are generated (comparison, clustering, redshift–age, subtype proportions).

## Tips

- Start with a small subset to validate parameters
- Use `--type-filter` to reduce runtime on large template sets
- Prefer `--minimal` for quick surveys; rerun interesting cases with `--complete`
 - When using CSV lists, keep spectrum paths relative to the CSV folder for portability

## Troubleshooting

- “Out of memory” on large batches: narrow the type range or run in smaller batches

## See also

- [Command Reference](command-reference.md)
- [Template Management](../gui/templates-manager.md)

