"""
Cross-Platform Window Manager for SNID SAGE
==========================================

Provides platform-agnostic window management functionality to ensure
consistent behavior across Windows, macOS, and Linux systems.

This module abstracts OS-specific window operations including:
- DPI awareness setup
- Fullscreen management  
- Window theming
- Icon management
- Font selection
- Keyboard shortcuts
"""

import os
import sys
import platform
import tkinter as tk
from pathlib import Path
from typing import Dict, Optional, Tuple, Any

# Import the centralized logging system
try:
    from shared.utils.logging import get_logger
    _LOGGER = get_logger('gui.cross_platform')
except ImportError:
    import logging
    _LOGGER = logging.getLogger('gui.cross_platform')


class CrossPlatformWindowManager:
    """
    Cross-platform window management utilities for consistent behavior
    across Windows, macOS, and Linux systems.
    """
    
    # Platform constants
    WINDOWS = "Windows"
    MACOS = "Darwin" 
    LINUX = "Linux"
    
    # Font mappings for each platform
    PLATFORM_FONTS = {
        WINDOWS: {
            'default': ('Segoe UI', 12, 'normal'),
            'title': ('Segoe UI', 16, 'bold'),
            'small': ('Segoe UI', 10, 'normal'),
            'code': ('Consolas', 11, 'normal')
        },
        MACOS: {
            'default': ('SF Pro Display', 12, 'normal'),
            'title': ('SF Pro Display', 16, 'bold'),
            'small': ('SF Pro Display', 10, 'normal'),
            'code': ('SF Mono', 11, 'normal')
        },
        LINUX: {
            'default': ('Ubuntu', 12, 'normal'),
            'title': ('Ubuntu', 16, 'bold'),
            'small': ('Ubuntu', 10, 'normal'),
            'code': ('Ubuntu Mono', 11, 'normal')
        }
    }
    
    # Keyboard shortcuts for each platform
    PLATFORM_SHORTCUTS = {
        WINDOWS: {
            'fullscreen': 'F11',
            'quit': 'Ctrl+Q',
            'preferences': 'Ctrl+P',
            'close': 'Alt+F4',
            'minimize': 'Ctrl+M',
            'copy': 'Ctrl+C',
            'paste': 'Ctrl+V',
            'select_all': 'Ctrl+A'
        },
        MACOS: {
            'fullscreen': 'Cmd+Ctrl+F',
            'quit': 'Cmd+Q', 
            'preferences': 'Cmd+Comma',
            'close': 'Cmd+W',
            'minimize': 'Cmd+M',
            'copy': 'Cmd+C',
            'paste': 'Cmd+V',
            'select_all': 'Cmd+A'
        },
        LINUX: {
            'fullscreen': 'F11',
            'quit': 'Ctrl+Q',
            'preferences': 'Ctrl+P',
            'close': 'Ctrl+W',
            'minimize': 'Ctrl+M',
            'copy': 'Ctrl+C',
            'paste': 'Ctrl+V',
            'select_all': 'Ctrl+A'
        }
    }
    
    @classmethod
    def get_platform(cls) -> str:
        """Get the current platform name"""
        return platform.system()
    
    @classmethod
    def is_windows(cls) -> bool:
        """Check if running on Windows"""
        return cls.get_platform() == cls.WINDOWS
    
    @classmethod
    def is_macos(cls) -> bool:
        """Check if running on macOS"""
        return cls.get_platform() == cls.MACOS
    
    @classmethod
    def is_linux(cls) -> bool:
        """Check if running on Linux"""
        return cls.get_platform() == cls.LINUX
    
    @classmethod
    def setup_dpi_awareness(cls) -> bool:
        """
        Setup DPI awareness for high-resolution displays
        Returns True if successful, False otherwise
        """
        try:
            if cls.is_windows():
                return cls._setup_windows_dpi()
            elif cls.is_macos():
                return cls._setup_macos_dpi()
            elif cls.is_linux():
                return cls._setup_linux_dpi()
            else:
                _LOGGER.warning(f"Unknown platform: {cls.get_platform()}")
                return False
        except Exception as e:
            _LOGGER.warning(f"DPI awareness setup failed: {e}")
            return False
    
    @classmethod
    def _setup_windows_dpi(cls) -> bool:
        """Setup Windows-specific DPI awareness"""
        try:
            import ctypes
            from ctypes import windll
            
            # Try newest API first (Windows 10 1703+)
            try:
                windll.shcore.SetProcessDpiAwarenessContext(-4)  # DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2
                _LOGGER.debug("✅ Windows DPI awareness: Per-monitor V2")
                return True
            except Exception:
                pass
            
            # Fallback to older API (Windows 8.1+)
            try:
                windll.shcore.SetProcessDpiAwareness(2)  # PROCESS_PER_MONITOR_DPI_AWARE
                _LOGGER.debug("✅ Windows DPI awareness: Per-monitor V1")
                return True
            except Exception:
                pass
            
            # Last resort (Windows Vista+)
            try:
                windll.user32.SetProcessDPIAware()
                _LOGGER.debug("✅ Windows DPI awareness: Basic")
                return True
            except Exception:
                pass
            
            _LOGGER.warning("⚠️ Could not set Windows DPI awareness")
            return False
            
        except ImportError:
            _LOGGER.warning("⚠️ Windows DPI libraries not available")
            return False
    
    @classmethod
    def _setup_macos_dpi(cls) -> bool:
        """Setup macOS-specific display handling"""
        try:
            # macOS handles retina displays automatically through the system
            # We just need to ensure proper scaling
            _LOGGER.debug("✅ macOS display handling: Automatic retina support")
            return True
        except Exception as e:
            _LOGGER.warning(f"⚠️ macOS display setup failed: {e}")
            return False
    
    @classmethod
    def _setup_linux_dpi(cls) -> bool:
        """Setup Linux-specific display handling"""
        try:
            # Linux DPI handling varies by desktop environment
            # Set environment variables for better scaling
            scale_factor = os.environ.get('GDK_SCALE', '1')
            _LOGGER.debug(f"✅ Linux display handling: GDK_SCALE={scale_factor}")
            return True
        except Exception as e:
            _LOGGER.warning(f"⚠️ Linux display setup failed: {e}")
            return False
    
    @classmethod
    def setup_window_properties(cls, window: tk.Tk) -> None:
        """Setup cross-platform window properties"""
        try:
            # Basic window properties
            window.resizable(True, True)
            window.minsize(800, 600)
            
            # Platform-specific window setup
            if cls.is_windows():
                cls._setup_windows_window(window)
            elif cls.is_macos():
                cls._setup_macos_window(window)
            elif cls.is_linux():
                cls._setup_linux_window(window)
            
            _LOGGER.debug("✅ Window properties configured")
            
        except Exception as e:
            _LOGGER.error(f"❌ Error setting up window properties: {e}")
    
    @classmethod
    def _setup_windows_window(cls, window: tk.Tk) -> None:
        """Setup Windows-specific window properties"""
        try:
            # Disable automatic DPI scaling for better control
            window.tk.call('tk', 'scaling', 1.0)
            window.wm_attributes('-alpha', 1.0)
            _LOGGER.debug("✅ Windows window properties set")
        except Exception as e:
            _LOGGER.warning(f"⚠️ Windows window setup failed: {e}")
    
    @classmethod
    def _setup_macos_window(cls, window: tk.Tk) -> None:
        """Setup macOS-specific window properties"""
        try:
            # macOS-specific window attributes
            window.createcommand('tk::mac::ShowPreferences', lambda: None)
            _LOGGER.debug("✅ macOS window properties set")
        except Exception as e:
            _LOGGER.warning(f"⚠️ macOS window setup failed: {e}")
    
    @classmethod
    def _setup_linux_window(cls, window: tk.Tk) -> None:
        """Setup Linux-specific window properties"""
        try:
            # Linux window manager hints
            window.wm_attributes('-type', 'normal')
            _LOGGER.debug("✅ Linux window properties set")
        except Exception as e:
            _LOGGER.warning(f"⚠️ Linux window setup failed: {e}")
    
    @classmethod
    def setup_fullscreen(cls, window: tk.Tk, enable: bool = True) -> bool:
        """
        Setup fullscreen mode in a cross-platform way
        Returns True if successful
        """
        try:
            if cls.is_macos():
                # macOS has special fullscreen behavior
                if enable:
                    window.attributes('-fullscreen', True)
                    window.attributes('-zoomed', True)  # Also maximize
                else:
                    window.attributes('-fullscreen', False)
                    window.attributes('-zoomed', False)
            else:
                # Windows and Linux standard approach
                window.attributes('-fullscreen', enable)
            
            _LOGGER.debug(f"✅ Fullscreen {'enabled' if enable else 'disabled'}")
            return True
            
        except Exception as e:
            _LOGGER.warning(f"⚠️ Fullscreen setup failed: {e}")
            return False
    
    @classmethod
    def toggle_fullscreen(cls, window: tk.Tk) -> bool:
        """Toggle fullscreen mode"""
        try:
            current_state = window.attributes('-fullscreen')
            return cls.setup_fullscreen(window, not current_state)
        except Exception as e:
            _LOGGER.warning(f"⚠️ Fullscreen toggle failed: {e}")
            return False
    
    @classmethod
    def setup_window_theme(cls, window: tk.Tk, dark_mode: bool = False) -> None:
        """Setup platform-specific window theming - light mode only"""
        try:
            if cls.is_windows():
                cls._setup_windows_theme(window)
            elif cls.is_macos():
                cls._setup_macos_theme(window)
            elif cls.is_linux():
                cls._setup_linux_theme(window)
                
            _LOGGER.debug(f"✅ Window theme configured (light mode)")
            
        except Exception as e:
            _LOGGER.warning(f"⚠️ Window theme setup failed: {e}")
    
    @classmethod
    def _setup_windows_theme(cls, window: tk.Tk) -> None:
        """Setup Windows-specific theming - light mode"""
        try:
            import ctypes
            from ctypes import windll
            
            # Windows 10+ light mode title bar
            window_id = windll.user32.GetParent(window.winfo_id())
            windll.dwmapi.DwmSetWindowAttribute(
                window_id, 
                20,  # DWMWA_USE_IMMERSIVE_DARK_MODE
                ctypes.byref(ctypes.c_int(0)),  # Always light mode (0)
                ctypes.sizeof(ctypes.c_int)
            )
            _LOGGER.debug("✅ Windows title bar theme set to light mode")
            
        except Exception as e:
            _LOGGER.debug(f"Windows theme setup failed (not critical): {e}")
    
    @classmethod
    def _setup_macos_theme(cls, window: tk.Tk) -> None:
        """Setup macOS-specific theming - light mode"""
        try:
            # macOS automatically handles system theme
            _LOGGER.debug("✅ macOS theme handled by system")
        except Exception as e:
            _LOGGER.debug(f"macOS theme setup failed (not critical): {e}")
    
    @classmethod
    def _setup_linux_theme(cls, window: tk.Tk) -> None:
        """Setup Linux-specific theming - light mode"""
        try:
            # Linux theming depends on desktop environment
            _LOGGER.debug("✅ Linux theme handled by desktop environment")
        except Exception as e:
            _LOGGER.debug(f"Linux theme setup failed (not critical): {e}")
    
    @classmethod
    def get_platform_icon_path(cls, icon_name: str, icons_dir: str) -> Optional[str]:
        """
        Get platform-appropriate icon path
        
        Args:
            icon_name: Base name of icon (without extension)
            icons_dir: Directory containing icons
            
        Returns:
            Path to appropriate icon file or None if not found
        """
        extensions = []
        
        if cls.is_windows():
            extensions = ['.ico', '.png']
        elif cls.is_macos():
            extensions = ['.icns', '.png']
        else:  # Linux
            extensions = ['.png', '.svg', '.xpm']
        
        for ext in extensions:
            icon_path = os.path.join(icons_dir, f"{icon_name}{ext}")
            if os.path.exists(icon_path):
                _LOGGER.debug(f"✅ Found icon: {icon_path}")
                return icon_path
        
        _LOGGER.warning(f"⚠️ No suitable icon found for {icon_name}")
        return None
    
    @classmethod
    def set_window_icon(cls, window: tk.Tk, icon_name: str = 'icon') -> bool:
        """Set window icon using platform-appropriate format"""
        try:
            # Find icons directory
            current_dir = Path(__file__).parent
            project_root = current_dir.parent.parent.parent
            icons_dir = project_root / 'images'
            
            icon_path = cls.get_platform_icon_path(icon_name, str(icons_dir))
            
            if icon_path:
                if cls.is_windows() and icon_path.endswith('.ico'):
                    window.iconbitmap(icon_path)
                else:
                    # Use PhotoImage for other platforms/formats
                    icon = tk.PhotoImage(file=icon_path)
                    window.iconphoto(True, icon)
                
                _LOGGER.debug(f"✅ Window icon set: {icon_path}")
                return True
            else:
                _LOGGER.warning("⚠️ No suitable icon found")
                return False
                
        except Exception as e:
            _LOGGER.warning(f"⚠️ Failed to set window icon: {e}")
            return False
    
    @classmethod
    def get_platform_font(cls, font_type: str = 'default') -> Tuple[str, int, str]:
        """
        Get appropriate font for current platform
        
        Args:
            font_type: Type of font ('default', 'title', 'small', 'code')
            
        Returns:
            Tuple of (font_family, size, style)
        """
        platform_name = cls.get_platform()
        fonts = cls.PLATFORM_FONTS.get(platform_name, cls.PLATFORM_FONTS[cls.LINUX])
        return fonts.get(font_type, fonts['default'])
    
    @classmethod
    def get_keyboard_shortcuts(cls) -> Dict[str, str]:
        """Get platform-appropriate keyboard shortcuts"""
        platform_name = cls.get_platform()
        return cls.PLATFORM_SHORTCUTS.get(platform_name, cls.PLATFORM_SHORTCUTS[cls.LINUX])
    
    @classmethod
    def center_window(cls, window: tk.Tk, width: Optional[int] = None, height: Optional[int] = None) -> None:
        """Center window on screen with proper error handling"""
        try:
            window.update_idletasks()
            
            # Get window dimensions
            if width is None:
                width = window.winfo_width()
            if height is None:
                height = window.winfo_height()
            
            # Get screen dimensions
            screen_width = window.winfo_screenwidth()
            screen_height = window.winfo_screenheight()
            
            # Calculate center position
            x = (screen_width // 2) - (width // 2)
            y = (screen_height // 2) - (height // 2)
            
            # Ensure window stays on screen
            x = max(0, min(x, screen_width - width))
            y = max(0, min(y, screen_height - height))
            
            window.geometry(f"{width}x{height}+{x}+{y}")
            _LOGGER.debug(f"✅ Window centered at {x},{y} (size: {width}x{height})")
            
        except Exception as e:
            _LOGGER.warning(f"⚠️ Could not center window: {e}")
    
    @classmethod
    def bind_platform_shortcuts(cls, window: tk.Tk, callbacks: Dict[str, Any]) -> None:
        """Bind platform-appropriate keyboard shortcuts"""
        try:
            shortcuts = cls.get_keyboard_shortcuts()
            
            for action, callback in callbacks.items():
                if action in shortcuts and callback:
                    window.bind_all(f"<{shortcuts[action]}>", callback)
                    _LOGGER.debug(f"✅ Bound {action}: {shortcuts[action]}")
            
        except Exception as e:
            _LOGGER.warning(f"⚠️ Failed to bind shortcuts: {e}")
    
    @classmethod 
    def get_config_directory(cls, app_name: str = 'SNID_SAGE') -> str:
        """Get platform-appropriate configuration directory"""
        try:
            if cls.is_windows():
                config_dir = os.path.join(os.environ.get('APPDATA', ''), app_name)
            elif cls.is_macos():
                config_dir = os.path.expanduser(f'~/Library/Application Support/{app_name}')
            else:  # Linux
                config_dir = os.path.expanduser(f'~/.config/{app_name.lower()}')
            
            # Create directory if it doesn't exist
            os.makedirs(config_dir, exist_ok=True)
            _LOGGER.debug(f"✅ Config directory: {config_dir}")
            return config_dir
            
        except Exception as e:
            _LOGGER.warning(f"⚠️ Failed to get config directory: {e}")
            # Fallback to current directory
            return os.getcwd()
    
    @classmethod
    def handle_window_close(cls, window: tk.Tk, cleanup_callback: Optional[Any] = None) -> None:
        """Handle window close event with proper cleanup"""
        try:
            _LOGGER.info("🛑 Shutting down application...")
            
            if cleanup_callback:
                cleanup_callback()
            
            # Close any matplotlib figures
            try:
                import matplotlib.pyplot as plt
                plt.close('all')
            except:
                pass
            
            # Destroy window
            window.quit()
            window.destroy()
            
            _LOGGER.info("✅ Application shutdown complete")
            
        except Exception as e:
            _LOGGER.warning(f"⚠️ Error during window close: {e}")
            # Force exit if normal cleanup fails
            sys.exit(0)


# Convenience functions for backward compatibility
def setup_dpi_awareness() -> bool:
    """Convenience function for DPI setup"""
    return CrossPlatformWindowManager.setup_dpi_awareness()

def get_platform_font(font_type: str = 'default') -> Tuple[str, int, str]:
    """Convenience function for font selection"""
    return CrossPlatformWindowManager.get_platform_font(font_type)

def get_config_directory(app_name: str = 'SNID_SAGE') -> str:
    """Convenience function for config directory"""
    return CrossPlatformWindowManager.get_config_directory(app_name)

def center_window(window: tk.Tk, width: Optional[int] = None, height: Optional[int] = None) -> None:
    """Convenience function for window centering"""
    return CrossPlatformWindowManager.center_window(window, width, height) 
