# Changelog

All notable changes to SNID SAGE will be documented in this file.

## [0.6.0] - 2025-08-18

### Changed
- **BREAKING**: CLI command renamed from `snid` to `sage` to avoid conflicts with existing SNID tool
- **BREAKING**: GUI utility commands renamed from `snid-lines`/`snid-templates` to `snid-sage-lines`/`snid-sage-templates`
- Updated all documentation to reflect new command names
- CLI tutorial now uses real analysis results from SN2018bif.fits

### Technical
- Updated `pyproject.toml` entry points for new command names
- Modified CLI modules to use `sage` command name
- Updated all documentation examples and references

### Migration Notes
- CLI users: replace `snid` with `sage` in all commands
- GUI users: no changes needed for main `snid-sage` command
- GUI utility users: update to `snid-sage-lines` and `snid-sage-templates`

---
