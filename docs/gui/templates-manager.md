## Templates GUI

Interactive manager for exploring, creating, and organizing templates.

### Overview
- Left: Template browser (search, type filter)
- Right: Tabs for Viewer, Create, Manage, Compare, Statistics
- Status bar: template count

### Data source and overrides
- The browser lists templates using a merged index:
  - Base index: `snid_sage/templates/template_index.json`
  - User index: `snid_sage/templates/User_templates/template_index.user.json`
- If a per-type user HDF5 exists (e.g., `User_templates/templates_Ia.user.hdf5`), entries for that type come exclusively from the user file; base entries for the same type are hidden. This prevents duplicates in the UI and reflects user edits immediately.

### Tasks
- Browse and preview templates with metadata
- Create templates from spectra (wizard)
- Edit metadata and reorganize
- Compare templates and generate statistics

### Tips
- Use type filters to speed navigation
- Keep metadata complete for research reuse

### Related CLI
See `snid template` subcommands for scripting the same operations.

