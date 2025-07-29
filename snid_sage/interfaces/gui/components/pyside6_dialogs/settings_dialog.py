"""
PySide6 Settings Dialog for SNID SAGE GUI
=========================================

This module provides a PySide6 dialog for GUI settings and preferences,
matching the functionality of the Tkinter version.

Features:
- Font size and display options
- Theme preferences  
- Window resolution and DPI settings
- Plot display preferences
- Interface customization options
"""

import platform
from typing import Optional, Dict, Any, List, Callable
import PySide6.QtWidgets as QtWidgets
import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui

# Import logging
try:
    from snid_sage.shared.utils.logging import get_logger
    _LOGGER = get_logger('gui.pyside6_settings_dialog')
except ImportError:
    import logging
    _LOGGER = logging.getLogger('gui.pyside6_settings_dialog')


class PySide6SettingsDialog(QtWidgets.QDialog):
    """PySide6 dialog for comprehensive GUI settings"""
    
    def __init__(self, parent=None, current_settings=None):
        """Initialize settings dialog"""
        super().__init__(parent)
        
        self.parent_gui = parent
        self.settings = current_settings or {}
        self.result = None
        
        # Settings widgets storage
        self.widgets = {}
        self.font_samples = {}
        
        # Available fonts (filtered for readability)
        self.available_fonts = self._get_available_fonts()
        
        # Color scheme
        self.colors = self._get_theme_colors()
        
        # Settings change callbacks
        self.settings_changed_callbacks: List[Callable[[Dict[str, Any]], None]] = []
        
        self.setup_ui()
    
    def _get_available_fonts(self) -> List[str]:
        """Get available system fonts filtered for readability"""
        # Get system fonts
        font_database = QtGui.QFontDatabase()
        all_fonts = font_database.families()
        
        # Priority fonts for different platforms
        preferred_fonts = []
        
        if platform.system() == "Windows":
            preferred_fonts = ["Segoe UI", "Calibri", "Arial", "Verdana", "Tahoma"]
        elif platform.system() == "Darwin":  # macOS
            preferred_fonts = ["SF Pro Display", "Helvetica Neue", "Arial", "Verdana"]
        else:  # Linux
            preferred_fonts = ["Ubuntu", "DejaVu Sans", "Liberation Sans", "Arial", "Verdana"]
        
        # Add common programming fonts
        programming_fonts = ["Consolas", "Monaco", "Courier New", "Menlo", "Source Code Pro"]
        
        # Combine and filter available fonts
        priority_fonts = preferred_fonts + programming_fonts
        available_fonts = []
        
        # Add priority fonts that are available
        for font in priority_fonts:
            if font in all_fonts:
                available_fonts.append(font)
        
        # Add other common fonts
        common_fonts = ["Arial", "Helvetica", "Times New Roman", "Georgia", "Trebuchet MS"]
        for font in common_fonts:
            if font in all_fonts and font not in available_fonts:
                available_fonts.append(font)
        
        return available_fonts[:20]  # Limit to 20 fonts
    
    def _get_theme_colors(self) -> Dict[str, str]:
        """Get theme colors from parent or use defaults"""
        if hasattr(self.parent_gui, 'theme_colors'):
            return self.parent_gui.theme_colors
        else:
            # Default theme colors
            return {
                'bg_primary': '#f8fafc',
                'bg_secondary': '#ffffff',
                'bg_tertiary': '#f1f5f9',
                'text_primary': '#1e293b',
                'text_secondary': '#475569',
                'border': '#cbd5e1',
                'accent_primary': '#3b82f6',
                'btn_primary': '#3b82f6',
                'btn_success': '#10b981',
                'btn_warning': '#f59e0b',
                'btn_danger': '#ef4444'
            }
    
    def setup_ui(self):
        """Setup the dialog UI"""
        self.setWindowTitle("⚙️ SNID SAGE Settings")
        self.setMinimumSize(1000, 700)
        self.resize(1200, 800)
        self.setModal(True)
        
        # Apply colors
        self.setStyleSheet(f"""
            QDialog {{
                background: {self.colors['bg_primary']};
                color: {self.colors['text_primary']};
            }}
            QGroupBox {{
                font-weight: bold;
                border: 2px solid {self.colors['border']};
                border-radius: 6px;
                margin-top: 8px;
                padding-top: 12px;
                background: {self.colors['bg_secondary']};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px;
                background: {self.colors['bg_secondary']};
            }}
        """)
        
        # Main layout
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(15)
        
        # Header
        self._create_header(main_layout)
        
        # Tabbed content
        self._create_tabbed_content(main_layout)
        
        # Footer buttons
        self._create_footer_buttons(main_layout)
        
        # Load current values
        self._load_current_values()
        
        _LOGGER.debug("PySide6 Settings dialog created")
    
    def _create_header(self, layout):
        """Create header section"""
        header_frame = QtWidgets.QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background: {self.colors['bg_secondary']};
                border: 1px solid {self.colors['border']};
                border-radius: 6px;
                padding: 12px;
            }}
        """)
        
        header_layout = QtWidgets.QVBoxLayout(header_frame)
        
        title_label = QtWidgets.QLabel("⚙️ GUI Settings & Preferences")
        title_label.setStyleSheet(f"""
            font-size: 18px;
            font-weight: bold;
            color: {self.colors['text_primary']};
            background: transparent;
            border: none;
        """)
        header_layout.addWidget(title_label)
        
        subtitle_label = QtWidgets.QLabel("Customize the appearance and behavior of SNID SAGE")
        subtitle_label.setStyleSheet(f"""
            font-size: 12px;
            color: {self.colors['text_secondary']};
            background: transparent;
            border: none;
        """)
        header_layout.addWidget(subtitle_label)
        
        layout.addWidget(header_frame)
    
    def _create_tabbed_content(self, layout):
        """Create tabbed content for different settings categories"""
        tab_widget = QtWidgets.QTabWidget()
        tab_widget.setStyleSheet(f"""
            QTabWidget::pane {{
                border: 1px solid {self.colors['border']};
                background: {self.colors['bg_secondary']};
            }}
            QTabBar::tab {{
                background: {self.colors['bg_tertiary']};
                color: {self.colors['text_primary']};
                padding: 8px 16px;
                margin-right: 2px;
                border: 1px solid {self.colors['border']};
                border-bottom: none;
            }}
            QTabBar::tab:selected {{
                background: {self.colors['bg_secondary']};
                color: {self.colors['accent_primary']};
                font-weight: bold;
            }}
        """)
        
        # Create tabs
        self._create_appearance_tab(tab_widget)
        self._create_display_tab(tab_widget)
        self._create_ai_tab(tab_widget)
        self._create_behavior_tab(tab_widget)
        self._create_advanced_tab(tab_widget)
        
        layout.addWidget(tab_widget, 1)
    
    def _create_appearance_tab(self, tab_widget):
        """Create appearance settings tab"""
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)
        
        # Font settings group
        font_group = QtWidgets.QGroupBox("Font & Typography")
        font_layout = QtWidgets.QGridLayout(font_group)
        
        # Font family
        font_layout.addWidget(QtWidgets.QLabel("Font Family:"), 0, 0)
        self.widgets['font_family'] = QtWidgets.QComboBox()
        self.widgets['font_family'].addItems(self.available_fonts)
        self.widgets['font_family'].currentTextChanged.connect(self._update_font_preview)
        font_layout.addWidget(self.widgets['font_family'], 0, 1)
        
        # Font size
        font_layout.addWidget(QtWidgets.QLabel("Font Size:"), 1, 0)
        self.widgets['font_size'] = QtWidgets.QSpinBox()
        self.widgets['font_size'].setRange(8, 24)
        self.widgets['font_size'].setValue(10)
        self.widgets['font_size'].valueChanged.connect(self._update_font_preview)
        font_layout.addWidget(self.widgets['font_size'], 1, 1)
        
        # Font preview
        font_layout.addWidget(QtWidgets.QLabel("Preview:"), 2, 0)
        self.font_samples['main'] = QtWidgets.QLabel("The quick brown fox jumps over the lazy dog 0123456789")
        self.font_samples['main'].setStyleSheet(f"border: 1px solid {self.colors['border']}; padding: 8px;")
        font_layout.addWidget(self.font_samples['main'], 2, 1)
        
        layout.addWidget(font_group)
        
        # Theme settings group  
        theme_group = QtWidgets.QGroupBox("Theme & Colors")
        theme_layout = QtWidgets.QGridLayout(theme_group)
        
        # Theme selection
        theme_layout.addWidget(QtWidgets.QLabel("Theme:"), 0, 0)
        self.widgets['theme'] = QtWidgets.QComboBox()
        self.widgets['theme'].addItems(["Light", "Dark", "Auto (System)"])
        theme_layout.addWidget(self.widgets['theme'], 0, 1)
        
        # Accent color
        theme_layout.addWidget(QtWidgets.QLabel("Accent Color:"), 1, 0)
        self.widgets['accent_color'] = QtWidgets.QComboBox()
        self.widgets['accent_color'].addItems(["Blue", "Purple", "Green", "Orange", "Red"])
        theme_layout.addWidget(self.widgets['accent_color'], 1, 1)
        
        layout.addWidget(theme_group)
        
        layout.addStretch()
        tab_widget.addTab(tab, "🎨 Appearance")
    
    def _create_display_tab(self, tab_widget):
        """Create display settings tab"""
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)
        
        # Window settings group
        window_group = QtWidgets.QGroupBox("Window & Display")
        window_layout = QtWidgets.QGridLayout(window_group)
        
        # Window size
        window_layout.addWidget(QtWidgets.QLabel("Default Window Size:"), 0, 0)
        size_widget = QtWidgets.QWidget()
        size_layout = QtWidgets.QHBoxLayout(size_widget)
        size_layout.setContentsMargins(0, 0, 0, 0)
        
        self.widgets['window_width'] = QtWidgets.QSpinBox()
        self.widgets['window_width'].setRange(800, 3840)
        self.widgets['window_width'].setValue(1200)
        size_layout.addWidget(self.widgets['window_width'])
        
        size_layout.addWidget(QtWidgets.QLabel("×"))
        
        self.widgets['window_height'] = QtWidgets.QSpinBox()
        self.widgets['window_height'].setRange(600, 2160)
        self.widgets['window_height'].setValue(800)
        size_layout.addWidget(self.widgets['window_height'])
        
        size_layout.addStretch()
        window_layout.addWidget(size_widget, 0, 1)
        
        # DPI scaling
        window_layout.addWidget(QtWidgets.QLabel("DPI Scaling:"), 1, 0)
        self.widgets['dpi_scaling'] = QtWidgets.QComboBox()
        self.widgets['dpi_scaling'].addItems(["Auto", "100%", "125%", "150%", "175%", "200%"])
        window_layout.addWidget(self.widgets['dpi_scaling'], 1, 1)
        
        # Remember window position
        self.widgets['remember_position'] = QtWidgets.QCheckBox("Remember window position on exit")
        window_layout.addWidget(self.widgets['remember_position'], 2, 0, 1, 2)
        
        layout.addWidget(window_group)
        
        # Plot settings group
        plot_group = QtWidgets.QGroupBox("Plot Display")
        plot_layout = QtWidgets.QGridLayout(plot_group)
        
        # Anti-aliasing
        self.widgets['plot_antialiasing'] = QtWidgets.QCheckBox("Enable plot anti-aliasing")
        plot_layout.addWidget(self.widgets['plot_antialiasing'], 0, 0, 1, 2)
        
        # Default plot size
        plot_layout.addWidget(QtWidgets.QLabel("Default Plot Resolution:"), 2, 0)
        self.widgets['plot_dpi'] = QtWidgets.QSpinBox()
        self.widgets['plot_dpi'].setRange(72, 300)
        self.widgets['plot_dpi'].setValue(100)
        self.widgets['plot_dpi'].setSuffix(" DPI")
        plot_layout.addWidget(self.widgets['plot_dpi'], 2, 1)
        
        layout.addWidget(plot_group)
        
        layout.addStretch()
        tab_widget.addTab(tab, "🖥️ Display")
    
    def _create_ai_tab(self, tab_widget):
        """Create AI configuration tab"""
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)
        
        # OpenRouter API configuration group
        api_group = QtWidgets.QGroupBox("🔑 OpenRouter API Configuration")
        api_layout = QtWidgets.QVBoxLayout(api_group)
        api_layout.setSpacing(12)
        
        # Information label
        info_label = QtWidgets.QLabel(
            "Configure your OpenRouter API key to enable AI-powered analysis features.\n"
            "Get your free API key at: https://openrouter.ai"
        )
        info_label.setStyleSheet(f"""
            color: {self.colors['text_secondary']};
            font-style: italic;
            padding: 8px;
            background: {self.colors['bg_tertiary']};
            border-radius: 4px;
        """)
        info_label.setWordWrap(True)
        api_layout.addWidget(info_label)
        
        # API Key input
        key_layout = QtWidgets.QHBoxLayout()
        key_layout.addWidget(QtWidgets.QLabel("API Key:"))
        
        self.widgets['openrouter_api_key'] = QtWidgets.QLineEdit()
        self.widgets['openrouter_api_key'].setEchoMode(QtWidgets.QLineEdit.Password)
        self.widgets['openrouter_api_key'].setPlaceholderText("Enter your OpenRouter API key")
        key_layout.addWidget(self.widgets['openrouter_api_key'])
        
        # Show/hide API key button
        self.show_key_btn = QtWidgets.QPushButton("Show")
        self.show_key_btn.setMaximumWidth(60)
        self.show_key_btn.clicked.connect(self._toggle_api_key_visibility)
        key_layout.addWidget(self.show_key_btn)
        
        api_layout.addLayout(key_layout)
        
        # Test connection button
        test_layout = QtWidgets.QHBoxLayout()
        self.test_connection_btn = QtWidgets.QPushButton("🔍 Test Connection")
        self.test_connection_btn.clicked.connect(self._test_openrouter_connection)
        test_layout.addWidget(self.test_connection_btn)
        
        self.connection_status_label = QtWidgets.QLabel("Not tested")
        self.connection_status_label.setStyleSheet(f"color: {self.colors['text_secondary']};")
        test_layout.addWidget(self.connection_status_label)
        test_layout.addStretch()
        
        api_layout.addLayout(test_layout)
        layout.addWidget(api_group)
        
        # Model selection group
        model_group = QtWidgets.QGroupBox("🤖 Favorite Free Model")
        model_layout = QtWidgets.QVBoxLayout(model_group)
        model_layout.setSpacing(12)
        
        # Model selection info
        model_info_label = QtWidgets.QLabel(
            "Choose your preferred free model for AI analysis. "
            "Click 'Fetch Free Models' to see available options."
        )
        model_info_label.setStyleSheet(f"color: {self.colors['text_secondary']}; font-style: italic;")
        model_info_label.setWordWrap(True)
        model_layout.addWidget(model_info_label)
        
        # Model selection controls
        model_controls_layout = QtWidgets.QHBoxLayout()
        
        self.fetch_models_btn = QtWidgets.QPushButton("📡 Fetch Free Models")
        self.fetch_models_btn.clicked.connect(self._fetch_free_models)
        model_controls_layout.addWidget(self.fetch_models_btn)
        
        self.model_status_label = QtWidgets.QLabel("No models loaded")
        self.model_status_label.setStyleSheet(f"color: {self.colors['text_secondary']};")
        model_controls_layout.addWidget(self.model_status_label)
        model_controls_layout.addStretch()
        
        model_layout.addLayout(model_controls_layout)
        
        # Model list
        self.widgets['favorite_model'] = QtWidgets.QListWidget()
        self.widgets['favorite_model'].setMaximumHeight(200)
        self.widgets['favorite_model'].setStyleSheet(f"""
            QListWidget {{
                background: {self.colors['bg_secondary']};
                border: 1px solid {self.colors['border']};
                border-radius: 4px;
                font-family: 'Consolas', monospace;
                font-size: 9pt;
            }}
            QListWidget::item {{
                padding: 4px 8px;
                border-bottom: 1px solid {self.colors['bg_tertiary']};
            }}
            QListWidget::item:selected {{
                background: {self.colors['btn_primary']};
                color: white;
            }}
        """)
        model_layout.addWidget(self.widgets['favorite_model'])
        
        layout.addWidget(model_group)
        
        # AI preferences group
        prefs_group = QtWidgets.QGroupBox("⚙️ AI Preferences")
        prefs_layout = QtWidgets.QFormLayout(prefs_group)
        
        # Temperature setting
        self.widgets['ai_temperature'] = QtWidgets.QDoubleSpinBox()
        self.widgets['ai_temperature'].setRange(0.0, 2.0)
        self.widgets['ai_temperature'].setSingleStep(0.1)
        self.widgets['ai_temperature'].setValue(0.7)
        self.widgets['ai_temperature'].setDecimals(1)
        prefs_layout.addRow("Temperature:", self.widgets['ai_temperature'])
        
        # Max tokens setting
        self.widgets['ai_max_tokens'] = QtWidgets.QSpinBox()
        self.widgets['ai_max_tokens'].setRange(100, 4000)
        self.widgets['ai_max_tokens'].setValue(2000)
        prefs_layout.addRow("Max Tokens:", self.widgets['ai_max_tokens'])
        
        # Checkboxes
        self.widgets['ai_verbose'] = QtWidgets.QCheckBox("Use verbose explanations")
        self.widgets['ai_verbose'].setChecked(True)
        prefs_layout.addRow("", self.widgets['ai_verbose'])
        
        self.widgets['ai_references'] = QtWidgets.QCheckBox("Include scientific references")
        self.widgets['ai_references'].setChecked(True)
        prefs_layout.addRow("", self.widgets['ai_references'])
        
        layout.addWidget(prefs_group)
        
        layout.addStretch()
        tab_widget.addTab(tab, "🤖 AI Assistant")
    
    def _create_behavior_tab(self, tab_widget):
        """Create behavior settings tab"""
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)
        
        # General behavior group
        general_group = QtWidgets.QGroupBox("General Behavior")
        general_layout = QtWidgets.QGridLayout(general_group)
        
        # Auto-save settings
        self.widgets['auto_save_settings'] = QtWidgets.QCheckBox("Auto-save settings on exit")
        general_layout.addWidget(self.widgets['auto_save_settings'], 0, 0, 1, 2)
        
        # Confirm before exit
        self.widgets['confirm_exit'] = QtWidgets.QCheckBox("Confirm before exiting application")
        general_layout.addWidget(self.widgets['confirm_exit'], 1, 0, 1, 2)
        
        # Show splash screen
        self.widgets['show_splash'] = QtWidgets.QCheckBox("Show splash screen on startup")
        general_layout.addWidget(self.widgets['show_splash'], 2, 0, 1, 2)
        
        layout.addWidget(general_group)
        
        # Analysis settings group
        analysis_group = QtWidgets.QGroupBox("Analysis Behavior")
        analysis_layout = QtWidgets.QGridLayout(analysis_group)
        
        # Auto-run after load
        self.widgets['auto_preprocess'] = QtWidgets.QCheckBox("Auto-preprocess loaded spectra")
        analysis_layout.addWidget(self.widgets['auto_preprocess'], 0, 0, 1, 2)
        
        # Show progress dialogs
        self.widgets['show_progress'] = QtWidgets.QCheckBox("Show progress dialogs during analysis")
        analysis_layout.addWidget(self.widgets['show_progress'], 1, 0, 1, 2)
        
        # Max templates to display
        analysis_layout.addWidget(QtWidgets.QLabel("Max templates to display:"), 2, 0)
        self.widgets['max_templates'] = QtWidgets.QSpinBox()
        self.widgets['max_templates'].setRange(5, 50)
        self.widgets['max_templates'].setValue(10)
        analysis_layout.addWidget(self.widgets['max_templates'], 2, 1)
        
        layout.addWidget(analysis_group)
        
        layout.addStretch()
        tab_widget.addTab(tab, "⚡ Behavior")
    
    def _create_advanced_tab(self, tab_widget):
        """Create advanced settings tab"""
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tab)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(20)
        
        # Performance group
        performance_group = QtWidgets.QGroupBox("Performance")
        performance_layout = QtWidgets.QGridLayout(performance_group)
        
        # Thread count
        performance_layout.addWidget(QtWidgets.QLabel("Analysis Threads:"), 0, 0)
        self.widgets['thread_count'] = QtWidgets.QSpinBox()
        self.widgets['thread_count'].setRange(1, 16)
        self.widgets['thread_count'].setValue(4)
        performance_layout.addWidget(self.widgets['thread_count'], 0, 1)
        
        # Memory limit
        performance_layout.addWidget(QtWidgets.QLabel("Memory Limit (GB):"), 1, 0)
        self.widgets['memory_limit'] = QtWidgets.QDoubleSpinBox()
        self.widgets['memory_limit'].setRange(1.0, 64.0)
        self.widgets['memory_limit'].setValue(8.0)
        self.widgets['memory_limit'].setSuffix(" GB")
        performance_layout.addWidget(self.widgets['memory_limit'], 1, 1)
        
        layout.addWidget(performance_group)
        
        # Debug group
        debug_group = QtWidgets.QGroupBox("Debug & Logging")
        debug_layout = QtWidgets.QGridLayout(debug_group)
        
        # Log level
        debug_layout.addWidget(QtWidgets.QLabel("Log Level:"), 0, 0)
        self.widgets['log_level'] = QtWidgets.QComboBox()
        self.widgets['log_level'].addItems(["ERROR", "WARNING", "INFO", "DEBUG"])
        debug_layout.addWidget(self.widgets['log_level'], 0, 1)
        
        # Enable debug mode
        self.widgets['debug_mode'] = QtWidgets.QCheckBox("Enable debug mode")
        debug_layout.addWidget(self.widgets['debug_mode'], 1, 0, 1, 2)
        
        layout.addWidget(debug_group)
        
        # Reset section
        reset_group = QtWidgets.QGroupBox("Reset Options")
        reset_layout = QtWidgets.QVBoxLayout(reset_group)
        
        reset_button = QtWidgets.QPushButton("🔄 Reset All Settings to Defaults")
        reset_button.setStyleSheet(f"""
            QPushButton {{
                background: {self.colors['btn_warning']};
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }}
            QPushButton:hover {{
                background: {self._darken_color(self.colors['btn_warning'])};
            }}
        """)
        reset_button.clicked.connect(self._reset_to_defaults)
        reset_layout.addWidget(reset_button)
        
        layout.addWidget(reset_group)
        
        layout.addStretch()
        tab_widget.addTab(tab, "Advanced")
    
    def _create_footer_buttons(self, layout):
        """Create footer button section"""
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.setSpacing(10)
        
        # Apply button
        apply_btn = QtWidgets.QPushButton("Apply")
        apply_btn.setStyleSheet(f"""
            QPushButton {{
                background: {self.colors['btn_success']};
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background: {self._darken_color(self.colors['btn_success'])};
            }}
        """)
        apply_btn.clicked.connect(self._apply_settings)
        
        # OK button
        ok_btn = QtWidgets.QPushButton("OK")
        ok_btn.setStyleSheet(f"""
            QPushButton {{
                background: {self.colors['btn_primary']};
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background: {self._darken_color(self.colors['btn_primary'])};
            }}
        """)
        ok_btn.clicked.connect(self._ok_clicked)
        ok_btn.setDefault(True)
        
        # Cancel button
        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.setStyleSheet(f"""
            QPushButton {{
                background: {self.colors['text_secondary']};
                color: white;
                border: none;
                padding: 8px 20px;
                border-radius: 4px;
                font-weight: bold;
                min-width: 80px;
            }}
            QPushButton:hover {{
                background: {self._darken_color(self.colors['text_secondary'])};
            }}
        """)
        cancel_btn.clicked.connect(self.reject)
        
        button_layout.addStretch()
        button_layout.addWidget(apply_btn)
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        
        layout.addLayout(button_layout)
    
    def _update_font_preview(self):
        """Update font preview"""
        if 'main' in self.font_samples:
            font_family = self.widgets['font_family'].currentText()
            font_size = self.widgets['font_size'].value()
            
            font = QtGui.QFont(font_family, font_size)
            self.font_samples['main'].setFont(font)
    
    def _darken_color(self, color: str) -> str:
        """Darken a hex color"""
        if color.startswith('#') and len(color) == 7:
            try:
                r = int(color[1:3], 16)
                g = int(color[3:5], 16)
                b = int(color[5:7], 16)
                
                r = max(0, r - 30)
                g = max(0, g - 30)
                b = max(0, b - 30)
                
                return f"#{r:02x}{g:02x}{b:02x}"
            except:
                pass
        return color
    
    def _load_current_values(self):
        """Load current settings values into widgets"""
        # Set default values or load from settings
        defaults = {
            'font_family': 'Arial',
            'font_size': 10,
            'theme': 'Light',
            'accent_color': 'Blue',
            'window_width': 1200,
            'window_height': 800,
            'dpi_scaling': 'Auto',
            'remember_position': True,
            'plot_antialiasing': True,
            'plot_dpi': 100,
            'auto_save_settings': True,
            'confirm_exit': True,
            'show_splash': True,
            'auto_preprocess': False,
            'show_progress': True,
            'max_templates': 10,
            'thread_count': 4,
            'memory_limit': 8.0,
            'log_level': 'INFO',
            'debug_mode': False,
            # AI settings
            'openrouter_api_key': '',
            'favorite_model': '',
            'ai_temperature': 0.7,
            'ai_max_tokens': 2000,
            'ai_verbose': True,
            'ai_references': True
        }
        
        for key, default_value in defaults.items():
            if key in self.widgets:
                widget = self.widgets[key]
                value = self.settings.get(key, default_value)
                
                if isinstance(widget, QtWidgets.QComboBox):
                    index = widget.findText(str(value))
                    if index >= 0:
                        widget.setCurrentIndex(index)
                elif isinstance(widget, QtWidgets.QSpinBox):
                    widget.setValue(int(value))
                elif isinstance(widget, QtWidgets.QDoubleSpinBox):
                    widget.setValue(float(value))
                elif isinstance(widget, QtWidgets.QCheckBox):
                    widget.setChecked(bool(value))
                elif isinstance(widget, QtWidgets.QLineEdit):
                    widget.setText(str(value))
                elif isinstance(widget, QtWidgets.QListWidget):
                    # For favorite_model, select the item if it exists
                    if key == 'favorite_model' and value:
                        for i in range(widget.count()):
                            item = widget.item(i)
                            if item and item.data(QtCore.Qt.UserRole) == value:
                                widget.setCurrentItem(item)
                                break
        
        # Update font preview
        self._update_font_preview()
    
    def _collect_settings(self) -> Dict[str, Any]:
        """Collect settings from widgets"""
        settings = {}
        
        for key, widget in self.widgets.items():
            if isinstance(widget, QtWidgets.QComboBox):
                settings[key] = widget.currentText()
            elif isinstance(widget, QtWidgets.QSpinBox):
                settings[key] = widget.value()
            elif isinstance(widget, QtWidgets.QDoubleSpinBox):
                settings[key] = widget.value()
            elif isinstance(widget, QtWidgets.QCheckBox):
                settings[key] = widget.isChecked()
            elif isinstance(widget, QtWidgets.QLineEdit):
                settings[key] = widget.text()
            elif isinstance(widget, QtWidgets.QListWidget):
                # For favorite model, get the selected item's model ID
                if key == 'favorite_model':
                    current_item = widget.currentItem()
                    if current_item:
                        settings[key] = current_item.data(QtCore.Qt.UserRole)
                    else:
                        settings[key] = ''
                else:
                    settings[key] = ''
        
        return settings
    
    def _apply_settings(self):
        """Apply settings without closing dialog"""
        settings = self._collect_settings()
        
        # Apply to parent if available
        if hasattr(self.parent_gui, 'apply_settings'):
            self.parent_gui.apply_settings(settings)
        
        # Call callbacks
        for callback in self.settings_changed_callbacks:
            callback(settings)
        
        _LOGGER.info("Settings applied")
    
    def _ok_clicked(self):
        """Handle OK button click"""
        self.result = self._collect_settings()
        self._apply_settings()
        self.accept()
    
    def _reset_to_defaults(self):
        """Reset all settings to defaults"""
        reply = QtWidgets.QMessageBox.question(
            self,
            "Reset Settings",
            "Are you sure you want to reset all settings to defaults?\n\nThis action cannot be undone.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No
        )
        
        if reply == QtWidgets.QMessageBox.Yes:
            self.settings.clear()
            self._load_current_values()
            _LOGGER.info("Settings reset to defaults")
    
    def add_settings_changed_callback(self, callback: Callable[[Dict[str, Any]], None]):
        """Add callback for settings changes"""
        self.settings_changed_callbacks.append(callback)
    
    def _toggle_api_key_visibility(self):
        """Toggle API key visibility"""
        if self.widgets['openrouter_api_key'].echoMode() == QtWidgets.QLineEdit.Password:
            self.widgets['openrouter_api_key'].setEchoMode(QtWidgets.QLineEdit.Normal)
            self.show_key_btn.setText("Hide")
        else:
            self.widgets['openrouter_api_key'].setEchoMode(QtWidgets.QLineEdit.Password)
            self.show_key_btn.setText("Show")
    
    def _test_openrouter_connection(self):
        """Test OpenRouter API connection"""
        api_key = self.widgets['openrouter_api_key'].text().strip()
        if not api_key:
            QtWidgets.QMessageBox.warning(
                self, 
                "No API Key", 
                "Please enter your OpenRouter API key first."
            )
            return
        
        self.connection_status_label.setText("Testing...")
        self.connection_status_label.setStyleSheet(f"color: {self.colors['btn_warning']};")
        self.test_connection_btn.setEnabled(False)
        
        # Test connection in a separate thread
        def test_connection():
            try:
                import requests
                response = requests.get(
                    "https://openrouter.ai/api/v1/models",
                    headers={"Authorization": f"Bearer {api_key}"},
                    timeout=10
                )
                
                if response.status_code == 200:
                    QtCore.QMetaObject.invokeMethod(
                        self, "_on_connection_success", 
                        QtCore.Qt.QueuedConnection
                    )
                else:
                    error_msg = f"API Error: {response.status_code}"
                    QtCore.QMetaObject.invokeMethod(
                        self, "_on_connection_error", 
                        QtCore.Qt.QueuedConnection,
                        QtCore.Q_ARG(str, error_msg)
                    )
                    
            except Exception as e:
                QtCore.QMetaObject.invokeMethod(
                    self, "_on_connection_error", 
                    QtCore.Qt.QueuedConnection,
                    QtCore.Q_ARG(str, str(e))
                )
        
        import threading
        thread = threading.Thread(target=test_connection, daemon=True)
        thread.start()
    
    @QtCore.Slot()
    def _on_connection_success(self):
        """Handle successful connection test"""
        self.connection_status_label.setText("✅ Connected successfully")
        self.connection_status_label.setStyleSheet(f"color: {self.colors['btn_success']};")
        self.test_connection_btn.setEnabled(True)
    
    @QtCore.Slot(str)
    def _on_connection_error(self, error):
        """Handle connection test error"""
        self.connection_status_label.setText(f"❌ Error: {error}")
        self.connection_status_label.setStyleSheet(f"color: {self.colors['btn_danger']};")
        self.test_connection_btn.setEnabled(True)
    
    def _fetch_free_models(self):
        """Fetch available free models from OpenRouter"""
        api_key = self.widgets['openrouter_api_key'].text().strip()
        if not api_key:
            QtWidgets.QMessageBox.warning(
                self, 
                "No API Key", 
                "Please enter your OpenRouter API key first."
            )
            return
        
        self.model_status_label.setText("Fetching models...")
        self.model_status_label.setStyleSheet(f"color: {self.colors['btn_warning']};")
        self.fetch_models_btn.setEnabled(False)
        self.widgets['favorite_model'].clear()
        
        # Fetch models in separate thread
        def fetch_models():
            try:
                import requests
                response = requests.get(
                    "https://openrouter.ai/api/v1/models",
                    headers={"Authorization": f"Bearer {api_key}"},
                    timeout=15
                )
                
                if response.status_code == 200:
                    data = response.json()
                    models_data = data.get('data', data)
                    
                    # Filter for free models
                    free_models = []
                    for model in models_data:
                        if isinstance(model, dict) and 'name' in model and 'id' in model:
                            name = model.get('name', '')
                            if "(free)" in name.lower() or model.get('pricing', {}).get('prompt', '0') == '0':
                                free_models.append({
                                    'id': model['id'],
                                    'name': model['name'],
                                    'context_length': model.get('context_length', 4096)
                                })
                    
                    QtCore.QMetaObject.invokeMethod(
                        self, "_on_models_fetched", 
                        QtCore.Qt.QueuedConnection,
                        QtCore.Q_ARG(list, free_models)
                    )
                else:
                    error_msg = f"API Error: {response.status_code}"
                    QtCore.QMetaObject.invokeMethod(
                        self, "_on_fetch_error", 
                        QtCore.Qt.QueuedConnection,
                        QtCore.Q_ARG(str, error_msg)
                    )
                    
            except Exception as e:
                QtCore.QMetaObject.invokeMethod(
                    self, "_on_fetch_error", 
                    QtCore.Qt.QueuedConnection,
                    QtCore.Q_ARG(str, str(e))
                )
        
        import threading
        thread = threading.Thread(target=fetch_models, daemon=True)
        thread.start()
    
    @QtCore.Slot(list)
    def _on_models_fetched(self, models):
        """Handle successful model fetch"""
        self.widgets['favorite_model'].clear()
        
        if models:
            for model in models:
                # Create display text with model name and context length
                context = model.get('context_length', 4096)
                if context >= 1000:
                    context_str = f"{context//1000}k"
                else:
                    context_str = str(context)
                    
                display_text = f"{model['name']} ({context_str} tokens)"
                item = QtWidgets.QListWidgetItem(display_text)
                item.setData(QtCore.Qt.UserRole, model['id'])  # Store model ID
                self.widgets['favorite_model'].addItem(item)
            
            self.model_status_label.setText(f"Found {len(models)} free models")
            self.model_status_label.setStyleSheet(f"color: {self.colors['btn_success']};")
        else:
            self.model_status_label.setText("No free models found")
            self.model_status_label.setStyleSheet(f"color: {self.colors['btn_warning']};")
        
        self.fetch_models_btn.setEnabled(True)
    
    @QtCore.Slot(str)
    def _on_fetch_error(self, error):
        """Handle model fetch error"""
        self.model_status_label.setText(f"Error: {error}")
        self.model_status_label.setStyleSheet(f"color: {self.colors['btn_danger']};")
        self.fetch_models_btn.setEnabled(True) 