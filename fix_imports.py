#!/usr/bin/env python3
"""
Script to fix relative imports to absolute imports in the snid_sage package.
"""

import os
import re
from pathlib import Path

def fix_imports_in_file(file_path):
    """Fix relative imports in a single file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original_content = content
        
        # Fix 'from shared.' imports
        content = re.sub(r'from shared\.', 'from snid_sage.shared.', content)
        
        # Fix 'from interfaces.' imports
        content = re.sub(r'from interfaces\.', 'from snid_sage.interfaces.', content)
        
        # Fix 'from snid.' imports (but not snid_sage.)
        content = re.sub(r'from snid\.(?!_sage)', 'from snid_sage.snid.', content)
        
        # Fix 'import shared.' imports
        content = re.sub(r'import shared\.', 'import snid_sage.shared.', content)
        
        # Fix 'import interfaces.' imports
        content = re.sub(r'import interfaces\.', 'import snid_sage.interfaces.', content)
        
        # Fix 'import snid.' imports (but not snid_sage.)
        content = re.sub(r'import snid\.(?!_sage)', 'import snid_sage.snid.', content)
        
        if content != original_content:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed imports in: {file_path}")
            return True
        return False
        
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        return False

def fix_all_imports():
    """Fix imports in all Python files in the snid_sage package."""
    snid_sage_dir = Path('snid_sage')
    
    if not snid_sage_dir.exists():
        print("snid_sage directory not found!")
        return
    
    fixed_count = 0
    total_count = 0
    
    for py_file in snid_sage_dir.rglob('*.py'):
        total_count += 1
        if fix_imports_in_file(py_file):
            fixed_count += 1
    
    print(f"\nProcessed {total_count} Python files")
    print(f"Fixed imports in {fixed_count} files")

if __name__ == '__main__':
    fix_all_imports() 