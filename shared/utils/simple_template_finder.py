"""
Simple Template Discovery Utility
=================================

Simplified template finder for GitHub-only distribution.
Assumes templates are always in the 'templates' directory relative to project root.
"""

import os
from pathlib import Path
from typing import Optional
from shared.utils.logging import get_logger

logger = get_logger('simple_template_finder')


def find_templates_directory() -> Optional[Path]:
    """
    Find the templates directory for GitHub-based installations.
    
    For GitHub installations, templates are always in the 'templates' 
    directory at the project root.
    
    Returns:
        Path to templates directory if found, None otherwise
    """
    # Strategy 1: Check current working directory
    cwd = Path.cwd()
    templates_dir = cwd / 'templates'
    if _validate_templates_directory(templates_dir):
        return templates_dir
    
    # Strategy 2: Find project root by looking for key files
    current = Path(__file__).resolve().parent
    for _ in range(10):  # Limit search depth
        # Look for project markers
        if any((current / marker).exists() for marker in ['pyproject.toml', 'setup.py', 'README.md']):
            templates_dir = current / 'templates'
            if _validate_templates_directory(templates_dir):
                return templates_dir
        current = current.parent
        if current == current.parent:  # Reached filesystem root
            break
    
    # Strategy 3: Check relative to module location (go up directories)
    current = Path(__file__).resolve().parent
    for _ in range(10):
        templates_dir = current / 'templates'
        if _validate_templates_directory(templates_dir):
            return templates_dir
        current = current.parent
        if current == current.parent:
            break
    
    logger.warning("No valid templates directory found")
    return None


def _validate_templates_directory(templates_dir: Path) -> bool:
    """
    Validate that a directory contains valid SNID templates.
    
    Args:
        templates_dir: Path to check
        
    Returns:
        True if directory contains valid templates
    """
    try:
        if not templates_dir.exists() or not templates_dir.is_dir():
            return False
        
        # Check for HDF5 template files (preferred format)
        hdf5_files = list(templates_dir.glob('templates_*.hdf5'))
        if hdf5_files:
            return True
        
        # Fallback: check for .lnw files (legacy format)
        lnw_files = list(templates_dir.glob('*.lnw'))
        return len(lnw_files) > 0
        
    except Exception:
        return False


def find_templates_directory_or_raise() -> Path:
    """
    Find templates directory or raise an exception.
    
    Returns:
        Path to templates directory
        
    Raises:
        FileNotFoundError: If templates directory cannot be found
    """
    templates_dir = find_templates_directory()
    if templates_dir is None:
        raise FileNotFoundError(
            "Could not find SNID templates directory.\n"
            "For GitHub installations, ensure you have cloned the full repository:\n"
            "  git clone https://github.com/FiorenSt/SNID-SAGE.git\n"
            "Templates should be in the 'templates/' directory at the project root."
        )
    return templates_dir


if __name__ == "__main__":
    logger.info("SNID Simple Template Directory Finder")
    logger.info("=" * 50)
    
    templates_dir = find_templates_directory()
    if templates_dir:
        logger.info(f"✅ Templates found: {templates_dir}")
        
        # Show what's in the directory
        hdf5_files = list(templates_dir.glob('templates_*.hdf5'))
        lnw_files = list(templates_dir.glob('*.lnw'))
        
        if hdf5_files:
            logger.info(f"   📁 HDF5 template files: {len(hdf5_files)}")
        if lnw_files:
            logger.info(f"   📁 LNW template files: {len(lnw_files)}")
    else:
        logger.error("❌ No templates directory found")
        logger.error("Ensure you have cloned the full SNID-SAGE repository from GitHub") 