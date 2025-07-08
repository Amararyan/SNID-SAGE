"""
Simple Template Discovery Utility
=================================

Simplified template finder for both GitHub installations and installed packages.
"""

import os
import sys
from pathlib import Path
from typing import Optional
from shared.utils.logging import get_logger

logger = get_logger('simple_template_finder')


def find_templates_directory() -> Optional[Path]:
    """
    Find the templates directory for both GitHub installations and installed packages.
    
    For GitHub installations, templates are in the 'templates' directory at the project root.
    For installed packages, templates are included in the package data.
    
    Returns:
        Path to templates directory if found, None otherwise
    """
    # Strategy 1: Check if we're in an installed package using importlib.resources
    try:
        import importlib.resources as pkg_resources
        
        # For Python 3.9+ with improved traversable API
        if hasattr(pkg_resources, 'files'):
            try:
                # Try to access the templates directory within the installed package
                # The package name will be snid_sage when installed via pip
                templates_package = pkg_resources.files('snid_sage') / 'templates'
                if templates_package.exists():
                    # Convert to Path and validate
                    templates_dir = Path(str(templates_package))
                    if _validate_templates_directory(templates_dir):
                        logger.info(f"✅ Found templates in installed package (files API): {templates_dir}")
                        return templates_dir
            except Exception as e:
                logger.debug(f"Files API with snid_sage failed: {e}")
                
            # Try alternative package names that might be used during development
            for pkg_name in ['snid_sage', 'SNID_SAGE', '.']:
                try:
                    templates_package = pkg_resources.files(pkg_name) / 'templates'
                    if templates_package.exists():
                        templates_dir = Path(str(templates_package))
                        if _validate_templates_directory(templates_dir):
                            logger.info(f"✅ Found templates in package {pkg_name} (files API): {templates_dir}")
                            return templates_dir
                except Exception as e:
                    logger.debug(f"Files API with {pkg_name} failed: {e}")
        
        # Fallback for older Python versions or if files API fails
        # Try accessing package resources directly
        for pkg_structure in [
            ('snid_sage', 'templates/template_index.json'),
            ('snid_sage.templates', 'template_index.json'), 
            ('.', 'templates/template_index.json'),
        ]:
            try:
                pkg_name, resource_path = pkg_structure
                with pkg_resources.path(pkg_name, resource_path) as template_path:
                    if 'templates/' in resource_path:
                        templates_dir = template_path.parent
                    else:
                        templates_dir = template_path.parent
                    if _validate_templates_directory(templates_dir):
                        logger.info(f"✅ Found templates in package {pkg_name} (path API): {templates_dir}")
                        return templates_dir
            except Exception as e:
                logger.debug(f"Path API with {pkg_structure} failed: {e}")
            
    except ImportError:
        logger.debug("importlib.resources not available")
    
    # Strategy 2: Check site-packages for installed package
    try:
        # Look for snid-sage in site-packages
        for path in sys.path:
            if 'site-packages' in path:
                site_packages = Path(path)
                
                # Check for different possible installation names
                for pkg_name in ['snid_sage', 'snid-sage', 'SNID_SAGE']:
                    pkg_dir = site_packages / pkg_name
                    if pkg_dir.exists():
                        templates_dir = pkg_dir / 'templates'
                        if _validate_templates_directory(templates_dir):
                            logger.info(f"✅ Found templates in site-packages: {templates_dir}")
                            return templates_dir
                        
                        # Also check for templates at package root level
                        templates_dir = site_packages / 'templates'
                        if _validate_templates_directory(templates_dir):
                            logger.info(f"✅ Found templates at site-packages root: {templates_dir}")
                            return templates_dir
    except Exception as e:
        logger.debug(f"Site-packages search failed: {e}")
    
    # Strategy 3: Check current working directory
    cwd = Path.cwd()
    templates_dir = cwd / 'templates'
    if _validate_templates_directory(templates_dir):
        logger.info(f"✅ Found templates in current directory: {templates_dir}")
        return templates_dir
    
    # Strategy 4: Find project root by looking for key files
    current = Path(__file__).resolve().parent
    for _ in range(10):  # Limit search depth
        # Look for project markers
        if any((current / marker).exists() for marker in ['pyproject.toml', 'setup.py', 'README.md']):
            templates_dir = current / 'templates'
            if _validate_templates_directory(templates_dir):
                logger.info(f"✅ Found templates relative to project root: {templates_dir}")
                return templates_dir
        current = current.parent
        if current == current.parent:  # Reached filesystem root
            break
    
    # Strategy 5: Check relative to module location (go up directories)
    current = Path(__file__).resolve().parent
    for _ in range(10):
        templates_dir = current / 'templates'
        if _validate_templates_directory(templates_dir):
            logger.info(f"✅ Found templates relative to module: {templates_dir}")
            return templates_dir
        current = current.parent
        if current == current.parent:
            break
    
    # Strategy 6: Check common installation paths
    common_paths = [
        Path.home() / '.local' / 'lib' / 'python*' / 'site-packages' / 'snid_sage' / 'templates',
        Path.home() / '.local' / 'share' / 'snid-sage' / 'templates',
        Path('/usr/local/lib/python*/site-packages/snid_sage/templates'),
        Path('/usr/share/snid-sage/templates'),
    ]
    
    for template_path in common_paths:
        # Handle wildcards in path
        if '*' in str(template_path):
            parent = template_path.parent
            pattern = template_path.name
            try:
                for candidate in parent.glob(pattern):
                    if _validate_templates_directory(candidate):
                        logger.info(f"✅ Found templates in common path: {candidate}")
                        return candidate
            except Exception:
                continue
        else:
            if _validate_templates_directory(template_path):
                logger.info(f"✅ Found templates in common path: {template_path}")
                return template_path
    
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
            logger.debug(f"Found {len(hdf5_files)} HDF5 template files in {templates_dir}")
            return True
        
        # Fallback: check for .lnw files (legacy format)
        lnw_files = list(templates_dir.glob('*.lnw'))
        if len(lnw_files) > 0:
            logger.debug(f"Found {len(lnw_files)} LNW template files in {templates_dir}")
            return True
        
        logger.debug(f"No template files found in {templates_dir}")
        return False
        
    except Exception as e:
        logger.debug(f"Error validating templates directory {templates_dir}: {e}")
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
            "For pip installations, ensure templates were included in the package.\n"
            "Templates should be in the 'templates/' directory."
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
            for hdf5_file in hdf5_files[:5]:  # Show first 5
                logger.info(f"      - {hdf5_file.name}")
            if len(hdf5_files) > 5:
                logger.info(f"      ... and {len(hdf5_files) - 5} more")
        if lnw_files:
            logger.info(f"   📁 LNW template files: {len(lnw_files)}")
    else:
        logger.error("❌ No templates directory found")
        logger.error("Ensure you have cloned the full SNID-SAGE repository from GitHub")
        logger.error("or that templates were included in your pip installation") 