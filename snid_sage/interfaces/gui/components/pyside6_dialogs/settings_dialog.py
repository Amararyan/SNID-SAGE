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
    
    # Define custom signals for thread communication
    models_fetched = QtCore.Signal(str)  # JSON string of models
    fetch_error = QtCore.Signal(str)     # Error message
    connection_success = QtCore.Signal()  # Connection test success
    connection_error = QtCore.Signal(str) # Connection test error
    model_test_success = QtCore.Signal(str, str)  # model_id, model_name
    model_test_error = QtCore.Signal(str, str)    # model_id, error_message
    
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
        
        # Connect custom signals to slots
        self.models_fetched.connect(self._on_models_fetched)
        self.fetch_error.connect(self._on_fetch_error)
        self.connection_success.connect(self._on_connection_success)
        self.connection_error.connect(self._on_connection_error)
        self.model_test_success.connect(self._on_model_test_success)
        self.model_test_error.connect(self._on_model_test_error)
        
        # Store all models for filtering
        self.all_models = []
        
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
        self.setMinimumSize(700, 500)
        self.resize(800, 600)
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
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(10)
        
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
                padding: 8px;
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
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
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
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
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
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
        # OpenRouter API configuration group
        api_group = QtWidgets.QGroupBox("🔑 OpenRouter API Configuration")
        api_layout = QtWidgets.QVBoxLayout(api_group)
        api_layout.setSpacing(12)
        
        # Information label with clickable link
        info_frame = QtWidgets.QFrame()
        info_frame.setStyleSheet(f"""
            color: {self.colors['text_secondary']};
            font-style: italic;
            padding: 8px;
            background: {self.colors['bg_tertiary']};
            border-radius: 4px;
        """)
        
        info_layout = QtWidgets.QHBoxLayout(info_frame)
        info_layout.setContentsMargins(8, 8, 8, 8)
        info_layout.setSpacing(4)
        
        # Main text
        info_text = QtWidgets.QLabel("Configure your OpenRouter API key to enable AI-powered analysis features. Get your free API key at:")
        info_text.setStyleSheet(f"color: {self.colors['text_secondary']}; font-style: italic;")
        info_layout.addWidget(info_text)
        
        # Clickable link
        link_label = QtWidgets.QLabel("https://openrouter.ai")
        link_label.setStyleSheet(f"""
            color: {self.colors['accent_primary']};
            text-decoration: underline;
            font-style: italic;
        """)
        link_label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        link_label.mousePressEvent = lambda event: self._open_openrouter_website()
        info_layout.addWidget(link_label)
        
        info_layout.addStretch()
        api_layout.addWidget(info_frame)
        
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
        
        self.fetch_models_btn = QtWidgets.QPushButton("📡 Fetch All Models")
        self.fetch_models_btn.clicked.connect(self._fetch_all_models)
        model_controls_layout.addWidget(self.fetch_models_btn)
        
        self.fetch_free_btn = QtWidgets.QPushButton("🆓 Free Only")
        self.fetch_free_btn.clicked.connect(self._fetch_free_models)
        model_controls_layout.addWidget(self.fetch_free_btn)
        
        self.test_model_btn = QtWidgets.QPushButton("🧪 Test Selected")
        self.test_model_btn.clicked.connect(self._test_selected_model)
        self.test_model_btn.setEnabled(False)
        model_controls_layout.addWidget(self.test_model_btn)
        
        model_controls_layout.addStretch()
        
        self.model_status_label = QtWidgets.QLabel("No models loaded")
        self.model_status_label.setStyleSheet(f"color: {self.colors['text_secondary']};")
        model_controls_layout.addWidget(self.model_status_label)
        
        model_layout.addLayout(model_controls_layout)
        
        # Filter controls
        filter_layout = QtWidgets.QHBoxLayout()
        
        filter_layout.addWidget(QtWidgets.QLabel("Filter:"))
        
        self.filter_input = QtWidgets.QLineEdit()
        self.filter_input.setPlaceholderText("Search models...")
        self.filter_input.textChanged.connect(self._filter_models)
        filter_layout.addWidget(self.filter_input)
        
        self.free_only_check = QtWidgets.QCheckBox("Free only")
        self.free_only_check.toggled.connect(self._filter_models)
        filter_layout.addWidget(self.free_only_check)
        
        self.reasoning_check = QtWidgets.QCheckBox("Reasoning support")
        self.reasoning_check.toggled.connect(self._filter_models)
        filter_layout.addWidget(self.reasoning_check)
        
        model_layout.addLayout(filter_layout)
        
        # Model table
        self.widgets['favorite_model'] = QtWidgets.QTableWidget()
        self.widgets['favorite_model'].setColumnCount(6)
        self.widgets['favorite_model'].setHorizontalHeaderLabels([
            "Model Name", "Provider", "Context", "Reasoning", "Price", "Status"
        ])
        self.widgets['favorite_model'].setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.widgets['favorite_model'].setAlternatingRowColors(True)
        self.widgets['favorite_model'].setSortingEnabled(True)
        self.widgets['favorite_model'].setMaximumHeight(300)
        
        # Set column widths
        header = self.widgets['favorite_model'].horizontalHeader()
        header.setStretchLastSection(True)
        header.resizeSection(0, 250)  # Model Name
        header.resizeSection(1, 100)  # Provider
        header.resizeSection(2, 80)   # Context
        header.resizeSection(3, 80)   # Reasoning
        header.resizeSection(4, 120)  # Price
        header.resizeSection(5, 80)   # Status
        
        self.widgets['favorite_model'].setStyleSheet(f"""
            QTableWidget {{
                background: {self.colors['bg_secondary']};
                border: 1px solid {self.colors['border']};
                border-radius: 4px;
                font-size: 9pt;
                gridline-color: {self.colors['bg_tertiary']};
            }}
            QTableWidget::item {{
                padding: 4px 8px;
                border: none;
            }}
            QTableWidget::item:selected {{
                background: {self.colors['btn_primary']};
                color: white;
            }}
            QHeaderView::section {{
                background: {self.colors['bg_tertiary']};
                border: 1px solid {self.colors['border']};
                padding: 4px 8px;
                font-weight: bold;
            }}
        """)
        
        # Connect selection change
        self.widgets['favorite_model'].itemSelectionChanged.connect(self._on_model_selection_changed)
        
        model_layout.addWidget(self.widgets['favorite_model'])
        
        layout.addWidget(model_group)
        
        layout.addStretch()
        tab_widget.addTab(tab, "🤖 AI Assistant")
    
    def _create_behavior_tab(self, tab_widget):
        """Create behavior settings tab"""
        tab = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(tab)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
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
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)
        
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
        # Load saved OpenRouter API key
        saved_api_key = ''
        saved_model = ''
        try:
            from snid_sage.interfaces.llm.openrouter.openrouter_llm import get_openrouter_api_key, get_openrouter_config
            saved_api_key = get_openrouter_api_key() or ''
            config = get_openrouter_config()
            saved_model = config.get('model_id', '') if config else ''
        except Exception as e:
            _LOGGER.warning(f"Could not load saved OpenRouter settings: {e}")
        
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
            'openrouter_api_key': saved_api_key,
            'favorite_model': saved_model
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
                elif isinstance(widget, (QtWidgets.QListWidget, QtWidgets.QTableWidget)):
                    # For favorite_model, select the item if it exists
                    if key == 'favorite_model' and value:
                        if isinstance(widget, QtWidgets.QTableWidget):
                            # Search through table rows
                            for row in range(widget.rowCount()):
                                item = widget.item(row, 0)  # First column contains model data
                                if item and item.data(QtCore.Qt.UserRole) == value:
                                    widget.selectRow(row)
                                    break
                        else:
                            # Original list widget logic
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
            elif isinstance(widget, (QtWidgets.QListWidget, QtWidgets.QTableWidget)):
                # For favorite model, get the selected item's model ID
                if key == 'favorite_model':
                    if isinstance(widget, QtWidgets.QTableWidget):
                        selected_rows = widget.selectionModel().selectedRows()
                        if selected_rows:
                            row = selected_rows[0].row()
                            item = widget.item(row, 0)  # First column
                            if item:
                                settings[key] = item.data(QtCore.Qt.UserRole)
                            else:
                                settings[key] = ''
                        else:
                            settings[key] = ''
                    else:
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
        
        # Save OpenRouter API key if provided
        api_key = settings.get('openrouter_api_key', '').strip()
        if api_key:
            try:
                from snid_sage.interfaces.llm.openrouter.openrouter_llm import save_openrouter_api_key
                save_openrouter_api_key(api_key)
                _LOGGER.info("OpenRouter API key saved successfully")
            except Exception as e:
                _LOGGER.error(f"Failed to save OpenRouter API key: {e}")
                QtWidgets.QMessageBox.warning(
                    self,
                    "API Key Save Error",
                    f"Failed to save OpenRouter API key: {str(e)}"
                )
        
        # Save selected model if provided
        selected_model = settings.get('favorite_model', '').strip()
        if selected_model:
            try:
                from snid_sage.interfaces.llm.openrouter.openrouter_llm import save_openrouter_config
                save_openrouter_config(api_key, selected_model)
                _LOGGER.info(f"OpenRouter model preference saved: {selected_model}")
            except Exception as e:
                _LOGGER.error(f"Failed to save OpenRouter model preference: {e}")
        
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
                    self.connection_success.emit()
                else:
                    error_msg = f"API Error: {response.status_code}"
                    self.connection_error.emit(error_msg)
                    
            except Exception as e:
                self.connection_error.emit(str(e))
        
        import threading
        thread = threading.Thread(target=test_connection, daemon=True)
        thread.start()
    
    def _on_connection_success(self):
        """Handle successful connection test"""
        self.connection_status_label.setText("✅ Connected successfully")
        self.connection_status_label.setStyleSheet(f"color: {self.colors['btn_success']};")
        self.test_connection_btn.setEnabled(True)
    
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
                    
                    # Convert to JSON string and emit signal
                    import json
                    models_json = json.dumps(free_models)
                    self.models_fetched.emit(models_json)
                else:
                    error_msg = f"API Error: {response.status_code}"
                    self.fetch_error.emit(error_msg)
                    
            except Exception as e:
                self.fetch_error.emit(str(e))
        
        import threading
        thread = threading.Thread(target=fetch_models, daemon=True)
        thread.start()
    
    def _on_models_fetched(self, models_json):
        """Handle successful model fetch"""
        # Parse JSON string back to list
        try:
            import json
            models = json.loads(models_json)
        except (json.JSONDecodeError, ValueError) as e:
            _LOGGER.error(f"Failed to parse models JSON: {e}")
            self.model_status_label.setText("Error parsing models data")
            self.model_status_label.setStyleSheet(f"color: {self.colors['btn_danger']};")
            self.fetch_models_btn.setEnabled(True)
            self.fetch_free_btn.setEnabled(True)
            return
        
        if models:
            # Store models for filtering
            self.all_models = models
            
            # Populate table
            self._populate_model_table(models)
            
            self.model_status_label.setText(f"Found {len(models)} models")
            self.model_status_label.setStyleSheet(f"color: {self.colors['btn_success']};")
        else:
            self.model_status_label.setText("No models found")
            self.model_status_label.setStyleSheet(f"color: {self.colors['btn_warning']};")
        
        self.fetch_models_btn.setEnabled(True)
        self.fetch_free_btn.setEnabled(True)
    
    def _populate_model_table(self, models):
        """Populate the model table with data"""
        table = self.widgets['favorite_model']
        table.setRowCount(len(models))
        
        # Get current selected model to preserve selection
        config = {}
        try:
            from snid_sage.interfaces.llm.openrouter.openrouter_llm import get_openrouter_config, get_model_test_status
            config = get_openrouter_config()
        except Exception as e:
            _LOGGER.warning(f"Could not load OpenRouter config: {e}")
        
        current_model_id = config.get('model_id', '')
        
        for row, model in enumerate(models):
            # Model Name (with fallback)
            model_name = model.get('name', model.get('id', 'Unknown Model'))
            model_id = model.get('id', '')
            name_item = QtWidgets.QTableWidgetItem(model_name)
            name_item.setData(QtCore.Qt.UserRole, model_id)
            table.setItem(row, 0, name_item)
            
            # Provider (with fallback)
            provider = model.get('provider', 'Unknown')
            if not provider and 'id' in model:
                # Extract provider from model ID as fallback
                provider = model['id'].split('/')[0] if '/' in model['id'] else 'Unknown'
            provider_item = QtWidgets.QTableWidgetItem(provider)
            table.setItem(row, 1, provider_item)
            
            # Context Length (with fallback)
            context_display = model.get('context_display', str(model.get('context_length', 'Unknown')))
            context_item = QtWidgets.QTableWidgetItem(context_display)
            context_item.setData(QtCore.Qt.UserRole, model.get('context_length', 0))  # Store raw number for sorting
            table.setItem(row, 2, context_item)
            
            # Reasoning Support (with fallback)
            supports_reasoning = model.get('supports_reasoning', False)
            reasoning_text = "✅ Yes" if supports_reasoning else "❌ No"
            reasoning_item = QtWidgets.QTableWidgetItem(reasoning_text)
            reasoning_item.setData(QtCore.Qt.UserRole, supports_reasoning)  # Store boolean for sorting
            table.setItem(row, 3, reasoning_item)
            
            # Price (with fallback)
            price_display = model.get('price_display', 'Unknown')
            price_item = QtWidgets.QTableWidgetItem(price_display)
            prompt_price = model.get('prompt_price', 0)
            price_item.setData(QtCore.Qt.UserRole, prompt_price)  # Store raw price for sorting
            is_free = model.get('is_free', False)
            if is_free:
                price_item.setBackground(QtGui.QColor(200, 255, 200))  # Light green for free
            table.setItem(row, 4, price_item)
            
            # Status
            try:
                is_tested = get_model_test_status(model_id)
                if model_id == current_model_id and is_tested:
                    status_text = "✅ Active"
                    status_item = QtWidgets.QTableWidgetItem(status_text)
                    status_item.setBackground(QtGui.QColor(144, 238, 144))  # Light green
                elif is_tested:
                    status_text = "✅ Tested"
                    status_item = QtWidgets.QTableWidgetItem(status_text)
                    status_item.setBackground(QtGui.QColor(200, 255, 200))  # Light green
                else:
                    status_text = "⏳ Untested"
                    status_item = QtWidgets.QTableWidgetItem(status_text)
            except:
                status_text = "⏳ Untested"
                status_item = QtWidgets.QTableWidgetItem(status_text)
            
            table.setItem(row, 5, status_item)
            
            # Select current model if it matches
            if model['id'] == current_model_id:
                table.selectRow(row)
    
    def _on_fetch_error(self, error):
        """Handle model fetch error"""
        self.model_status_label.setText(f"Error: {error}")
        self.model_status_label.setStyleSheet(f"color: {self.colors['btn_danger']};")
        self.fetch_models_btn.setEnabled(True)
        self.fetch_free_btn.setEnabled(True)
    
    def _fetch_all_models(self):
        """Fetch all available models from OpenRouter"""
        api_key = self.widgets['openrouter_api_key'].text().strip()
        if not api_key:
            QtWidgets.QMessageBox.warning(
                self, 
                "No API Key", 
                "Please enter your OpenRouter API key first."
            )
            return
        
        self.model_status_label.setText("Fetching all models...")
        self.model_status_label.setStyleSheet(f"color: {self.colors['btn_warning']};")
        self.fetch_models_btn.setEnabled(False)
        self.fetch_free_btn.setEnabled(False)
        self.widgets['favorite_model'].setRowCount(0)
        
        # Fetch models in separate thread
        def fetch_all():
            try:
                from snid_sage.interfaces.llm.openrouter.openrouter_llm import fetch_all_models
                models = fetch_all_models(api_key, free_only=False)
                
                if models:
                    import json
                    models_json = json.dumps(models)
                    self.models_fetched.emit(models_json)
                else:
                    self.fetch_error.emit("No models found")
                    
            except Exception as e:
                self.fetch_error.emit(str(e))
        
        import threading
        thread = threading.Thread(target=fetch_all, daemon=True)
        thread.start()
    
    def _on_model_selection_changed(self):
        """Handle model selection change"""
        selected_rows = self.widgets['favorite_model'].selectionModel().selectedRows()
        self.test_model_btn.setEnabled(len(selected_rows) > 0)
    
    def _test_selected_model(self):
        """Test the selected model"""
        selected_rows = self.widgets['favorite_model'].selectionModel().selectedRows()
        if not selected_rows:
            return
        
        api_key = self.widgets['openrouter_api_key'].text().strip()
        if not api_key:
            QtWidgets.QMessageBox.warning(
                self, 
                "No API Key", 
                "Please enter your OpenRouter API key first."
            )
            return
        
        row = selected_rows[0].row()
        model_item = self.widgets['favorite_model'].item(row, 0)
        if not model_item:
            return
            
        model_id = model_item.data(QtCore.Qt.UserRole)
        model_name = model_item.text()
        
        self.test_model_btn.setEnabled(False)
        self.test_model_btn.setText("🧪 Testing...")
        
        # Test model in separate thread
        def test_model():
            try:
                from snid_sage.interfaces.llm.openrouter.openrouter_llm import call_openrouter_api, save_openrouter_config
                
                # Temporarily save this model for testing
                save_openrouter_config(api_key, model_id, model_name, False)
                
                # Test with a simple prompt
                test_prompt = "Hello! Please respond with a simple 'OK' if you can process this request."
                response = call_openrouter_api(test_prompt, max_tokens=50)
                
                if response and len(response.strip()) > 0:
                    # Mark as tested
                    save_openrouter_config(api_key, model_id, model_name, True)
                    self.model_test_success.emit(model_id, model_name)
                else:
                    self.model_test_error.emit(model_id, "Empty response from model")
                    
            except Exception as e:
                self.model_test_error.emit(model_id, str(e))
        
        import threading
        thread = threading.Thread(target=test_model, daemon=True)
        thread.start()
    
    def _on_model_test_success(self, model_id, model_name):
        """Handle successful model test"""
        self.test_model_btn.setEnabled(True)
        self.test_model_btn.setText("🧪 Test Selected")
        
        # Update the status column in the table
        for row in range(self.widgets['favorite_model'].rowCount()):
            item = self.widgets['favorite_model'].item(row, 0)
            if item and item.data(QtCore.Qt.UserRole) == model_id:
                status_item = self.widgets['favorite_model'].item(row, 5)  # Status column
                if status_item:
                    status_item.setText("✅ Tested")
                    status_item.setBackground(QtGui.QColor(200, 255, 200))  # Light green
                break
        
        QtWidgets.QMessageBox.information(
            self,
            "Model Test Successful",
            f"Model '{model_name}' tested successfully!\nIt will be used for future AI operations."
        )
    
    def _on_model_test_error(self, model_id, error_message):
        """Handle model test error"""
        self.test_model_btn.setEnabled(True)
        self.test_model_btn.setText("🧪 Test Selected")
        
        # Update the status column in the table
        for row in range(self.widgets['favorite_model'].rowCount()):
            item = self.widgets['favorite_model'].item(row, 0)
            if item and item.data(QtCore.Qt.UserRole) == model_id:
                status_item = self.widgets['favorite_model'].item(row, 5)  # Status column
                if status_item:
                    status_item.setText("❌ Failed")
                    status_item.setBackground(QtGui.QColor(255, 200, 200))  # Light red
                break
        
        QtWidgets.QMessageBox.warning(
            self,
            "Model Test Failed",
            f"Failed to test model:\n{error_message}"
        )
    
    def _open_openrouter_website(self):
        """Open OpenRouter website in default browser"""
        import webbrowser
        try:
            webbrowser.open("https://openrouter.ai")
        except Exception as e:
            _LOGGER.error(f"Failed to open OpenRouter website: {e}")
            QtWidgets.QMessageBox.warning(
                self,
                "Browser Error",
                "Failed to open browser. Please visit https://openrouter.ai manually."
            )
    
    def _filter_models(self):
        """Filter models based on search criteria"""
        if not hasattr(self, 'all_models') or not self.all_models:
            return
        
        search_text = self.filter_input.text().lower()
        free_only = self.free_only_check.isChecked()
        reasoning_only = self.reasoning_check.isChecked()
        
        # Filter models
        filtered_models = []
        for model in self.all_models:
            # Text search
            if search_text and search_text not in model['name'].lower() and search_text not in model['provider'].lower():
                continue
            
            # Free only filter
            if free_only and not model['is_free']:
                continue
                
            # Reasoning support filter
            if reasoning_only and not model['supports_reasoning']:
                continue
            
            filtered_models.append(model)
        
        # Update table with filtered models
        self._populate_model_table(filtered_models) 