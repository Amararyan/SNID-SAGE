"""
User Templates Path Resolver
===========================

- Single source of truth for resolving and persisting the User Templates directory.
- GUI should call with strict=True to avoid silent fallbacks and instead prompt users.
- CLI can decide policy (e.g., require config or allow legacy discovery explicitly).
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional
import os

try:
    from importlib import resources
except Exception:  # pragma: no cover
    resources = None  # type: ignore

from snid_sage.shared.utils.config.configuration_manager import ConfigurationManager


def _is_writable_dir(path: Path) -> bool:
    try:
        if not path.exists():
            path.mkdir(parents=True, exist_ok=True)
        return os.access(path, os.W_OK)
    except Exception:
        return False


def get_user_templates_dir(strict: bool = False) -> Optional[Path]:
    """
    Return the configured user templates directory, or None if unset/invalid.

    - strict=True: do not attempt any legacy fallbacks; only return configured path if valid
    - strict=False: same behavior for now (no implicit fallbacks). Legacy discovery should
      be explicitly requested by callers via discover_legacy_user_templates().
    """
    cm = ConfigurationManager()
    cfg = cm.get_current_config() or cm.load_config()
    paths = (cfg.get('paths') or {})
    override = paths.get('user_templates_dir')
    if override:
        p = Path(override)
        if _is_writable_dir(p):
            return p
    # No legacy fallback here; caller decides policy
    return None


def set_user_templates_dir(path: Path) -> None:
    """Persist the user templates directory into configuration after validation."""
    if not _is_writable_dir(path):
        raise PermissionError(f"User templates directory is not writable: {path}")

    cm = ConfigurationManager()
    cfg = cm.get_current_config() or cm.load_config()
    cfg.setdefault('paths', {})['user_templates_dir'] = str(path)
    cm.save_config(cfg)


def discover_legacy_user_templates() -> List[Path]:
    """
    Discover previous fallback locations that may contain an existing user library.

    This does NOT create directories; it only returns existing, writable candidates
    that contain hints of a user library (index or per-type user HDF5 files).
    """
    candidates: List[Path] = []

    # 0) If config already points to a dir that exists/writable, prefer it
    current = get_user_templates_dir(strict=False)
    if current and current.exists() and _is_writable_dir(current):
        candidates.append(current)

    # 1) Sibling to built-ins (snid_sage/templates/User_templates)
    try:
        if resources is not None:
            with resources.as_file(resources.files('snid_sage') / 'templates') as tpl_dir:
                p = (tpl_dir / 'User_templates')
                if p.exists() and _is_writable_dir(p):
                    candidates.append(p)
    except Exception:
        pass

    # 2) Documents/SNID_SAGE/User_templates
    try:
        docs = Path.home() / 'Documents' / 'SNID_SAGE' / 'User_templates'
        if docs.exists() and _is_writable_dir(docs):
            candidates.append(docs)
    except Exception:
        pass

    # 3) App config dir templates/User_templates
    try:
        cm = ConfigurationManager()
        appdata = Path(cm.config_dir) / 'templates' / 'User_templates'
        if appdata.exists() and _is_writable_dir(appdata):
            candidates.append(appdata)
    except Exception:
        pass

    # 4) Home fallback ~/.snid_sage/User_templates
    try:
        home_fb = Path.home() / '.snid_sage' / 'User_templates'
        if home_fb.exists() and _is_writable_dir(home_fb):
            candidates.append(home_fb)
    except Exception:
        pass

    # Filter for libraries that look populated
    filtered: List[Path] = []
    seen = set()
    for p in candidates:
        key = str(p.resolve())
        if key in seen:
            continue
        seen.add(key)
        try:
            has_index = (p / 'template_index.user.json').exists()
            has_h5 = any(p.glob('templates_*.user.hdf5'))
            if has_index or has_h5:
                filtered.append(p)
        except Exception:
            continue

    return filtered


__all__ = [
    'get_user_templates_dir',
    'set_user_templates_dir',
    'discover_legacy_user_templates',
]


