# Template Management

SNID SAGE provides comprehensive template management capabilities for organizing and maintaining your supernova template library.

## Overview

Templates are the foundation of SNID SAGE's classification system. The template management commands help you:
- List and explore existing templates
- Add new templates to your library
- Create custom template libraries
- Manage template metadata and quality

### User overrides and merged index (HDF5)

- Base templates live under `snid_sage/templates/` with `template_index.json` and per-type files `templates_<Type>.hdf5`.
- User edits are stored under `snid_sage/templates/User_templates/`:
  - Per-type files: `templates_<Type>.user.hdf5`
  - User index: `template_index.user.json`
- Once a user file exists for a type, that type is loaded exclusively from the user file and base entries for the same type are ignored. The CLI and GUI both consume the merged index, avoiding duplicates.

## Commands

### list - List Templates

Display information about templates in your library.

#### Basic Usage
```bash
snid template list [TEMPLATE_DIR] [OPTIONS]
```

#### Options
```bash
--detailed              # Show detailed information
--type TYPE             # Filter by type
--format FORMAT         # Output format (table, json, csv)
--sort-by FIELD         # Sort by field (name, type, age, quality)
```

#### Examples
```bash
# Basic listing
snid template list templates/

# Detailed information
snid template list templates/ --detailed --type Ia --sort-by age

# Export as JSON
snid template list templates/ --format json --output templates.json
```

### info - Template Information

Get detailed information about a specific template.

#### Basic Usage
```bash
snid template info TEMPLATE_FILE [OPTIONS]
```

#### Options
```bash
--plot                  # Generate template plot
--metadata              # Show all metadata
```

#### Examples
```bash
# Basic template info
snid template info templates/sn1994I.dat

# With plot generation
snid template info templates/sn1994I.dat --plot

# Show all metadata
snid template info templates/sn1994I.dat --metadata
```

### add - Add Templates

Add a new spectrum to your template library.

#### Basic Usage
```bash
snid template add LIBRARY_DIR SPECTRUM_FILE [OPTIONS]
```

#### Options
```bash
--type TYPE             # Supernova type (Ia, Ib, Ic, II, etc.)
--subtype SUBTYPE       # Detailed subtype (norm, pec, IIn, IIP, etc.)
--age DAYS              # Days from maximum light
--name NAME             # Template name
--quality QUALITY       # Quality rating (0-10)
--metadata FILE         # Additional metadata file
```

#### Examples
```bash
# Add spectrum as template
snid template add my_library/ spectrum.dat \
    --type Ia --subtype norm --age 15.0 \
    --name sn2023abc --quality 8

# Add with metadata file
snid template add templates/ new_spectrum.dat \
    --type II --subtype IIP --age 5.0 \
    --name sn2023xyz --quality 7 \
    --metadata metadata.json
```

### create - Create Library

Create a new template library directory.

#### Basic Usage
```bash
snid template create LIBRARY_NAME [OPTIONS]
```

#### Options
```bash
--output-dir DIR        # Output directory
--description TEXT      # Library description
--copy-from SOURCE      # Copy existing library
```

#### Examples
```bash
# Create empty library
snid template create my_templates --output-dir libraries/ \
    --description "Custom template library"

# Copy existing library
snid template create backup_templates \
    --copy-from templates/ \
    --output-dir backups/
```

## Template Formats

### Supported Input Formats
- **ASCII files** (.dat, .txt, .ascii, .asci)
- **FITS files** (.fits, .fit)
- **Two-column format**: wavelength, flux
- **Space or tab separated values**

### Template Metadata
Templates can include metadata such as:
- Supernova type and subtype
- Age relative to maximum light
- Quality rating
- Observation details
- Redshift information
- Instrument details

## Best Practices

### Template Quality
- **High S/N**: Use spectra with good signal-to-noise ratio
- **Good coverage**: Ensure wavelength coverage matches your analysis needs
- **Proper calibration**: Verify wavelength and flux calibration
- **Documentation**: Include detailed metadata for each template

### Organization
- **Consistent naming**: Use clear, descriptive names
- **Type organization**: Group templates by supernova type
- **Quality ratings**: Assign appropriate quality scores
- **Regular updates**: Keep template library current

### Validation
- **Test templates**: Verify templates work with SNID SAGE
- **Cross-validation**: Check template performance
- **Documentation**: Maintain detailed records

## Advanced Usage

### Batch Template Operations
```bash
# Add multiple templates
for spectrum in new_templates/*.dat; do
    snid template add templates/ "$spectrum" \
        --type Ia --quality 6
done

# List templates by type
snid template list templates/ --type Ia --detailed
```

### Template Validation
```bash
# Check template quality
snid template list templates/ --detailed --sort-by quality

# Validate specific template
snid template info templates/sn1994I.dat --plot
```

## Troubleshooting

### Common Issues

**Template not found:**
- Check file path and permissions
- Verify template directory exists
- Ensure template file is readable

**Invalid template format:**
- Check file format (two-column ASCII or FITS)
- Verify wavelength units (Angstroms)
- Check for header lines or comments

**Poor template performance:**
- Review quality rating
- Check wavelength coverage
- Verify flux calibration

### Getting Help
- Use `snid template --help` for command options
- Check template file format with `head -20 template.dat`
- Verify template directory structure

## Next Steps

- **[CLI Reference](command-reference.md)** - Complete CLI documentation
- **[Batch Processing](batch-processing.md)** - Process multiple spectra
- **[Configuration Guide](../reference/configuration-guide.md)** - Configure template settings 