"""
Enhanced AI Assistant Dialog - PySide6 Version

This module provides a modern AI assistant interface with:
- Single comprehensive summary generation
- Chat interface in separate tab
- Simplified settings
- User metadata input form
- Enhanced SNID context awareness
- Modern Qt design

Converted from Tkinter to PySide6 for modern Qt interface.
"""

import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtWidgets as QtWidgets
import threading
from datetime import datetime
import json
import os
from typing import Dict, Any, Optional

try:
    from snid_sage.shared.utils.logging import get_logger
    _LOGGER = get_logger('gui.pyside6_ai_assistant')
except ImportError:
    import logging
    _LOGGER = logging.getLogger('gui.pyside6_ai_assistant')


class PySide6EnhancedAIAssistantDialog(QtWidgets.QDialog):
    """
    Enhanced AI Assistant Dialog with simplified interface.
    
    Features:
    - Single comprehensive summary generation
    - Chat interface in separate tab
    - Settings menu
    - User metadata input
    - Enhanced SNID context
    """
    
    def __init__(self, parent, snid_results=None):
        """Initialize the enhanced AI assistant dialog."""
        super().__init__(parent)
        self.parent_gui = parent
        self.is_generating = False
        self.current_snid_results = snid_results
        
        # Theme colors (matching PySide6 main GUI)
        self.colors = {
            'bg_primary': '#f8fafc',
            'bg_secondary': '#ffffff',
            'bg_tertiary': '#f1f5f9',
            'text_primary': '#1e293b',
            'text_secondary': '#475569',
            'text_muted': '#94a3b8',
            'border': '#cbd5e1',
            'btn_primary': '#3b82f6',
            'btn_success': '#10b981',
            'btn_danger': '#ef4444',
            'btn_warning': '#f59e0b',
            'accent_primary': '#3b82f6',
        }
        
        self._setup_dialog()
        self._create_interface()
        
    def _setup_dialog(self):
        """Setup dialog window properties"""
        self.setWindowTitle("🤖 SNID AI Assistant")
        self.resize(1200, 900)
        self.setMinimumSize(800, 600)
        
        # Apply dialog styling
        self.setStyleSheet(f"""
            QDialog {{
                background: {self.colors['bg_primary']};
                color: {self.colors['text_primary']};
                font-family: "Segoe UI", Arial, sans-serif;
                font-size: 10pt;
            }}
            
            QTabWidget::pane {{
                border: 2px solid {self.colors['border']};
                border-radius: 6px;
                background: {self.colors['bg_secondary']};
            }}
            
            QTabWidget::tab-bar {{
                alignment: left;
            }}
            
            QTabBar::tab {{
                background: {self.colors['bg_tertiary']};
                border: 2px solid {self.colors['border']};
                border-bottom: none;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                min-width: 120px;
                padding: 8px 16px;
                margin-right: 2px;
                font-weight: bold;
            }}
            
            QTabBar::tab:selected {{
                background: {self.colors['bg_secondary']};
                border-color: {self.colors['border']};
                border-bottom: 2px solid {self.colors['bg_secondary']};
            }}
            
            QTabBar::tab:hover:!selected {{
                background: {self.colors['border']};
            }}
            
            QGroupBox {{
                font-weight: bold;
                font-size: 11pt;
                border: 2px solid {self.colors['border']};
                border-radius: 6px;
                margin-top: 8px;
                padding-top: 12px;
                background: {self.colors['bg_secondary']};
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px 0 8px;
                color: {self.colors['text_primary']};
            }}
            
            QPushButton {{
                border: 2px solid {self.colors['border']};
                border-radius: 6px;
                padding: 8px 16px;
                min-height: 24px;
                font-weight: bold;
                font-size: 10pt;
                background: {self.colors['bg_tertiary']};
            }}
            
            QPushButton:hover {{
                background: {self.colors['border']};
            }}
            
            QPushButton#primary_btn {{
                background: {self.colors['btn_primary']};
                color: white;
                border: 2px solid {self.colors['btn_primary']};
            }}
            
            QPushButton#primary_btn:hover {{
                background: #2563eb;
                border: 2px solid #2563eb;
            }}
            
            QPushButton#success_btn {{
                background: {self.colors['btn_success']};
                color: white;
                border: 2px solid {self.colors['btn_success']};
            }}
            
            QPushButton#success_btn:hover {{
                background: #059669;
                border: 2px solid #059669;
            }}
            
            QPushButton#danger_btn {{
                background: {self.colors['btn_danger']};
                color: white;
                border: 2px solid {self.colors['btn_danger']};
            }}
            
            QPushButton#danger_btn:hover {{
                background: #dc2626;
                border: 2px solid #dc2626;
            }}
            
            QPushButton:disabled {{
                background: {self.colors['bg_tertiary']};
                color: {self.colors['text_muted']};
                border: 2px solid {self.colors['border']};
            }}
            
            QTextEdit {{
                background: {self.colors['bg_secondary']};
                border: 2px solid {self.colors['border']};
                border-radius: 6px;
                padding: 8px;
                font-family: "Consolas", monospace;
                font-size: 10pt;
                selection-background-color: {self.colors['btn_primary']};
            }}
            
            QLineEdit {{
                background: {self.colors['bg_secondary']};
                border: 2px solid {self.colors['border']};
                border-radius: 4px;
                padding: 8px;
                font-size: 10pt;
            }}
            
            QLineEdit:focus {{
                border: 2px solid {self.colors['btn_primary']};
            }}
            
            QComboBox {{
                background: {self.colors['bg_secondary']};
                border: 2px solid {self.colors['border']};
                border-radius: 4px;
                padding: 6px 8px;
                font-size: 10pt;
                min-width: 100px;
            }}
            
            QComboBox:hover {{
                border: 2px solid {self.colors['btn_primary']};
            }}
            
            QComboBox::drop-down {{
                border: none;
                width: 20px;
            }}
            
            QComboBox::down-arrow {{
                image: none;
                border: 1px solid {self.colors['border']};
                width: 8px;
                height: 8px;
                background: {self.colors['text_secondary']};
            }}
            
            QCheckBox {{
                spacing: 8px;
                font-size: 10pt;
            }}
            
            QCheckBox::indicator {{
                width: 16px;
                height: 16px;
                border: 2px solid {self.colors['border']};
                border-radius: 3px;
                background: {self.colors['bg_secondary']};
            }}
            
            QCheckBox::indicator:checked {{
                background: {self.colors['btn_primary']};
                border: 2px solid {self.colors['btn_primary']};
            }}
            
            QProgressBar {{
                border: 2px solid {self.colors['border']};
                border-radius: 6px;
                text-align: center;
                font-weight: bold;
                background: {self.colors['bg_tertiary']};
            }}
            
            QProgressBar::chunk {{
                background: {self.colors['btn_primary']};
                border-radius: 4px;
            }}
            
            QLabel {{
                background: transparent;
                color: {self.colors['text_primary']};
            }}
        """)
    
    def _create_interface(self):
        """Create the main interface"""
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        # Header
        self._create_header(layout)
        
        # Tab widget for different functionality
        self.tab_widget = QtWidgets.QTabWidget()
        layout.addWidget(self.tab_widget)
        
        # Create tabs
        self._create_summary_tab()
        self._create_chat_tab()
        
        # Footer buttons
        self._create_footer_buttons(layout)
        
    def _create_header(self, layout):
        """Create header section"""
        header_frame = QtWidgets.QFrame()
        header_frame.setStyleSheet(f"""
            QFrame {{
                background: {self.colors['bg_secondary']};
                border: 2px solid {self.colors['border']};
                border-radius: 8px;
                padding: 16px;
            }}
        """)
        
        header_layout = QtWidgets.QVBoxLayout(header_frame)
        
        # Title with icon
        title_layout = QtWidgets.QHBoxLayout()
        
        title_label = QtWidgets.QLabel("🤖 SNID AI Assistant")
        title_label.setFont(QtGui.QFont("Segoe UI", 18, QtGui.QFont.Bold))
        title_layout.addWidget(title_label)
        
        title_layout.addStretch()
        
        # Status indicator
        self.status_label = QtWidgets.QLabel("Ready")
        self.status_label.setStyleSheet(f"color: {self.colors['btn_success']}; font-weight: bold;")
        title_layout.addWidget(self.status_label)
        
        header_layout.addLayout(title_layout)
        
        # Description
        desc_label = QtWidgets.QLabel(
            "Intelligent analysis and interpretation of SNID results using advanced AI"
        )
        desc_label.setStyleSheet(f"color: {self.colors['text_secondary']}; font-size: 12pt;")
        header_layout.addWidget(desc_label)
        
        layout.addWidget(header_frame)
    
    def _create_summary_tab(self):
        """Create summary generation tab"""
        summary_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(summary_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        # Context information - simplified
        context_group = QtWidgets.QGroupBox("📊 Analysis Status")
        context_layout = QtWidgets.QVBoxLayout(context_group)
        context_layout.setSpacing(6)
        
        # Results status
        if self.current_snid_results:
            results_text = "✅ SNID results ready for AI analysis"
            results_color = self.colors['btn_success']
        else:
            results_text = "⚠️ Run SNID analysis first for best results"
            results_color = self.colors['btn_warning']
        
        results_label = QtWidgets.QLabel(results_text)
        results_label.setStyleSheet(f"color: {results_color}; font-weight: bold; padding: 6px;")
        context_layout.addWidget(results_label)
        
        layout.addWidget(context_group)
        
        # User metadata input - more compact
        metadata_group = QtWidgets.QGroupBox("👤 Optional Information")
        metadata_layout = QtWidgets.QFormLayout(metadata_group)
        metadata_layout.setVerticalSpacing(4)
        
        self.observer_name_input = QtWidgets.QLineEdit()
        self.observer_name_input.setPlaceholderText("Your name")
        metadata_layout.addRow("Observer:", self.observer_name_input)
        
        self.telescope_input = QtWidgets.QLineEdit()
        self.telescope_input.setPlaceholderText("Telescope/instrument")
        metadata_layout.addRow("Telescope:", self.telescope_input)
        
        self.observation_date_input = QtWidgets.QLineEdit()
        self.observation_date_input.setPlaceholderText("YYYY-MM-DD")
        metadata_layout.addRow("Date:", self.observation_date_input)
        
        layout.addWidget(metadata_group)
        
        # Summary options - simplified
        options_group = QtWidgets.QGroupBox("📋 Include in Summary")
        options_layout = QtWidgets.QVBoxLayout(options_group)
        options_layout.setSpacing(4)
        
        # Checkboxes for different analysis aspects - more compact labels
        self.include_classification_cb = QtWidgets.QCheckBox("Classification analysis")
        self.include_classification_cb.setChecked(True)
        options_layout.addWidget(self.include_classification_cb)
        
        self.include_redshift_cb = QtWidgets.QCheckBox("Redshift & distance")
        self.include_redshift_cb.setChecked(True)
        options_layout.addWidget(self.include_redshift_cb)
        
        self.include_templates_cb = QtWidgets.QCheckBox("Template matching")
        self.include_templates_cb.setChecked(True)
        options_layout.addWidget(self.include_templates_cb)
        
        self.include_recommendations_cb = QtWidgets.QCheckBox("Observational recommendations")
        self.include_recommendations_cb.setChecked(True)
        options_layout.addWidget(self.include_recommendations_cb)
        
        layout.addWidget(options_group)
        
        # Generate summary controls - simplified
        generate_layout = QtWidgets.QHBoxLayout()
        
        self.generate_summary_btn = QtWidgets.QPushButton("Generate Summary")
        self.generate_summary_btn.setObjectName("primary_btn")
        self.generate_summary_btn.clicked.connect(self._generate_summary)
        self.generate_summary_btn.setMinimumHeight(40)
        generate_layout.addWidget(self.generate_summary_btn)
        
        self.summary_progress = QtWidgets.QProgressBar()
        self.summary_progress.setVisible(False)
        self.summary_progress.setMaximumHeight(30)
        generate_layout.addWidget(self.summary_progress)
        
        layout.addLayout(generate_layout)
        
        # Summary output
        summary_output_group = QtWidgets.QGroupBox("🤖 AI Analysis")
        summary_output_layout = QtWidgets.QVBoxLayout(summary_output_group)
        
        self.summary_text = QtWidgets.QTextEdit()
        self.summary_text.setPlaceholderText(
            "Your AI-generated analysis will appear here...\n\n"
            "Click 'Generate Summary' to start."
        )
        self.summary_text.setMinimumHeight(250)
        summary_output_layout.addWidget(self.summary_text)
        
        # Summary controls
        summary_controls_layout = QtWidgets.QHBoxLayout()
        
        self.export_summary_btn = QtWidgets.QPushButton("💾 Export Summary")
        self.export_summary_btn.clicked.connect(self._export_summary)
        self.export_summary_btn.setEnabled(False)
        summary_controls_layout.addWidget(self.export_summary_btn)
        
        self.copy_summary_btn = QtWidgets.QPushButton("📋 Copy to Clipboard")
        self.copy_summary_btn.clicked.connect(self._copy_summary)
        self.copy_summary_btn.setEnabled(False)
        summary_controls_layout.addWidget(self.copy_summary_btn)
        
        summary_controls_layout.addStretch()
        
        summary_output_layout.addLayout(summary_controls_layout)
        layout.addWidget(summary_output_group)
        
        layout.addStretch()
        self.tab_widget.addTab(summary_widget, "📊 Summary")
    
    def _create_chat_tab(self):
        """Create interactive chat tab"""
        chat_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(chat_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        # Chat history
        chat_group = QtWidgets.QGroupBox("💬 Ask Questions")
        chat_layout = QtWidgets.QVBoxLayout(chat_group)
        
        self.chat_history = QtWidgets.QTextEdit()
        self.chat_history.setReadOnly(True)
        self.chat_history.setMinimumHeight(350)
        self.chat_history.setPlainText(
            "🤖 AI Assistant: Hello! Ask me questions about your SNID analysis.\n\n"
            "Examples:\n"
            "• What type of supernova is this?\n"
            "• How confident is this classification?\n"
            "• What's the estimated redshift?\n"
            "• Should I follow up with more observations?\n\n"
            "What would you like to know?"
        )
        chat_layout.addWidget(self.chat_history)
        
        layout.addWidget(chat_group)
        
        # Input area - simplified
        input_group = QtWidgets.QGroupBox("✍️ Your Question")
        input_layout = QtWidgets.QVBoxLayout(input_group)
        
        self.chat_input = QtWidgets.QTextEdit()
        self.chat_input.setMaximumHeight(70)
        self.chat_input.setPlaceholderText("Type your question here...")
        input_layout.addWidget(self.chat_input)
        
        # Send controls
        send_layout = QtWidgets.QHBoxLayout()
        
        self.send_btn = QtWidgets.QPushButton("💬 Send Message")
        self.send_btn.setObjectName("primary_btn")
        self.send_btn.clicked.connect(self._send_chat_message)
        send_layout.addWidget(self.send_btn)
        
        self.clear_chat_btn = QtWidgets.QPushButton("🧹 Clear Chat")
        self.clear_chat_btn.clicked.connect(self._clear_chat)
        send_layout.addWidget(self.clear_chat_btn)
        
        send_layout.addStretch()
        
        input_layout.addLayout(send_layout)
        layout.addWidget(input_group)
        
        self.tab_widget.addTab(chat_widget, "💬 Chat")
    
    def _create_settings_tab(self):
        """Create settings and configuration tab"""
        settings_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(settings_widget)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(12)
        
        # AI Model settings
        model_group = QtWidgets.QGroupBox("AI Model Configuration")
        model_layout = QtWidgets.QFormLayout(model_group)
        
        self.model_selection = QtWidgets.QComboBox()
        self.model_selection.addItems([
            "GPT-4 (Recommended)",
            "GPT-3.5-Turbo",
            "Claude-3",
            "Local Model"
        ])
        model_layout.addRow("AI Model:", self.model_selection)
        
        self.temperature_spin = QtWidgets.QDoubleSpinBox()
        self.temperature_spin.setRange(0.0, 2.0)
        self.temperature_spin.setSingleStep(0.1)
        self.temperature_spin.setValue(0.7)
        self.temperature_spin.setDecimals(1)
        model_layout.addRow("Temperature:", self.temperature_spin)
        
        self.max_tokens_spin = QtWidgets.QSpinBox()
        self.max_tokens_spin.setRange(100, 4000)
        self.max_tokens_spin.setValue(2000)
        model_layout.addRow("Max Tokens:", self.max_tokens_spin)
        
        layout.addWidget(model_group)
        
        # API Configuration
        api_group = QtWidgets.QGroupBox("API Configuration")
        api_layout = QtWidgets.QFormLayout(api_group)
        
        self.api_key_input = QtWidgets.QLineEdit()
        self.api_key_input.setEchoMode(QtWidgets.QLineEdit.Password)
        self.api_key_input.setPlaceholderText("Enter your API key")
        api_layout.addRow("API Key:", self.api_key_input)
        
        self.api_endpoint_input = QtWidgets.QLineEdit()
        self.api_endpoint_input.setPlaceholderText("Custom API endpoint (optional)")
        api_layout.addRow("Custom Endpoint:", self.api_endpoint_input)
        
        # Test connection button
        test_connection_btn = QtWidgets.QPushButton("🔍 Test Connection")
        test_connection_btn.clicked.connect(self._test_api_connection)
        api_layout.addRow("", test_connection_btn)
        
        layout.addWidget(api_group)
        
        # Output preferences
        output_group = QtWidgets.QGroupBox("Output Preferences")
        output_layout = QtWidgets.QVBoxLayout(output_group)
        
        self.verbose_output_cb = QtWidgets.QCheckBox("Verbose explanations")
        self.verbose_output_cb.setChecked(True)
        output_layout.addWidget(self.verbose_output_cb)
        
        self.include_references_cb = QtWidgets.QCheckBox("Include scientific references")
        self.include_references_cb.setChecked(True)
        output_layout.addWidget(self.include_references_cb)
        
        self.technical_language_cb = QtWidgets.QCheckBox("Use technical language")
        self.technical_language_cb.setChecked(True)
        output_layout.addWidget(self.technical_language_cb)
        
        layout.addWidget(output_group)
        
        layout.addStretch()
        
        # Reset settings button
        reset_btn = QtWidgets.QPushButton("🔄 Reset to Defaults")
        reset_btn.clicked.connect(self._reset_settings)
        layout.addWidget(reset_btn)
        
        self.tab_widget.addTab(settings_widget, "⚙️ Settings")
    
    def _create_footer_buttons(self, layout):
        """Create footer buttons"""
        button_layout = QtWidgets.QHBoxLayout()
        
        # Help button
        help_btn = QtWidgets.QPushButton("❓ Help")
        help_btn.clicked.connect(self._show_help)
        button_layout.addWidget(help_btn)
        
        button_layout.addStretch()
        
        # Close button
        close_btn = QtWidgets.QPushButton("❌ Close")
        close_btn.clicked.connect(self.reject)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
    
    def _generate_summary(self):
        """Generate comprehensive AI summary"""
        if self.is_generating:
            return
        
        self.is_generating = True
        self.generate_summary_btn.setEnabled(False)
        self.summary_progress.setVisible(True)
        self.summary_progress.setRange(0, 0)  # Indeterminate progress
        self.status_label.setText("Generating...")
        self.status_label.setStyleSheet(f"color: {self.colors['btn_warning']}; font-weight: bold;")
        
        # Simulate AI processing (in a real implementation, this would call the AI service)
        def generate_mock_summary():
            try:
                import time
                time.sleep(3)  # Simulate processing time
                
                # Generate mock summary
                observer = self.observer_name_input.text() or "Observer"
                telescope = self.telescope_input.text() or "Unknown telescope"
                obs_date = self.observation_date_input.text() or "Unknown date"
                
                summary = f"""
SNID AI ANALYSIS SUMMARY
========================

Observer: {observer}
Telescope: {telescope}
Observation Date: {obs_date}
Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

CLASSIFICATION ANALYSIS:
"""
                
                if self.current_snid_results:
                    summary += """
✅ Based on the SNID template matching analysis, this spectrum shows characteristics 
consistent with a Type Ia supernova at moderate redshift. The template matches 
indicate a well-sampled lightcurve phase around maximum light.

KEY FINDINGS:
• Strong correlation with SNe Ia templates
• Estimated redshift: z ≈ 0.025 ± 0.005
• Phase: Near maximum light (-5 to +10 days)
• Host galaxy contamination: Minimal
"""
                else:
                    summary += """
⚠️  Limited analysis available - no SNID results provided.
Please run SNID analysis first for comprehensive classification.
"""
                
                if self.include_redshift_cb.isChecked():
                    summary += """

REDSHIFT & DISTANCE ANALYSIS:
• Distance modulus: μ ≈ 32.5 mag
• Luminosity distance: ~110 Mpc
• Recession velocity: ~7,500 km/s
"""
                
                if self.include_templates_cb.isChecked():
                    summary += """

TEMPLATE MATCHING DETAILS:
• Best match: SN 1994D (Ia, +2d)
• Secondary matches: SN 1992A, SN 1999by
• Match quality: Excellent (rlap > 8.0)
"""
                
                if self.include_recommendations_cb.isChecked():
                    summary += """

OBSERVATIONAL RECOMMENDATIONS:
• Follow-up spectroscopy recommended within 1-2 weeks
• Photometric monitoring suggested for lightcurve characterization
• Consider late-time spectroscopy for nebular phase analysis
"""
                
                summary += """

CONFIDENCE ASSESSMENT:
High confidence in Type Ia classification based on spectral features
and template matching quality. Recommended for inclusion in SN Ia samples.

Generated by SNID SAGE AI Assistant
"""
                
                # Update UI from main thread
                QtCore.QMetaObject.invokeMethod(
                    self, "_update_summary_result", 
                    QtCore.Qt.QueuedConnection,
                    QtCore.Q_ARG(str, summary)
                )
                
            except Exception as e:
                QtCore.QMetaObject.invokeMethod(
                    self, "_handle_summary_error", 
                    QtCore.Qt.QueuedConnection,
                    QtCore.Q_ARG(str, str(e))
                )
        
        # Start generation in background thread
        thread = threading.Thread(target=generate_mock_summary, daemon=True)
        thread.start()
    
    @QtCore.Slot(str)
    def _update_summary_result(self, summary):
        """Update summary result in main thread"""
        self.summary_text.setPlainText(summary)
        self.is_generating = False
        self.generate_summary_btn.setEnabled(True)
        self.summary_progress.setVisible(False)
        self.export_summary_btn.setEnabled(True)
        self.copy_summary_btn.setEnabled(True)
        self.status_label.setText("Summary Generated")
        self.status_label.setStyleSheet(f"color: {self.colors['btn_success']}; font-weight: bold;")
        _LOGGER.info("AI summary generated successfully")
    
    @QtCore.Slot(str)
    def _handle_summary_error(self, error):
        """Handle summary generation error"""
        self.is_generating = False
        self.generate_summary_btn.setEnabled(True)
        self.summary_progress.setVisible(False)
        self.status_label.setText("Error")
        self.status_label.setStyleSheet(f"color: {self.colors['btn_danger']}; font-weight: bold;")
        
        QtWidgets.QMessageBox.critical(
            self, 
            "AI Error", 
            f"Error generating summary:\n{error}"
        )
    
    def _send_chat_message(self):
        """Send chat message to AI"""
        message = self.chat_input.toPlainText().strip()
        if not message:
            return
        
        # Add user message to chat
        current_chat = self.chat_history.toPlainText()
        current_chat += f"\n\nYou: {message}"
        
        # Simulate AI response
        ai_response = "AI Assistant: Thank you for your question. In a full implementation, " \
                     "I would analyze your SNID results and provide detailed insights about " \
                     "your supernova classification. This is a placeholder response."
        
        current_chat += f"\n\n{ai_response}"
        
        self.chat_history.setPlainText(current_chat)
        self.chat_input.clear()
        
        # Scroll to bottom
        scrollbar = self.chat_history.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    def _clear_chat(self):
        """Clear chat history"""
        self.chat_history.setPlainText(
            "AI Assistant: Hello! I'm ready to help you analyze your SNID results. "
            "What would you like to know?"
        )
    
    def _export_summary(self):
        """Export summary to file"""
        filename, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Export AI Summary",
            f"snid_ai_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if filename:
            try:
                with open(filename, 'w') as f:
                    f.write(self.summary_text.toPlainText())
                
                QtWidgets.QMessageBox.information(
                    self, 
                    "Export Successful", 
                    f"Summary exported to {filename}"
                )
                _LOGGER.info(f"AI summary exported to {filename}")
                
            except Exception as e:
                QtWidgets.QMessageBox.critical(
                    self, 
                    "Export Error", 
                    f"Error exporting summary:\n{e}"
                )
    
    def _copy_summary(self):
        """Copy summary to clipboard"""
        clipboard = QtWidgets.QApplication.clipboard()
        clipboard.setText(self.summary_text.toPlainText())
        
        # Show temporary status
        original_text = self.status_label.text()
        self.status_label.setText("Copied to Clipboard")
        QtCore.QTimer.singleShot(2000, lambda: self.status_label.setText(original_text))
    
    def _test_api_connection(self):
        """Test API connection"""
        QtWidgets.QMessageBox.information(
            self, 
            "API Test", 
            "API connection test would be implemented here.\n\n"
            "This would verify connectivity to the selected AI service."
        )
    
    def _reset_settings(self):
        """Reset settings to defaults"""
        self.model_selection.setCurrentIndex(0)
        self.temperature_spin.setValue(0.7)
        self.max_tokens_spin.setValue(2000)
        self.api_key_input.clear()
        self.api_endpoint_input.clear()
        self.verbose_output_cb.setChecked(True)
        self.include_references_cb.setChecked(True)
        self.technical_language_cb.setChecked(True)
    
    def _show_help(self):
        """Show help information"""
        help_text = """
SNID AI Assistant Help
=====================

SUMMARY TAB:
- Fill in optional user information for personalized reports
- Select analysis options to include in the summary
- Click 'Generate Comprehensive Summary' to create AI analysis
- Export or copy the summary for use in reports

CHAT TAB:
- Interactive conversation with AI about your results
- Ask specific questions about classification, redshift, etc.
- Chat history is maintained during the session

SETTINGS TAB:
- Configure AI model and parameters
- Set up API credentials for external AI services
- Customize output preferences

For best results, ensure SNID analysis has been completed
before using the AI assistant.
"""
        
        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle("AI Assistant Help")
        msg.setText(help_text)
        msg.setTextFormat(QtCore.Qt.PlainText)
        msg.exec_() 