# SNID SAGE Icon Setup Guide

This guide explains how to set up the custom SNID SAGE icon across all operating systems to ensure it appears correctly in taskbars, docks, application menus, and file associations.

## Quick Start

**For all platforms:**
```bash
# Generate all platform-specific icons
python scripts/generate_platform_icons.py

# Set up platform-specific integration (auto-detects OS)
python scripts/setup_all_platform_icons.py
```

## Platform-Specific Setup

### Windows

**Requirements:**
- Python 3.8+
- pywin32 package: `pip install pywin32`

**Setup:**
```bash
# Generate Windows .ico files
python scripts/generate_platform_icons.py

# Complete Windows setup
python scripts/setup_windows_icons.py --all
```

**What this does:**
- ✅ Creates desktop shortcut with custom icon
- ✅ Adds Start Menu entry with custom icon
- ✅ Registers application in Windows registry
- ✅ Sets up file associations for spectrum files (.fits, .dat, .txt, .ascii, .asci, .spec)
- ✅ Creates batch launcher with icon
- ✅ Configures taskbar and Alt+Tab icon display

**Verification:**
1. Check desktop for "SNID SAGE" shortcut with custom icon
2. Look in Start Menu under "SNID SAGE" folder
3. Launch app and verify icon appears in taskbar
4. Right-click spectrum files and see "Open with SNID SAGE" option

### macOS

**Requirements:**
- macOS system with iconutil (built-in)
- Python 3.8+

**Setup:**
```bash
# Generate macOS .icns files (requires macOS)
python scripts/generate_platform_icons.py
python scripts/setup_macos_icons.py --all
```

**What this does:**
- ✅ Converts .iconset directories to .icns files using iconutil
- ✅ Creates SNID SAGE.app bundle in Applications folder
- ✅ Sets up file associations for spectrum files
- ✅ Registers with Launch Services for Spotlight search
- ✅ Creates desktop alias for easy access
- ✅ Configures Dock and Cmd+Tab icon display

**Manual Alternative (Automator):**
1. Open Automator → New Application
2. Add "Run Shell Script" action
3. Set script to: `cd '/path/to/SNID_SAGE' && python -m snid_sage.interfaces.gui.launcher`
4. Save as "SNID SAGE" in Applications
5. Right-click app → Get Info → drag icon.icns to icon area

**Verification:**
1. Check Applications folder for "SNID SAGE.app"
2. Drag to Dock for easy access
3. Launch app and verify icon appears in Dock
4. Check Cmd+Tab switcher shows custom icon

### Linux

**Requirements:**
- Linux with desktop environment (GNOME, KDE, XFCE, etc.)
- Python 3.8+
- Optional: PIL/Pillow for better icon scaling: `pip install Pillow`

**Setup:**
```bash
# Generate Linux icons and desktop integration
python scripts/generate_platform_icons.py
python scripts/setup_linux_icons.py --all
```

**What this does:**
- ✅ Installs icons to system icon theme (multiple sizes)
- ✅ Creates .desktop file for application menu
- ✅ Sets up desktop shortcut
- ✅ Configures MIME types for spectrum files
- ✅ Sets up file associations
- ✅ Creates command-line launcher script
- ✅ Updates desktop databases and icon caches

**Verification:**
1. Search for "SNID SAGE" in application menu
2. Check under Education → Science category
3. Verify desktop shortcut works
4. Launch app and verify icon appears in panel/taskbar
5. Try command: `snid-sage` (if ~/.local/bin is in PATH)

## Icon Files Structure

The icon system uses multiple formats for cross-platform compatibility:

```
images/
├── icon.ico           # Windows format (light theme)
├── icon_dark.ico      # Windows format (dark theme)
├── icon.icns          # macOS format (light theme)
├── icon_dark.icns     # macOS format (dark theme)
├── icon.png           # Linux/universal format (light theme)
├── icon_dark.png      # Linux/universal format (dark theme)
├── light.png          # Source image (light theme)
├── dark.png           # Source image (dark theme)
├── icon.iconset/      # macOS iconset directory
│   ├── icon_16x16.png
│   ├── icon_32x32.png
│   ├── icon_64x64.png
│   ├── icon_128x128.png
│   ├── icon_256x256.png
│   ├── icon_512x512.png
│   └── icon_1024x1024.png
└── icon_dark.iconset/ # macOS dark iconset directory
    └── (same structure as above)
```

## GUI Integration

The PySide6 GUI sets the window icon via Qt where available. Example calls found in the codebase:

```python
from PySide6 import QtGui
self.setWindowIcon(QtGui.QIcon(str(icon_path)))
```

**Supported platforms:**
- **Windows/macOS/Linux**: Uses Qt's `QIcon` handling of `.ico`, `.icns`, or `.png` depending on the file provided

## Troubleshooting

### Icon Not Appearing

**Windows:**
1. Ensure .ico files exist: `dir images\*.ico`
2. Check registry entries were created
3. Try logging out/in to refresh icon cache
4. Run setup script as administrator

**macOS:**
1. Ensure .icns files exist: `ls images/*.icns`
2. Restart Dock: `killall Dock`
3. Clear Launch Services cache: `/System/Library/Frameworks/CoreServices.framework/Frameworks/LaunchServices.framework/Support/lsregister -kill -r -domain local -domain system -domain user`
4. Verify iconutil is available: `which iconutil`

**Linux:**
1. Ensure .png files exist: `ls images/*.png`
2. Update icon cache: `gtk-update-icon-cache ~/.local/share/icons/hicolor/`
3. Update desktop database: `update-desktop-database ~/.local/share/applications/`
4. Check desktop environment variables: `echo $XDG_CURRENT_DESKTOP`

### File Associations Not Working

**Windows:**
- Check registry entries in `HKEY_CURRENT_USER\Software\Classes\`
- Verify file extensions are properly associated
- Try "Open with" → "Choose another app" → Browse for Python/SNID

**macOS:**
- Check Info.plist in application bundle
- Right-click file → Get Info → Open with → Change All
- Verify Launch Services registration

**Linux:**
- Check MIME types: `file --mime-type your_spectrum_file.fits`
- Verify associations: `xdg-mime query default application/x-fits-spectrum`
- Update MIME database: `update-mime-database ~/.local/share/mime/`

### Permission Issues

**All platforms:**
- Ensure write permissions to target directories
- On Linux/macOS: Check ~/.local/share/ permissions
- On Windows: May need administrator privileges for system-wide registration

## Manual Icon Replacement

If automatic setup fails, you can manually set icons:

**Windows:**
1. Right-click shortcut → Properties → Change Icon
2. Browse to `images\icon.ico`

**macOS:**
1. Right-click app → Get Info
2. Drag `images/icon.icns` to icon area in top-left

**Linux:**
1. Right-click .desktop file → Properties → Icon
2. Browse to `images/icon.png`

## Development Notes

**Adding new icon sizes:**
1. Edit `scripts/generate_platform_icons.py`
2. Add size to appropriate platform arrays
3. Regenerate icons

**Supporting new platforms:**
1. Update `CrossPlatformWindowManager.get_platform_icon_path()`
2. Add platform-specific icon loading logic
3. Create platform-specific setup script

**Icon design guidelines:**
- Use simple, recognizable symbols
- Ensure visibility at 16x16 pixels
- Provide both light and dark variants
- Use transparent backgrounds
- Save source files as PNG with high resolution (1024x1024 recommended)

## Related Files

- `snid_sage/interfaces/gui/utils/logo_manager.py` - Logo/icon management helpers
- `scripts/generate_platform_icons.py` - Icon generation
- `scripts/setup_windows_icons.py` - Windows-specific setup
- `scripts/setup_macos_icons.py` - macOS-specific setup
- `scripts/setup_linux_icons.py` - Linux-specific setup
- `scripts/setup_all_platform_icons.py` - Cross-platform setup
- `setup.py` / `pyproject.toml` - Package icon distribution 