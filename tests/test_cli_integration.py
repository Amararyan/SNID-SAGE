#!/usr/bin/env python3
"""
SNID SAGE CLI Integration Tests
===============================

Test suite for the restructured CLI interface after the project reorganization.
Tests all major CLI functionality including output directory handling.

Run with: python tests/test_cli_integration.py
"""

import os
import sys
import shutil
import tempfile
import subprocess
from pathlib import Path
import json

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def run_cli_command(cmd, cwd=None):
    """Run a CLI command and return results."""
    if cwd is None:
        cwd = project_root
    
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd,
            capture_output=True, 
            text=True, 
            timeout=300,  # 5 minute timeout
            encoding='utf-8',
            errors='replace'  # Replace problematic characters instead of failing
        )
        return {
            'returncode': result.returncode,
            'stdout': result.stdout,
            'stderr': result.stderr,
            'success': result.returncode == 0
        }
    except subprocess.TimeoutExpired:
        return {
            'returncode': -1,
            'stdout': '',
            'stderr': 'Command timed out',
            'success': False
        }
    except Exception as e:
        return {
            'returncode': -1,
            'stdout': '',
            'stderr': str(e),
            'success': False
        }

def test_basic_cli_import():
    """Test that CLI imports work correctly after restructuring."""
    print("🔍 Testing CLI imports...")
    
    # Test direct import
    try:
        from interfaces.cli.main import main
        print("  ✅ Direct import successful")
    except ImportError as e:
        print(f"  ❌ Direct import failed: {e}")
        return False
    
    # Test CLI launcher import
    cmd = 'python -c "from interfaces.cli.main import main; print(\'CLI import successful\')"'
    result = run_cli_command(cmd)
    
    if result['success'] and 'CLI import successful' in result['stdout']:
        print("  ✅ CLI launcher import successful")
        return True
    else:
        print(f"  ❌ CLI launcher import failed: {result['stderr']}")
        return False

def test_cli_help():
    """Test CLI help system."""
    print("🔍 Testing CLI help system...")
    
    # Test main help
    result = run_cli_command('python run_snid_cli.py --help')
    if result['success'] and 'SNID SAGE' in result['stdout']:
        print("  ✅ Main help working")
    else:
        print(f"  ❌ Main help failed: {result['stderr']}")
        return False
    
    # Test subcommand help
    result = run_cli_command('python run_snid_cli.py identify --help')
    if result['success'] and 'spectrum_path' in result['stdout']:
        print("  ✅ Identify help working")
    else:
        print(f"  ❌ Identify help failed: {result['stderr']}")
        return False
    
    return True

def test_template_listing():
    """Test template listing functionality."""
    print("🔍 Testing template listing...")
    
    # Check if templates directory exists
    templates_dir = project_root / 'templates'
    if not templates_dir.exists():
        print("  ⚠️  Templates directory not found, skipping template tests")
        return True
    
    result = run_cli_command('python run_snid_cli.py template list templates/')
    if result['success'] and ('templates' in result['stdout'].lower() or 'Template Library' in result['stdout']):
        print("  ✅ Template listing working")
        return True
    else:
        print(f"  ❌ Template listing failed: {result['stderr']}")
        return False

def test_output_directory_fix():
    """Test the critical output directory fix."""
    print("🔍 Testing output directory fix...")
    
    # Check if we have test data
    test_spectrum = project_root / 'data' / 'sn2003jo.dat'
    templates_dir = project_root / 'templates'
    
    if not test_spectrum.exists():
        print("  ⚠️  Test spectrum not found, skipping output test")
        return True
    
    if not templates_dir.exists():
        print("  ⚠️  Templates directory not found, skipping output test")
        return True
    
    # Create temporary output directory
    with tempfile.TemporaryDirectory() as temp_dir:
        output_dir = Path(temp_dir) / 'test_results'
        
        # Run analysis with output directory
        cmd = f'python run_snid_cli.py identify "{test_spectrum}" "{templates_dir}" --output-dir "{output_dir}" --save-plots --output-main'
        print(f"  Running: {cmd}")
        
        result = run_cli_command(cmd)
        
        if not result['success']:
            print(f"  ❌ Analysis failed: {result['stderr']}")
            return False
        
        # Check if output directory was created
        if not output_dir.exists():
            print("  ❌ Output directory was not created")
            return False
        
        # Check for expected files
        expected_files = [
            'sn2003jo_snid.output',  # Main results
        ]
        
        expected_plots = [
            'snid_comparison.png',
            'snid_correlation.png', 
            'snid_gmm_clustering.png',
            'snid_redshift_age.png',
            'snid_type_fractions.png'
        ]
        
        # Check main files
        missing_files = []
        for filename in expected_files:
            filepath = output_dir / filename
            if not filepath.exists():
                missing_files.append(filename)
        
        # Check plot files (the critical fix)
        missing_plots = []
        for filename in expected_plots:
            filepath = output_dir / filename
            if not filepath.exists():
                missing_plots.append(filename)
        
        if missing_files:
            print(f"  ❌ Missing main files: {missing_files}")
            return False
        
        if missing_plots:
            print(f"  ❌ Missing plot files: {missing_plots}")
            print(f"  🔧 This indicates the output directory fix may not be working")
            return False
        
        print("  ✅ All output files correctly saved to specified directory")
        print(f"  ✅ Output directory fix working correctly")
        
        # List what was created
        created_files = list(output_dir.glob('*'))
        print(f"  📁 Created {len(created_files)} files in output directory")
        
        return True

def test_bin_scripts():
    """Test the bin scripts with path fixes."""
    print("🔍 Testing bin scripts...")
    
    bin_dir = project_root / 'scripts' / 'entry_points' / 'bin'
    
    # Test snid script
    snid_script = bin_dir / 'snid'
    if snid_script.exists():
        result = run_cli_command(f'python "{snid_script}" --help')
        if result['success']:
            print("  ✅ snid bin script working")
        else:
            print(f"  ❌ snid bin script failed: {result['stderr']}")
            return False
    else:
        print("  ⚠️  snid bin script not found")
    
    return True

def run_all_tests():
    """Run all CLI integration tests."""
    print("="*60)
    print("SNID SAGE CLI Integration Test Suite")
    print("="*60)
    print(f"Project root: {project_root}")
    print()
    
    tests = [
        ("Basic CLI imports", test_basic_cli_import),
        ("CLI help system", test_cli_help), 
        ("Template listing", test_template_listing),
        ("Output directory fix", test_output_directory_fix),
        ("Bin scripts", test_bin_scripts)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"Running test: {test_name}")
        try:
            success = test_func()
            results[test_name] = success
            status = "✅ PASSED" if success else "❌ FAILED"
            print(f"  Result: {status}")
        except Exception as e:
            print(f"  ❌ ERROR: {e}")
            results[test_name] = False
        print()
    
    # Summary
    print("="*60)
    print("TEST RESULTS SUMMARY")
    print("="*60)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, success in results.items():
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{test_name:30} {status}")
    
    print()
    print(f"Overall: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! CLI is fully functional after restructuring.")
        return True
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 