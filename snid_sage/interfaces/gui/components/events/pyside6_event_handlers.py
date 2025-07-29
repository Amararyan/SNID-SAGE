"""
SNID SAGE - PySide6 Event Handlers
=================================

Dedicated event handlers for PySide6 GUI that handle all UI events including
view changes, button clicks, keyboard shortcuts, and workflow interactions.

This extracts all event handling logic from the main GUI class to keep it clean and focused.

Developed by Fiorenzo Stoppa for SNID SAGE
"""

import os
import sys
import numpy as np
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple, Callable

# PySide6 imports
import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtWidgets as QtWidgets

# Import logging
try:
    from snid_sage.shared.utils.logging import get_logger
    _LOGGER = get_logger('gui.pyside6_event_handlers')
except ImportError:
    import logging
    _LOGGER = logging.getLogger('gui.pyside6_event_handlers')


class PySide6EventHandlers(QtCore.QObject):
    """
    Handles all events for PySide6 GUI
    
    This class manages:
    - View change events (Flux/Flat toggle)
    - Button click events
    - Keyboard shortcuts
    - Dialog interactions
    - File operations
    - Workflow state changes
    - Template navigation
    """
    
    def __init__(self, main_window):
        """
        Initialize the event handlers
        
        Args:
            main_window: Reference to the main PySide6 GUI window
        """
        super().__init__()
        self.main_window = main_window
        self.app_controller = main_window.app_controller
        
        # Setup all event handlers
        self.setup_keyboard_shortcuts()
    
    def setup_keyboard_shortcuts(self):
        """Setup comprehensive keyboard shortcuts matching Tkinter GUI functionality"""
        try:
            # File operations
            QtGui.QShortcut("Ctrl+O", self.main_window, self.on_browse_file)
            QtGui.QShortcut("Ctrl+Shift+O", self.main_window, self.on_open_configuration_dialog)
            
            # Quick workflow (combined preprocessing + analysis)
            QtGui.QShortcut("Ctrl+Return", self.main_window, self.on_run_quick_workflow)
            QtGui.QShortcut("Ctrl+Enter", self.main_window, self.on_run_quick_workflow)
            
            # Extended quick workflow (preprocessing + analysis + auto cluster selection)
            QtGui.QShortcut("Ctrl+Shift+Return", self.main_window, self.on_run_quick_workflow_with_auto_cluster)
            QtGui.QShortcut("Ctrl+Shift+Enter", self.main_window, self.on_run_quick_workflow_with_auto_cluster)
            
            # Analysis operations
            QtGui.QShortcut("F5", self.main_window, self.on_run_analysis)
            QtGui.QShortcut("Ctrl+R", self.main_window, self.on_run_analysis)
            QtGui.QShortcut("F6", self.main_window, self.on_open_preprocessing_dialog)
            
            # Settings and configuration
            QtGui.QShortcut("Ctrl+,", self.main_window, self.on_open_settings_dialog)
            
            # Template navigation
            QtGui.QShortcut("Left", self.main_window, self.on_previous_template)
            QtGui.QShortcut("Right", self.main_window, self.on_next_template)
            
            
            # View toggles
            QtGui.QShortcut("F", self.main_window, lambda: self.on_view_change('flux'))
            QtGui.QShortcut("T", self.main_window, lambda: self.on_view_change('flat'))
            QtGui.QShortcut("Space", self.main_window, self.on_switch_view_mode)
            
            # Reset functionality
            QtGui.QShortcut("Ctrl+Shift+R", self.main_window, self.on_reset_to_initial_state)
            
            # Help and documentation
            QtGui.QShortcut("F1", self.main_window, self.on_show_shortcuts_dialog)
            QtGui.QShortcut("Ctrl+/", self.main_window, self.on_show_shortcuts_dialog)
            
            _LOGGER.debug("Keyboard shortcuts setup completed")
            
        except Exception as e:
            _LOGGER.error(f"Error setting up keyboard shortcuts: {e}")
    
    def on_view_change(self, view_type):
        """Handle view toggle changes"""
        try:
            _LOGGER.info(f"🔄 View change requested: {view_type}")
            
            # CRITICAL: Only prevent switching to Flat view if we don't have any spectrum data
            # or if we have spectrum data but preprocessing has never been completed
            from snid_sage.interfaces.gui.controllers.pyside6_app_controller import WorkflowState
            current_state = self.app_controller.get_current_state()
            
            # Block flat view only if:
            # 1. No spectrum loaded at all (INITIAL state), OR
            # 2. Spectrum loaded but never preprocessed (FILE_LOADED state)
            if view_type == 'flat' and current_state in [WorkflowState.INITIAL, WorkflowState.FILE_LOADED]:
                _LOGGER.warning("🚫 Flat view requested but preprocessing not completed")
                # Show warning and revert to Flux view
                QtWidgets.QMessageBox.warning(
                    self.main_window,
                    "Preprocessing Required",
                    "Flat view requires preprocessing.\n\n"
                    "Please run preprocessing first to enable flat spectrum view."
                )
                # Force Flux view
                view_type = 'flux'
            
            self.main_window.current_view = view_type
            
            # CRITICAL: Use unified layout manager for consistent button state management
            # instead of direct styling that overrides workflow state management
            if view_type == 'flux':
                # Determine if both buttons should be enabled based on workflow state
                flux_enabled = True  # Flux should be enabled after FILE_LOADED
                flat_enabled = current_state not in [WorkflowState.INITIAL, WorkflowState.FILE_LOADED]
                
                self.main_window.unified_layout_manager.update_flux_flat_button_states(
                    self.main_window,
                    flux_active=True,    # Flux becomes active
                    flat_active=False,   # Flat becomes inactive
                    flux_enabled=flux_enabled,
                    flat_enabled=flat_enabled
                )
            else:  # flat view
                # Both buttons should be enabled if we reached this point (flat view allowed)
                self.main_window.unified_layout_manager.update_flux_flat_button_states(
                    self.main_window,
                    flux_active=False,   # Flux becomes inactive
                    flat_active=True,    # Flat becomes active
                    flux_enabled=True,   # Both enabled since flat is accessible
                    flat_enabled=True
                )
            
            # IMPORTANT: Flux/Flat buttons should return to spectrum mode
            from snid_sage.interfaces.gui.components.plots.pyside6_plot_manager import PlotMode
            if self.main_window.plot_manager.current_plot_mode != PlotMode.SPECTRUM:
                _LOGGER.info("Flux/Flat button pressed - returning to spectrum mode")
                self.main_window.plot_manager.switch_to_plot_mode(PlotMode.SPECTRUM)
            
            # Always try to update plot
            # This ensures view changes are reflected immediately
            wave, flux = self.app_controller.get_spectrum_for_view(view_type)
            if wave is not None and flux is not None:
                _LOGGER.info(f"📊 Plotting spectrum in {view_type} view")
                self.main_window.plot_manager.plot_spectrum(view_type)
                
        except Exception as e:
            _LOGGER.error(f"❌ Error handling view change: {e}")
            import traceback
            traceback.print_exc()
    
    def on_switch_view_mode(self):
        """Switch between view modes (Space key)"""
        try:
            if self.main_window.current_view == 'flux':
                # Check workflow state - only block if no spectrum or spectrum never preprocessed
                from snid_sage.interfaces.gui.controllers.pyside6_app_controller import WorkflowState
                current_state = self.app_controller.get_current_state()
                
                if current_state not in [WorkflowState.INITIAL, WorkflowState.FILE_LOADED]:
                    self.on_view_change('flat')
                else:
                    _LOGGER.info("🚫 Cannot switch to Flat view - preprocessing required")
            else:
                self.on_view_change('flux')
        except Exception as e:
            _LOGGER.error(f"❌ Error switching view mode: {e}")
    
    def on_browse_file(self):
        """Handle file browsing"""
        try:
            file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
                self.main_window,
                "Load Spectrum File",
                "",
                "Spectrum Files (*.dat *.txt *.ascii *.fits);;All Files (*)"
            )
            
            if file_path:
                self.main_window.status_label.setText(f"Loading: {Path(file_path).name}")
                self.main_window.file_status_label.setText(f"File: {Path(file_path).name}")
                
                # Try to load the spectrum data using app controller
                if self.app_controller.load_spectrum_file(file_path):
                    # Reset preprocessing status for new file
                    self.main_window.preprocess_status_label.setText("Not preprocessed")
                    self.main_window.preprocess_status_label.setStyleSheet("font-style: italic; color: #475569; font-size: 10px !important; font-weight: normal !important; font-family: 'Segoe UI', Arial, sans-serif !important; line-height: 1.0 !important;")
                    
                    # CRITICAL: Ensure FILE_LOADED state is processed immediately
                    # Force call our own _update_workflow_state to make sure Flux button becomes blue
                    from snid_sage.interfaces.gui.controllers.pyside6_app_controller import WorkflowState
                    _LOGGER.info("🔧 FORCE CALLING: _update_workflow_state(FILE_LOADED) to ensure Flux button becomes blue")
                    self.main_window._update_workflow_state(WorkflowState.FILE_LOADED)
                    
                    # Plot the loaded spectrum
                    self.main_window.plot_manager.plot_spectrum(self.main_window.current_view)
                    self.main_window.status_label.setText(f"Loaded: {Path(file_path).name}")
                    
                    # CRITICAL: Re-apply button states after plotting to ensure visual appearance
                    # Sometimes the plotting operation can interfere with button styling
                    _LOGGER.info("🔧 RE-APPLYING: Button states after plotting to ensure Flux button stays blue")
                    self.main_window.unified_layout_manager.update_flux_flat_button_states(
                        self.main_window,
                        flux_active=True,    # Flux becomes active (blue)
                        flat_active=False,   # Flat stays inactive
                        flux_enabled=True,   # Flux becomes enabled
                        flat_enabled=False   # Flat stays disabled until preprocessing
                    )
                    
                    # Update file status label
                    self.main_window.file_status_label.setText(f"File: {Path(file_path).name}")
                    self.main_window.file_status_label.setStyleSheet("font-style: italic; color: #059669; font-size: 10px !important; font-weight: normal !important; font-family: 'Segoe UI', Arial, sans-serif !important; line-height: 1.0 !important;")
                    
                    _LOGGER.info(f"Spectrum file loaded successfully: {file_path}")
                else:
                    self.main_window.status_label.setText(f"Error loading file")
                    # Show error message
                    QtWidgets.QMessageBox.warning(
                        self.main_window, 
                        "File Loading Error", 
                        f"Could not load spectrum file."
                    )
                    
        except Exception as e:
            _LOGGER.error(f"Error handling file browse: {e}")
    
    def on_open_preprocessing_dialog(self):
        """Handle opening preprocessing dialog"""
        try:
            from snid_sage.interfaces.gui.components.pyside6_dialogs.preprocessing_dialog import PySide6PreprocessingDialog
            
            # Check if spectrum is loaded
            wave, flux = self.app_controller.get_spectrum_data()
            if wave is None or flux is None:
                QtWidgets.QMessageBox.warning(
                    self.main_window, 
                    "No Spectrum", 
                    "Please load a spectrum file before preprocessing."
                )
                return
            
            dialog = PySide6PreprocessingDialog(self.main_window, (wave, flux))
            result = dialog.exec()
            
            if result == QtWidgets.QDialog.Accepted:
                # Apply preprocessing results
                from snid_sage.interfaces.gui.controllers.pyside6_app_controller import WorkflowState
                self.app_controller.update_workflow_state(WorkflowState.PREPROCESSED)
                self.main_window.preprocess_status_label.setText("Preprocessed")
                self.main_window.preprocess_status_label.setStyleSheet("font-style: italic; color: #059669; font-size: 10px !important; font-weight: normal !important; font-family: 'Segoe UI', Arial, sans-serif !important; line-height: 1.0 !important;")
                self.main_window.status_label.setText("Spectrum preprocessed - Ready for analysis")
                
                # CRITICAL: Switch to Flat view to show the preprocessed (flat) spectrum  
                self.on_view_change('flat')
                _LOGGER.info("🔄 Automatically switched to Flat view after advanced preprocessing")
                
                # Update the plot to show the new processed spectrum
                self.main_window.plot_manager.plot_spectrum(self.main_window.current_view)
                
                _LOGGER.info("Preprocessing completed successfully")
            else:
                _LOGGER.debug("Preprocessing dialog cancelled")
                
        except ImportError as e:
            _LOGGER.warning(f"PySide6 preprocessing dialog not available: {e}")
            # Fallback to simple simulation
            from snid_sage.interfaces.gui.controllers.pyside6_app_controller import WorkflowState
            self.app_controller.update_workflow_state(WorkflowState.PREPROCESSED)
            self.main_window.preprocess_status_label.setText("Preprocessed")
            self.main_window.preprocess_status_label.setStyleSheet("font-style: italic; color: #059669; font-size: 10px !important; font-weight: normal !important; font-family: 'Segoe UI', Arial, sans-serif !important; line-height: 1.0 !important;")
            self.main_window.status_label.setText("Spectrum preprocessed - Ready for analysis")
            QtWidgets.QMessageBox.information(self.main_window, "Preprocessing", "Preprocessing completed (simulated).")
        except Exception as e:
            _LOGGER.error(f"Error opening preprocessing dialog: {e}")
    
    def on_run_analysis(self):
        """Handle running SNID analysis - directly open advanced configuration"""
        try:
            wave, flux = self.app_controller.get_spectrum_data()
            if wave is None or flux is None:
                QtWidgets.QMessageBox.warning(
                    self.main_window, 
                    "Analysis Error", 
                    "Please load a spectrum file before running analysis."
                )
                return
            
            # Check if spectrum is preprocessed
            if not hasattr(self.app_controller, 'processed_spectrum') or self.app_controller.processed_spectrum is None:
                # Ask user if they want to preprocess first
                reply = QtWidgets.QMessageBox.question(
                    self.main_window,
                    "Preprocessing Required",
                    "Spectrum needs to be preprocessed before analysis.\n\n"
                    "Run quick preprocessing with default settings?",
                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                    QtWidgets.QMessageBox.Yes
                )
                
                if reply == QtWidgets.QMessageBox.Yes:
                    # Run quick preprocessing first
                    success = self.app_controller.run_preprocessing()
                    if not success:
                        QtWidgets.QMessageBox.critical(
                            self.main_window,
                            "Preprocessing Error",
                            "Failed to preprocess spectrum"
                        )
                        return
                else:
                    return  # User cancelled
            
            # Directly open configuration dialog for advanced options
            try:
                from snid_sage.interfaces.gui.components.pyside6_dialogs.configuration_dialog import show_configuration_dialog
                
                # Get current parameters if available
                current_params = {}
                if hasattr(self.app_controller, 'current_config'):
                    current_params = self.app_controller.current_config.get('analysis', {})
                
                # Show configuration dialog
                dialog_result = show_configuration_dialog(self.main_window, current_params, self.app_controller)
                
                if dialog_result is None:
                    # User cancelled configuration
                    _LOGGER.debug("Analysis configuration cancelled")
                    return
                
                config_params, analysis_started = dialog_result
                
                if analysis_started:
                    # Analysis was already started from the dialog - no need to run it again
                    _LOGGER.info("Analysis already started from configuration dialog")
                    return
                
                # Update status
                self.main_window.status_label.setText("Running SNID analysis with configured settings...")
                
                # Apply configuration and run analysis
                if hasattr(self.app_controller, 'current_config'):
                    if 'analysis' not in self.app_controller.current_config:
                        self.app_controller.current_config['analysis'] = {}
                    self.app_controller.current_config['analysis'].update(config_params)
                
                # Run the analysis with configured parameters
                success = self._run_configured_analysis(config_params)
                
                if success:
                    # Analysis completed successfully - enable advanced features
                    from snid_sage.interfaces.gui.controllers.pyside6_app_controller import WorkflowState
                    self.app_controller.update_workflow_state(WorkflowState.ANALYSIS_COMPLETE)
                    self.main_window.status_label.setText("SNID analysis completed successfully")
                    
                    # Enable analysis plot buttons
                    for btn in self.main_window.analysis_plot_buttons:
                        btn.setEnabled(True)
                    for btn in self.main_window.nav_buttons:
                        btn.setEnabled(True)
                    
                    # Enable advanced features
                    self.main_window.emission_line_overlay_btn.setEnabled(True)
                    self.main_window.ai_assistant_btn.setEnabled(True)
                    
                    _LOGGER.info("SNID analysis completed successfully")
                else:
                    QtWidgets.QMessageBox.critical(
                        self.main_window,
                        "Analysis Error",
                        "Failed to run SNID analysis with configured parameters"
                    )
                    
            except ImportError as e:
                _LOGGER.error(f"Configuration dialog not available: {e}")
                QtWidgets.QMessageBox.critical(
                    self.main_window,
                    "Configuration Error",
                    "Configuration dialog is not available"
                )
                
        except Exception as e:
            _LOGGER.error(f"Error running analysis: {e}")
            QtWidgets.QMessageBox.critical(
                self.main_window,
                "Analysis Error",
                f"Failed to run analysis:\n{str(e)}"
            )
    
    def _run_configured_analysis(self, config_params):
        """Run SNID analysis with configured parameters"""
        try:
            # Check if we have an analysis controller
            if hasattr(self.app_controller, 'run_snid_analysis'):
                return self.app_controller.run_snid_analysis(config_params)
            else:
                # Show error if analysis controller is not available
                _LOGGER.error("Analysis controller not available - cannot run analysis")
                QtWidgets.QMessageBox.critical(
                    self.main_window,
                    "Analysis Error",
                    "Analysis controller not available.\nPlease check the application setup."
                )
                return False
        except Exception as e:
            _LOGGER.error(f"Error running configured analysis: {e}")
            QtWidgets.QMessageBox.critical(
                self.main_window,
                "Analysis Error",
                f"Error running analysis:\n{str(e)}"
            )
            return False

    def on_run_quick_workflow(self):
        """Handle quick workflow (simulate right-click preprocessing + right-click analysis)"""
        try:
            _LOGGER.info("Starting quick workflow (simulating right-click on preprocessing + analysis buttons)")
            
            # Check if spectrum is loaded
            wave, flux = self.app_controller.get_spectrum_data()
            if wave is None or flux is None:
                QtWidgets.QMessageBox.warning(
                    self.main_window, 
                    "No Spectrum", 
                    "Please load a spectrum file before running quick workflow."
                )
                return
            
            # Simulate right-click on preprocessing button (quick preprocessing)
            if hasattr(self.main_window, 'preprocessing_controller') and hasattr(self.main_window.preprocessing_controller, 'run_quick_preprocessing'):
                _LOGGER.info("🔧 Simulating right-click on preprocessing button...")
                self.main_window.preprocessing_controller.run_quick_preprocessing()
            else:
                _LOGGER.warning("Quick preprocessing not available")
                return
            
            # Simulate right-click on analysis button (quick analysis)
            if hasattr(self.main_window, 'run_quick_analysis'):
                _LOGGER.info("🚀 Simulating right-click on analysis button...")
                self.main_window.run_quick_analysis()
            else:
                _LOGGER.warning("Quick analysis not available")
                return
            
        except Exception as e:
            _LOGGER.error(f"Error in quick workflow: {e}")

    def on_run_quick_workflow_with_auto_cluster(self):
        """Handle extended quick workflow (simulate right-click preprocessing + right-click analysis + auto cluster selection)"""
        try:
            _LOGGER.info("Starting extended quick workflow (simulating right-click on buttons + auto cluster)")
            
            # Check if spectrum is loaded
            wave, flux = self.app_controller.get_spectrum_data()
            if wave is None or flux is None:
                QtWidgets.QMessageBox.warning(
                    self.main_window, 
                    "No Spectrum", 
                    "Please load a spectrum file before running extended quick workflow."
                )
                return
            
            # Set flag to automatically select best cluster
            self.app_controller.auto_select_best_cluster = True
            _LOGGER.info("🤖 Auto cluster selection enabled")
            
            # Simulate right-click on preprocessing button (quick preprocessing)
            if hasattr(self.main_window, 'preprocessing_controller') and hasattr(self.main_window.preprocessing_controller, 'run_quick_preprocessing'):
                _LOGGER.info("🔧 Simulating right-click on preprocessing button...")
                self.main_window.preprocessing_controller.run_quick_preprocessing()
            else:
                _LOGGER.warning("Quick preprocessing not available")
                # Reset the auto select flag on error
                self.app_controller.auto_select_best_cluster = False
                return
            
            # Simulate right-click on analysis button (quick analysis with auto cluster)
            if hasattr(self.main_window, 'run_quick_analysis'):
                _LOGGER.info("🚀 Simulating right-click on analysis button (with auto cluster)...")
                self.main_window.run_quick_analysis()
            else:
                _LOGGER.warning("Quick analysis not available")
                # Reset the auto select flag on error
                self.app_controller.auto_select_best_cluster = False
                return
            
        except Exception as e:
            _LOGGER.error(f"Error in extended quick workflow: {e}")
            # Reset the auto select flag on error
            self.app_controller.auto_select_best_cluster = False
    
    def on_reset_to_initial_state(self):
        """Handle reset to initial state"""
        try:
            reply = QtWidgets.QMessageBox.question(
                self.main_window, 
                "Reset Application", 
                "Are you sure you want to reset to initial state?\nThis will clear all data and analysis results.",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
                QtWidgets.QMessageBox.No
            )
            
            if reply == QtWidgets.QMessageBox.Yes:
                self.app_controller.reset_to_initial_state()
                self.main_window.status_label.setText("Application reset to initial state")
                self.main_window.plot_manager.plot_pyqtgraph_welcome_message()
                _LOGGER.info("Application reset to initial state")
                
        except Exception as e:
            _LOGGER.error(f"Error resetting application: {e}")
    
    def on_previous_template(self):
        """Handle previous template navigation"""
        try:
            if hasattr(self.app_controller, 'snid_results') and self.app_controller.snid_results:
                current_idx = getattr(self.app_controller, 'current_template', 0)
                max_templates = len(self.app_controller.snid_results.best_matches)
                
                if current_idx > 0:
                    self.app_controller.current_template = current_idx - 1
                    self.main_window.plot_manager.plot_spectrum(self.main_window.current_view)
                    _LOGGER.debug(f"Moved to previous template: {self.app_controller.current_template}")
                    
        except Exception as e:
            _LOGGER.error(f"Error navigating to previous template: {e}")
    
    def on_next_template(self):
        """Handle next template navigation"""
        try:
            if hasattr(self.app_controller, 'snid_results') and self.app_controller.snid_results:
                current_idx = getattr(self.app_controller, 'current_template', 0)
                max_templates = len(self.app_controller.snid_results.best_matches)
                
                if current_idx < max_templates - 1:
                    self.app_controller.current_template = current_idx + 1
                    self.main_window.plot_manager.plot_spectrum(self.main_window.current_view)
                    _LOGGER.debug(f"Moved to next template: {self.app_controller.current_template}")
                    
        except Exception as e:
            _LOGGER.error(f"Error navigating to next template: {e}")
    

    
    def on_open_configuration_dialog(self):
        """Handle opening configuration dialog"""
        try:
            # Implementation for configuration dialog
            QtWidgets.QMessageBox.information(
                self.main_window,
                "Configuration",
                "Configuration dialog will be implemented."
            )
        except Exception as e:
            _LOGGER.error(f"Error opening configuration dialog: {e}")
    
    def on_open_settings_dialog(self):
        """Handle opening settings dialog"""
        try:
            # Implementation for settings dialog
            QtWidgets.QMessageBox.information(
                self.main_window,
                "Settings",
                "Settings dialog will be implemented."
            )
        except Exception as e:
            _LOGGER.error(f"Error opening settings dialog: {e}")
    
    def on_show_shortcuts_dialog(self):
        """Handle showing keyboard shortcuts dialog"""
        try:
            shortcuts_text = """
            <h3>Keyboard Shortcuts</h3>
            <p><b>File Operations:</b></p>
            <ul>
            <li>Ctrl+O : Load spectrum file</li>
            <li>Ctrl+Shift+O : Open configuration</li>
            </ul>
            <p><b>Workflow:</b></p>
            <ul>
            <li>F6 : Open preprocessing dialog</li>
                         <li>Ctrl+Enter : Quick workflow (simulate right-click preprocessing + analysis)</li>
             <li>Ctrl+Shift+Enter : Extended quick workflow (right-click preprocessing + analysis + auto-select best cluster)</li>
            <li>Ctrl+Shift+R : Reset to initial state</li>
            </ul>
            <p><b>View Controls:</b></p>
            <ul>
            <li>F : Switch to Flux view</li>
            <li>T : Switch to Flat view</li>
            <li>Space : Toggle between views</li>
            </ul>
            <p><b>Template Navigation:</b></p>
            <ul>
            <li>Left/Right : Previous/Next template</li>
            <li>Up/Down : Move template up/down</li>
            </ul>
            <p><b>Analysis:</b></p>
            <ul>
            <li>Ctrl+O : Load spectrum file</li>
            <li>Ctrl+R : Run analysis</li>
            <li>Ctrl+, : Open settings</li>
            </ul>
            <p><b>Help:</b></p>
            <ul>
            <li>F1 or Ctrl+/ : Show this help</li>
            </ul>
            """
            
            msg = QtWidgets.QMessageBox(self.main_window)
            msg.setWindowTitle("Keyboard Shortcuts")
            msg.setTextFormat(QtCore.Qt.RichText)
            msg.setText(shortcuts_text)
            msg.exec_()
            
            _LOGGER.debug("Shortcuts dialog shown")
        except Exception as e:
            _LOGGER.error(f"Error showing shortcuts dialog: {e}") 