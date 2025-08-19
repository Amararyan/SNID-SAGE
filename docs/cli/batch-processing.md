# Batch Processing

Efficiently process many spectra with the CLI `batch` command.

## Command

```powershell
# Process multiple spectra; write outputs under results/
sage batch "data/*.dat" templates/ --output-dir results/
```

## Modes

- Default: main outputs per spectrum plus a summary
- `--minimal`: summary only (fastest, least disk)
- `--complete`: full outputs and plots (largest disk)

## Common options

```powershell
# Redshift search range
sage batch "data/*.dat" templates/ --zmin 0.0 --zmax 0.5 --output-dir results/

# Force a fixed redshift for all spectra
sage batch "data/*.dat" templates/ --forced-redshift 0.023 --output-dir results/

# Restrict to specific types
sage batch "data/*.dat" templates/ --type-filter Ia Ib Ic --output-dir results/

# Stop on first error; increase verbosity
sage batch "data/*.dat" templates/ --stop-on-error --verbose --output-dir results/
```

## Output structure (default)

- Per spectrum: `.output`, `.fluxed`, `.flattened`
- Summary: `batch_summary.txt` in the output directory

With `--complete`, additional plots are generated (comparison, clustering, redshift–age, subtype proportions).

## Tips

- Start with a small subset to validate parameters
- Use `--type-filter` to reduce runtime on large template sets
- Prefer `--minimal` for quick surveys; rerun interesting cases with `--complete`

## Troubleshooting

- “Templates not found”: pass the templates directory explicitly or set it via `sage config set templates.default_dir ...`
- “Out of memory” on large batches: narrow the type range or run in smaller batches

## See also

- [Command Reference](command-reference.md)
- [Template Management](../gui/templates-manager.md)

