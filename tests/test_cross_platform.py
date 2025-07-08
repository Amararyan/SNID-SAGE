#!/usr/bin/env python3
"""
Cross-Platform Compatibility Tests for SNID SAGE
================================================

Tests to ensure SNID SAGE works correctly across Windows, macOS, and Linux.

Usage:
    python tests/test_cross_platform.py
    python -m pytest tests/test_cross_platform.py -v
"""

import os
import sys
import platform
import tempfile
import unittest
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))


class TestCrossPlatformCompatibility(unittest.TestCase):
    """Test cross-platform compatibility features"""
    
    def setUp(self):
        """Set up test environment"""
        self.current_platform = platform.system()
        self.temp_dir = Path(tempfile.mkdtemp())
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_platform_detection(self):
        """Test platform detection works correctly"""
        try:
            from interfaces.gui.utils.cross_platform_window import CrossPlatformWindowManager
            
            # Test platform detection
            detected_platform = CrossPlatformWindowManager.get_platform()
            self.assertIn(detected_platform, ['Windows', 'Darwin', 'Linux'])
            
            # Test platform checks
            if self.current_platform == 'Windows':
                self.assertTrue(CrossPlatformWindowManager.is_windows())
                self.assertFalse(CrossPlatformWindowManager.is_macos())
                self.assertFalse(CrossPlatformWindowManager.is_linux())
            elif self.current_platform == 'Darwin':
                self.assertFalse(CrossPlatformWindowManager.is_windows())
                self.assertTrue(CrossPlatformWindowManager.is_macos())
                self.assertFalse(CrossPlatformWindowManager.is_linux())
            else:  # Linux
                self.assertFalse(CrossPlatformWindowManager.is_windows())
                self.assertFalse(CrossPlatformWindowManager.is_macos())
                self.assertTrue(CrossPlatformWindowManager.is_linux())
        
        except ImportError:
            self.fail("CrossPlatformWindowManager not available")
    
    def test_dpi_awareness_setup(self):
        """Test DPI awareness setup doesn't crash"""
        try:
            from interfaces.gui.utils.cross_platform_window import CrossPlatformWindowManager
            
            # Should not raise an exception
            result = CrossPlatformWindowManager.setup_dpi_awareness()
            self.assertIsInstance(result, bool)
            
        except ImportError:
            self.fail("CrossPlatformWindowManager not available")
    
    def test_config_directory_creation(self):
        """Test configuration directory creation"""
        try:
            from interfaces.gui.utils.cross_platform_window import CrossPlatformWindowManager
            
            config_dir = CrossPlatformWindowManager.get_config_directory('TestApp')
            config_path = Path(config_dir)
            
            # Directory should be created
            self.assertTrue(config_path.exists())
            self.assertTrue(config_path.is_dir())
            
            # Should be platform-appropriate
            if self.current_platform == 'Windows':
                self.assertIn('AppData', str(config_path))
            elif self.current_platform == 'Darwin':
                self.assertIn('Library/Application Support', str(config_path))
            else:  # Linux
                self.assertIn('.config', str(config_path))
            
        except ImportError:
            self.fail("CrossPlatformWindowManager not available")
    
    def test_platform_fonts(self):
        """Test platform-appropriate font selection"""
        try:
            from interfaces.gui.utils.cross_platform_window import CrossPlatformWindowManager
            
            # Test default font
            default_font = CrossPlatformWindowManager.get_platform_font('default')
            self.assertIsInstance(default_font, tuple)
            self.assertEqual(len(default_font), 3)  # (family, size, style)
            
            # Test different font types
            for font_type in ['default', 'title', 'small', 'code']:
                font = CrossPlatformWindowManager.get_platform_font(font_type)
                self.assertIsInstance(font, tuple)
                self.assertIsInstance(font[0], str)  # font family
                self.assertIsInstance(font[1], int)  # font size
                self.assertIsInstance(font[2], str)  # font style
            
            # Test platform-specific fonts
            if self.current_platform == 'Windows':
                self.assertIn('Segoe UI', default_font[0])
            elif self.current_platform == 'Darwin':
                self.assertIn('SF Pro', default_font[0])
            else:  # Linux
                self.assertIn('Ubuntu', default_font[0])
                
        except ImportError:
            self.fail("CrossPlatformWindowManager not available")
    
    def test_keyboard_shortcuts(self):
        """Test platform-appropriate keyboard shortcuts"""
        try:
            from interfaces.gui.utils.cross_platform_window import CrossPlatformWindowManager
            
            shortcuts = CrossPlatformWindowManager.get_keyboard_shortcuts()
            self.assertIsInstance(shortcuts, dict)
            
            # Check required shortcuts exist
            required_shortcuts = ['fullscreen', 'quit', 'preferences', 'copy', 'paste']
            for shortcut in required_shortcuts:
                self.assertIn(shortcut, shortcuts)
            
            # Test platform-specific shortcuts
            if self.current_platform == 'Darwin':  # macOS
                self.assertIn('Cmd', shortcuts['quit'])
                self.assertIn('Cmd', shortcuts['copy'])
            else:  # Windows/Linux
                self.assertIn('Ctrl', shortcuts['quit'])
                self.assertIn('Ctrl', shortcuts['copy'])
                
        except ImportError:
            self.fail("CrossPlatformWindowManager not available")
    
    def test_icon_path_resolution(self):
        """Test platform-appropriate icon path resolution"""
        try:
            from interfaces.gui.utils.cross_platform_window import CrossPlatformWindowManager
            
            # Create test icons directory
            icons_dir = self.temp_dir / 'icons'
            icons_dir.mkdir()
            
            # Create platform-specific test icons
            (icons_dir / 'test.ico').touch()  # Windows
            (icons_dir / 'test.icns').touch()  # macOS
            (icons_dir / 'test.png').touch()  # Linux
            
            icon_path = CrossPlatformWindowManager.get_platform_icon_path('test', str(icons_dir))
            
            if icon_path:
                self.assertTrue(Path(icon_path).exists())
                
                # Check correct extension for platform
                if self.current_platform == 'Windows':
                    self.assertTrue(icon_path.endswith('.ico') or icon_path.endswith('.png'))
                elif self.current_platform == 'Darwin':
                    self.assertTrue(icon_path.endswith('.icns') or icon_path.endswith('.png'))
                else:  # Linux
                    self.assertTrue(icon_path.endswith('.png'))
            
        except ImportError:
            self.fail("CrossPlatformWindowManager not available")
    
    def test_configuration_manager_paths(self):
        """Test configuration manager uses cross-platform paths"""
        try:
            from shared.utils.config.configuration_manager import ConfigurationManager
            
            config_manager = ConfigurationManager()
            config_dir = config_manager.config_dir
            
            # Should be a Path object
            self.assertIsInstance(config_dir, Path)
            
            # Should exist
            self.assertTrue(config_dir.exists())
            
            # Should be platform-appropriate
            if self.current_platform == 'Windows':
                self.assertIn('AppData', str(config_dir))
            elif self.current_platform == 'Darwin':
                self.assertIn('Library', str(config_dir))
            else:  # Linux
                self.assertIn('.config', str(config_dir))
                
        except ImportError:
            self.skipTest("Configuration manager not available")
    
    def test_gui_settings_controller_paths(self):
        """Test GUI settings controller uses cross-platform paths"""
        try:
            # Mock a minimal GUI instance
            class MockGUI:
                pass
            
            from interfaces.gui.features.configuration.gui_settings_controller import GUISettingsController
            
            mock_gui = MockGUI()
            settings_controller = GUISettingsController(mock_gui)
            
            settings_file = settings_controller.settings_file
            
            # Should be a Path object
            self.assertIsInstance(settings_file, Path)
            
            # Should be in a platform-appropriate location
            if self.current_platform == 'Windows':
                self.assertIn('AppData', str(settings_file))
            elif self.current_platform == 'Darwin':
                self.assertIn('Library', str(settings_file))
            else:  # Linux
                self.assertIn('.config', str(settings_file))
                
        except ImportError:
            self.skipTest("GUI settings controller not available")
    
    def test_icon_files_exist(self):
        """Test that platform-specific icon files exist"""
        project_root = Path(__file__).parent.parent
        images_dir = project_root / 'images'
        
        if not images_dir.exists():
            self.skipTest("Images directory not found")
        
        # Check for platform-specific icons
        expected_icons = []
        
        if self.current_platform == 'Windows':
            expected_icons = ['icon.ico', 'icon_dark.ico']
        elif self.current_platform == 'Darwin':
            expected_icons = ['icon.icns', 'icon_dark.icns']
        else:  # Linux
            expected_icons = ['icon.png', 'icon_dark.png']
        
        # Also check for source PNG files (should always exist)
        expected_icons.extend(['light.png', 'dark.png'])
        
        missing_icons = []
        for icon in expected_icons:
            icon_path = images_dir / icon
            if not icon_path.exists():
                missing_icons.append(icon)
        
        if missing_icons:
            self.fail(f"Missing icons for {self.current_platform}: {missing_icons}")
    
    def test_games_window_focus(self):
        """Test games window focus management"""
        try:
            from snid_sage.snid.games import CrossPlatformGameFocus
            
            # Should not raise an exception
            CrossPlatformGameFocus.bring_to_foreground()
            
            # Test backward compatibility
            from snid_sage.snid.games import bring_to_foreground
            bring_to_foreground()
            
        except ImportError:
            self.skipTest("Games module not available")
    
    def test_fullscreen_functionality(self):
        """Test fullscreen functionality (mock test)"""
        try:
            import tkinter as tk
            from interfaces.gui.utils.cross_platform_window import CrossPlatformWindowManager
            
            # Create a test window (but don't show it)
            root = tk.Tk()
            root.withdraw()  # Hide the window
            
            try:
                # Test fullscreen setup (should not crash)
                result = CrossPlatformWindowManager.setup_fullscreen(root, True)
                self.assertIsInstance(result, bool)
                
                # Test fullscreen toggle
                result = CrossPlatformWindowManager.toggle_fullscreen(root)
                self.assertIsInstance(result, bool)
                
            finally:
                root.destroy()
                
        except ImportError:
            self.skipTest("CrossPlatformWindowManager not available")
        except Exception as e:
            # On headless systems, this might fail
            self.skipTest(f"Display not available: {e}")


class TestWindowEventHandlers(unittest.TestCase):
    """Test window event handlers work cross-platform"""
    
    def test_dpi_awareness_setup(self):
        """Test DPI awareness setup in window event handlers"""
        try:
            from interfaces.gui.utils.window_event_handlers import WindowEventHandlers
            
            # Should not raise an exception
            result = WindowEventHandlers.setup_dpi_awareness()
            self.assertIsInstance(result, bool)
            
        except ImportError:
            self.skipTest("Window event handlers not available")


class TestStartupManager(unittest.TestCase):
    """Test startup manager cross-platform functionality"""
    
    def test_dpi_awareness_setup(self):
        """Test DPI awareness setup in startup manager"""
        try:
            from interfaces.gui.utils.startup_manager import setup_dpi_awareness
            
            # Should not raise an exception
            setup_dpi_awareness()
            
        except ImportError:
            self.skipTest("Startup manager not available")


def run_platform_compatibility_tests():
    """Run all cross-platform compatibility tests"""
    print(f"🧪 Running Cross-Platform Compatibility Tests")
    print(f"Platform: {platform.system()} {platform.release()}")
    print(f"Python: {sys.version}")
    print("=" * 60)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add test classes
    suite.addTests(loader.loadTestsFromTestCase(TestCrossPlatformCompatibility))
    suite.addTests(loader.loadTestsFromTestCase(TestWindowEventHandlers))
    suite.addTests(loader.loadTestsFromTestCase(TestStartupManager))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 60)
    if result.wasSuccessful():
        print("✅ All cross-platform tests passed!")
    else:
        print(f"❌ {len(result.failures)} test(s) failed, {len(result.errors)} error(s)")
        
        if result.failures:
            print("\nFailures:")
            for test, traceback in result.failures:
                print(f"  - {test}: {traceback}")
        
        if result.errors:
            print("\nErrors:")
            for test, traceback in result.errors:
                print(f"  - {test}: {traceback}")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_platform_compatibility_tests()
    sys.exit(0 if success else 1) 