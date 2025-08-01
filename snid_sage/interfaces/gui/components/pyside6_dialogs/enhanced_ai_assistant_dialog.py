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
        self.setWindowTitle("AI Assistant")
        self.resize(1000, 700)
        self.setMinimumSize(700, 500)
        
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
        """Create header section with AI controls"""
        header_layout = QtWidgets.QHBoxLayout()
        
        # Left side - Status indicator
        self.status_label = QtWidgets.QLabel("Ready")
        self.status_label.setStyleSheet(f"color: {self.colors['btn_success']}; font-weight: bold; font-size: 11pt;")
        header_layout.addWidget(self.status_label)
        
        header_layout.addStretch()
        
        # Right side - AI Controls
        ai_controls_group = QtWidgets.QGroupBox("🔧 AI Settings")
        ai_controls_layout = QtWidgets.QGridLayout(ai_controls_group)
        ai_controls_layout.setSpacing(8)
        
        # Model selection
        ai_controls_layout.addWidget(QtWidgets.QLabel("Model:"), 0, 0)
        self.model_combo = QtWidgets.QComboBox()
        self.model_combo.setMinimumWidth(200)
        self.model_combo.currentTextChanged.connect(self._on_model_changed)
        ai_controls_layout.addWidget(self.model_combo, 0, 1)
        
        # Refresh models button
        self.refresh_models_btn = QtWidgets.QPushButton("🔄")
        self.refresh_models_btn.setMaximumWidth(30)
        self.refresh_models_btn.setToolTip("Refresh available models")
        self.refresh_models_btn.clicked.connect(self._refresh_models)
        ai_controls_layout.addWidget(self.refresh_models_btn, 0, 2)
        
        # Temperature setting
        ai_controls_layout.addWidget(QtWidgets.QLabel("Temperature:"), 1, 0)
        self.temperature_spin = QtWidgets.QDoubleSpinBox()
        self.temperature_spin.setRange(0.0, 2.0)
        self.temperature_spin.setSingleStep(0.1)
        self.temperature_spin.setValue(0.7)
        self.temperature_spin.setDecimals(1)
        self.temperature_spin.setMaximumWidth(80)
        ai_controls_layout.addWidget(self.temperature_spin, 1, 1)
        
        # Max tokens setting
        ai_controls_layout.addWidget(QtWidgets.QLabel("Max Tokens:"), 1, 2)
        self.max_tokens_spin = QtWidgets.QSpinBox()
        self.max_tokens_spin.setRange(100, 4000)
        self.max_tokens_spin.setValue(2000)
        self.max_tokens_spin.setMaximumWidth(80)
        ai_controls_layout.addWidget(self.max_tokens_spin, 1, 3)
        
        # Style the group box
        ai_controls_group.setStyleSheet(f"""
            QGroupBox {{
                font-weight: bold;
                font-size: 9pt;
                border: 1px solid {self.colors['border']};
                border-radius: 4px;
                margin-top: 8px;
                padding-top: 8px;
                background: {self.colors['bg_secondary']};
            }}
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 8px;
                padding: 0 4px 0 4px;
                background: {self.colors['bg_secondary']};
            }}
        """)
        
        header_layout.addWidget(ai_controls_group)
        
        layout.addLayout(header_layout)
        
        # Load available models
        self._load_available_models()
    
    def _create_summary_tab(self):
        """Create summary generation tab"""
        summary_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(summary_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        # Simple status indicator
        if self.current_snid_results:
            results_text = "✅ SNID results ready for AI analysis"
            results_color = self.colors['btn_success']
        else:
            results_text = "⚠️ Run SNID analysis first for best results"
            results_color = self.colors['btn_warning']
        
        results_label = QtWidgets.QLabel(results_text)
        results_label.setStyleSheet(f"color: {results_color}; font-weight: bold; padding: 8px; margin-bottom: 8px;")
        layout.addWidget(results_label)
        
        # Compact metadata input
        metadata_layout = QtWidgets.QHBoxLayout()
        
        self.observer_name_input = QtWidgets.QLineEdit()
        self.observer_name_input.setPlaceholderText("Observer name (optional)")
        metadata_layout.addWidget(self.observer_name_input)
        
        self.telescope_input = QtWidgets.QLineEdit()
        self.telescope_input.setPlaceholderText("Telescope (optional)")
        metadata_layout.addWidget(self.telescope_input)
        
        self.observation_date_input = QtWidgets.QLineEdit()
        self.observation_date_input.setPlaceholderText("Date (optional)")
        metadata_layout.addWidget(self.observation_date_input)
        
        layout.addLayout(metadata_layout)
        
        # Simplified options in a single row
        options_layout = QtWidgets.QHBoxLayout()
        
        self.include_classification_cb = QtWidgets.QCheckBox("Classification")
        self.include_classification_cb.setChecked(True)
        options_layout.addWidget(self.include_classification_cb)
        
        self.include_redshift_cb = QtWidgets.QCheckBox("Redshift")
        self.include_redshift_cb.setChecked(True)
        options_layout.addWidget(self.include_redshift_cb)
        
        self.include_templates_cb = QtWidgets.QCheckBox("Templates")
        self.include_templates_cb.setChecked(True)
        options_layout.addWidget(self.include_templates_cb)
        
        self.include_recommendations_cb = QtWidgets.QCheckBox("Recommendations")
        self.include_recommendations_cb.setChecked(True)
        options_layout.addWidget(self.include_recommendations_cb)
        
        options_layout.addStretch()
        layout.addLayout(options_layout)
        
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
        
        # Summary output - no group box
        self.summary_text = QtWidgets.QTextEdit()
        self.summary_text.setPlaceholderText(
            "Your AI-generated analysis will appear here...\n\n"
            "Click 'Generate Summary' to start."
        )
        self.summary_text.setMinimumHeight(300)
        layout.addWidget(self.summary_text)
        
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
        layout.addLayout(summary_controls_layout)
        
        layout.addStretch()
        self.tab_widget.addTab(summary_widget, "📊 Summary")
    
    def _create_chat_tab(self):
        """Create interactive chat tab"""
        chat_widget = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(chat_widget)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        
        # Chat history - no group box
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
        layout.addWidget(self.chat_history)
        
        # Input area - simplified, no group box
        self.chat_input = QtWidgets.QTextEdit()
        self.chat_input.setMaximumHeight(70)
        self.chat_input.setPlaceholderText("Type your question here...")
        layout.addWidget(self.chat_input)
        
        # Send controls
        send_layout = QtWidgets.QHBoxLayout()
        
        self.send_btn = QtWidgets.QPushButton("💬 Send")
        self.send_btn.setObjectName("primary_btn")
        self.send_btn.clicked.connect(self._send_chat_message)
        send_layout.addWidget(self.send_btn)
        
        self.clear_chat_btn = QtWidgets.QPushButton("🧹 Clear")
        self.clear_chat_btn.clicked.connect(self._clear_chat)
        send_layout.addWidget(self.clear_chat_btn)
        
        send_layout.addStretch()
        
        layout.addLayout(send_layout)
        
        self.tab_widget.addTab(chat_widget, "💬 Chat")
    

    
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
        
        # Generate real AI summary using current settings
        def generate_real_summary():
            try:
                # Get current AI settings
                ai_settings = self._get_current_ai_settings()
                
                # Collect user metadata
                user_metadata = {
                    'observer_name': self.observer_name_input.text(),
                    'telescope': self.telescope_input.text(),
                    'observation_date': self.observation_date_input.text(),
                    'specific_request': self.specific_request_input.toPlainText()
                }
                
                # Generate summary using LLM integration
                if hasattr(self.parent_gui, 'llm_integration') and self.parent_gui.llm_integration:
                    summary_text = self.parent_gui.llm_integration.generate_summary(
                        self.current_snid_results,
                        user_metadata=user_metadata,
                        max_tokens=ai_settings['max_tokens'],
                        temperature=ai_settings['temperature']
                    )
                else:
                    # Fallback if no LLM integration
                    from snid_sage.interfaces.gui.features.results.llm_integration import LLMIntegration
                    llm = LLMIntegration(self.current_snid_results)
                    summary_text = llm.generate_summary(
                        user_metadata=user_metadata,
                        max_tokens=ai_settings['max_tokens'],
                        temperature=ai_settings['temperature']
                    )
                
                summary = f"""
SNID AI ANALYSIS SUMMARY
========================

Observer: {user_metadata.get('observer_name', 'Not specified')}
Telescope: {user_metadata.get('telescope', 'Not specified')}  
Observation Date: {user_metadata.get('observation_date', 'Not specified')}
Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
AI Model: {self.model_combo.currentText().replace('✅ ', '').replace('⏳ ', '').replace('🆓 ', '').replace('🧠 ', '')}

CLASSIFICATION ANALYSIS:
{summary_text}
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
        thread = threading.Thread(target=generate_real_summary, daemon=True)
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
        self.chat_history.setPlainText(current_chat)
        self.chat_input.clear()
        
        # Get AI response using current settings
        def get_ai_response():
            try:
                ai_settings = self._get_current_ai_settings()
                
                # Use LLM integration to get real response
                if hasattr(self.parent_gui, 'llm_integration') and self.parent_gui.llm_integration:
                    ai_response = self.parent_gui.llm_integration.chat_with_llm(
                        message,
                        context=str(self.current_snid_results) if self.current_snid_results else "",
                        max_tokens=ai_settings['max_tokens']
                    )
                else:
                    # Fallback if no LLM integration
                    from snid_sage.interfaces.gui.features.results.llm_integration import LLMIntegration
                    llm = LLMIntegration(self.current_snid_results)
                    ai_response = llm.chat_with_llm(
                        message,
                        context="",
                        max_tokens=ai_settings['max_tokens']
                    )
                
                # Update chat in main thread
                current_chat = self.chat_history.toPlainText()
                current_chat += f"\n\nAI Assistant: {ai_response}"
                
                QtCore.QMetaObject.invokeMethod(
                    self, "_update_chat",
                    QtCore.Qt.QueuedConnection,
                    QtCore.Q_ARG(str, current_chat)
                )
                
            except Exception as e:
                error_msg = f"Sorry, I encountered an error: {str(e)}"
                current_chat = self.chat_history.toPlainText()
                current_chat += f"\n\nAI Assistant: {error_msg}"
                
                QtCore.QMetaObject.invokeMethod(
                    self, "_update_chat",
                    QtCore.Qt.QueuedConnection,
                    QtCore.Q_ARG(str, current_chat)
                )
        
        # Start chat response in background
        thread = threading.Thread(target=get_ai_response, daemon=True)
        thread.start()
        
        # Scroll to bottom
        scrollbar = self.chat_history.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())
    
    @QtCore.Slot(str)
    def _update_chat(self, chat_text):
        """Update chat display in main thread"""
        self.chat_history.setPlainText(chat_text)
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

SETTINGS:
- Use the main application settings to configure AI options

For best results, ensure SNID analysis has been completed
before using the AI assistant.
"""
        
        msg = QtWidgets.QMessageBox(self)
        msg.setWindowTitle("AI Assistant Help")
        msg.setText(help_text)
        msg.setTextFormat(QtCore.Qt.PlainText)
        msg.exec_()
    
    def _load_available_models(self):
        """Load available models from OpenRouter or saved config"""
        try:
            from snid_sage.interfaces.llm.openrouter.openrouter_llm import get_openrouter_config, get_openrouter_api_key
            
            config = get_openrouter_config()
            api_key = get_openrouter_api_key()
            
            # Start with current model if available
            current_model_id = config.get('model_id', '')
            current_model_name = config.get('model_name', '')
            
            self.model_combo.clear()
            
            if current_model_name and current_model_id:
                # Add current model first
                status = "✅ " if config.get('model_tested', False) else "⏳ "
                display_text = f"{status}{current_model_name}"
                self.model_combo.addItem(display_text, current_model_id)
            
            # Add some popular fallback models
            fallback_models = [
                ("GPT-4o Mini", "openai/gpt-4o-mini"),
                ("GPT-3.5 Turbo", "openai/gpt-3.5-turbo"),
                ("Claude 3 Haiku", "anthropic/claude-3-haiku"),
                ("Llama 3.1 8B", "meta-llama/llama-3.1-8b-instruct:free"),
            ]
            
            for name, model_id in fallback_models:
                if model_id != current_model_id:  # Don't duplicate current model
                    self.model_combo.addItem(f"⏳ {name}", model_id)
            
            # Add option to refresh from API
            self.model_combo.addItem("🔄 Load from API...", "refresh_from_api")
            
        except Exception as e:
            _LOGGER.warning(f"Could not load models: {e}")
            # Add basic fallback
            self.model_combo.addItem("GPT-4o Mini", "openai/gpt-4o-mini")
    
    def _refresh_models(self):
        """Refresh models from OpenRouter API"""
        try:
            from snid_sage.interfaces.llm.openrouter.openrouter_llm import get_openrouter_api_key, fetch_all_models
            
            api_key = get_openrouter_api_key()
            if not api_key:
                QtWidgets.QMessageBox.warning(
                    self,
                    "No API Key",
                    "Please configure your OpenRouter API key in Settings first."
                )
                return
            
            self.refresh_models_btn.setEnabled(False)
            self.refresh_models_btn.setText("...")
            
            # Fetch models in background
            def fetch_models():
                try:
                    models = fetch_all_models(api_key, free_only=False)
                    if models:
                        # Filter to tested and popular models
                        priority_models = []
                        other_models = []
                        
                        for model in models:
                            if model['is_free'] or 'gpt' in model['name'].lower() or 'claude' in model['name'].lower():
                                priority_models.append(model)
                            else:
                                other_models.append(model)
                        
                        # Update UI on main thread
                        self._update_model_combo(priority_models + other_models[:10])  # Limit to avoid overwhelming
                    else:
                        self._on_model_refresh_error("No models found")
                except Exception as e:
                    self._on_model_refresh_error(str(e))
            
            import threading
            thread = threading.Thread(target=fetch_models, daemon=True)
            thread.start()
            
        except Exception as e:
            QtWidgets.QMessageBox.warning(
                self,
                "Refresh Error", 
                f"Failed to refresh models: {str(e)}"
            )
    
    def _update_model_combo(self, models):
        """Update model combo box with fetched models"""
        try:
            from snid_sage.interfaces.llm.openrouter.openrouter_llm import get_openrouter_config
            
            config = get_openrouter_config()
            current_model_id = config.get('model_id', '')
            
            self.model_combo.clear()
            
            # Add models with status indicators
            for model in models:
                status = "✅ " if model['id'] == current_model_id else "⏳ "
                if model['is_free']:
                    status += "🆓 "
                if model['supports_reasoning']:
                    status += "🧠 "
                
                display_text = f"{status}{model['name']}"
                self.model_combo.addItem(display_text, model['id'])
            
            # Select current model if it exists
            for i in range(self.model_combo.count()):
                if self.model_combo.itemData(i) == current_model_id:
                    self.model_combo.setCurrentIndex(i)
                    break
            
            self.refresh_models_btn.setEnabled(True)
            self.refresh_models_btn.setText("🔄")
            
        except Exception as e:
            self._on_model_refresh_error(str(e))
    
    def _on_model_refresh_error(self, error_msg):
        """Handle model refresh error"""
        self.refresh_models_btn.setEnabled(True)
        self.refresh_models_btn.setText("🔄")
        QtWidgets.QMessageBox.warning(
            self,
            "Model Refresh Failed",
            f"Could not refresh models: {error_msg}"
        )
    
    def _on_model_changed(self):
        """Handle model selection change"""
        current_data = self.model_combo.currentData()
        
        if current_data == "refresh_from_api":
            self._refresh_models()
            return
        
        if current_data:
            try:
                from snid_sage.interfaces.llm.openrouter.openrouter_llm import save_openrouter_config, get_openrouter_api_key
                
                api_key = get_openrouter_api_key()
                model_name = self.model_combo.currentText()
                # Clean up status indicators from display name
                clean_name = model_name.replace("✅ ", "").replace("⏳ ", "").replace("🆓 ", "").replace("🧠 ", "")
                
                save_openrouter_config(api_key, current_data, clean_name, False)
                _LOGGER.info(f"Selected model: {clean_name} ({current_data})")
                
            except Exception as e:
                _LOGGER.error(f"Failed to save model selection: {e}")
    
    def _get_current_ai_settings(self):
        """Get current AI settings from the controls"""
        return {
            'temperature': self.temperature_spin.value(),
            'max_tokens': self.max_tokens_spin.value(),
            'model_id': self.model_combo.currentData()
        } 