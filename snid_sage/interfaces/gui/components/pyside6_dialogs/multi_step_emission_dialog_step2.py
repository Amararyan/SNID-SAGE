"""
PySide6 Multi-Step SN Emission Line Analysis Dialog - Step 2 (Peak Analysis)
===========================================================================

This module contains all the Step 2 analysis functionality for the emission line dialog.
Separated from the main dialog to keep the code organized and manageable.

Step 2 Features:
- Line selection and navigation
- Peak analysis methods (Auto Detection, Gaussian Fit, Empirical Analysis, Manual Points)
- FWHM measurements
- Line fitting and analysis
- Results export
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Any
from PySide6 import QtWidgets, QtCore, QtGui

# PyQtGraph for plotting
try:
    import pyqtgraph as pg
    PYQTGRAPH_AVAILABLE = True
except ImportError:
    PYQTGRAPH_AVAILABLE = False
    pg = None

# Enhanced interactive analysis (scipy for peak analysis)
try:
    from scipy import signal
    from scipy.optimize import curve_fit
    SCIPY_AVAILABLE = True
except ImportError:
    SCIPY_AVAILABLE = False

# Import logging
try:
    from snid_sage.shared.utils.logging import get_logger
    _LOGGER = get_logger('gui.pyside6_emission_step2')
except ImportError:
    import logging
    _LOGGER = logging.getLogger('gui.pyside6_emission_step2')


class EmissionLineStep2Analysis:
    """
    Step 2 analysis functionality for emission line peak analysis and FWHM measurements.
    This class handles all the complex analysis methods separated from the main dialog.
    """
    
    def __init__(self, parent_dialog):
        """Initialize Step 2 analysis with reference to parent dialog"""
        self.parent = parent_dialog
        self.spectrum_data = parent_dialog.spectrum_data
        self.colors = parent_dialog.colors
        
        # Step 2 specific data
        self.available_lines = []
        self.current_line_index = 0
        self.line_analysis_results = {}
        self.selected_manual_points = []
        self.line_fit_results = {}
        
        # UI components (will be set by parent)
        self.line_dropdown = None
        self.method_combo = None
        self.line_counter_label = None
        self.current_result_text = None
        self.summary_text = None
        
    def create_step_2_interface(self, layout):
        """Create Step 2 peak analysis interface (simplified - only Manual Points method)"""
        # Description
        desc = QtWidgets.QLabel(
            "Manual point selection for emission line analysis. "
            "Use the toolbar above to navigate lines and adjust zoom level."
        )
        desc.setWordWrap(True)
        desc.setStyleSheet(f"color: {self.colors['text_secondary']}; margin-bottom: 10px;")
        layout.addWidget(desc)
        
        # Manual Points Instructions (always visible since it's the only method)
        self.manual_instructions = QtWidgets.QLabel(
            "Manual Selection Instructions:\n"
            "• Left Click: Smart peak detection\n"
            "• Ctrl+Click: Add free-floating point\n"
            "• Shift+Click: Add spectrum-snapped point\n" 
            "• Right Click: Remove closest point"
        )
        self.manual_instructions.setWordWrap(True)
        self.manual_instructions.setStyleSheet(f"color: {self.colors.get('text_secondary', '#666')}; padding: 5px;")
        layout.addWidget(self.manual_instructions)
        
        # Manual point controls
        manual_controls = QtWidgets.QHBoxLayout()
        
        self.clear_points_btn = QtWidgets.QPushButton("Clear Points")
        self.clear_points_btn.clicked.connect(self.clear_selected_points)
        manual_controls.addWidget(self.clear_points_btn)
        
        self.auto_contour_btn = QtWidgets.QPushButton("Auto Contour")
        self.auto_contour_btn.clicked.connect(self.auto_detect_contour)
        manual_controls.addWidget(self.auto_contour_btn)
        
        self.point_counter_label = QtWidgets.QLabel("Points: 0")
        manual_controls.addWidget(self.point_counter_label)
        
        manual_controls.addStretch()
        layout.addLayout(manual_controls)
        
        # Current results display
        analysis_group = QtWidgets.QGroupBox("📊 Current Line Analysis")
        analysis_layout = QtWidgets.QVBoxLayout(analysis_group)
        
        self.current_result_text = QtWidgets.QTextEdit()
        self.current_result_text.setMaximumHeight(100)
        self.current_result_text.setReadOnly(True)
        self.current_result_text.setPlainText("Select a line and click 'Analyze' in the toolbar above...")
        analysis_layout.addWidget(self.current_result_text)
        
        layout.addWidget(analysis_group)
        
        # All Lines Summary
        summary_group = QtWidgets.QGroupBox("📋 All Lines Summary")
        summary_layout = QtWidgets.QVBoxLayout(summary_group)
        
        summary_controls = QtWidgets.QHBoxLayout()
        
        copy_summary_btn = QtWidgets.QPushButton("Copy Summary")
        copy_summary_btn.clicked.connect(self.copy_summary)
        summary_controls.addWidget(copy_summary_btn)
        
        refresh_summary_btn = QtWidgets.QPushButton("Refresh")
        refresh_summary_btn.clicked.connect(self.refresh_summary)
        summary_controls.addWidget(refresh_summary_btn)
        
        export_btn = QtWidgets.QPushButton("💾 Export Results")
        export_btn.clicked.connect(self.export_results)
        summary_controls.addWidget(export_btn)
        
        summary_controls.addStretch()
        summary_layout.addLayout(summary_controls)
        
        self.summary_text = QtWidgets.QTextEdit()
        self.summary_text.setMaximumHeight(150)
        self.summary_text.setReadOnly(True)
        summary_layout.addWidget(self.summary_text)
        
        layout.addWidget(summary_group)
        
        # Initialize - will be properly connected by parent
        self.populate_line_dropdown()
        # No method visibility update needed since only Manual Points is supported
    
    def populate_line_dropdown(self):
        """Populate line dropdown with available lines"""
        self.line_dropdown.clear()
        self.available_lines = []
        
        # Add SN lines
        for line_name in self.parent.sn_lines.keys():
            self.available_lines.append(('sn', line_name))
            self.line_dropdown.addItem(f"🌟 {line_name}")
        
        # Add Galaxy lines
        for line_name in self.parent.galaxy_lines.keys():
            self.available_lines.append(('galaxy', line_name))
            self.line_dropdown.addItem(f"🌌 {line_name}")
        
        self.update_line_counter()
        self.update_line_navigation_buttons()
    
    def on_line_selection_changed(self, text):
        """Handle line selection change"""
        if not text or not self.available_lines:
            return
        
        # Find the index of the selected line
        for i, (line_type, line_name) in enumerate(self.available_lines):
            display_name = f"{'🌟' if line_type == 'sn' else '🌌'} {line_name}"
            if display_name == text:
                self.current_line_index = i
                break
        
        self.update_line_counter()
        self.plot_focused_line()
    
    def previous_line(self):
        """Go to previous line"""
        if self.current_line_index > 0:
            self.current_line_index -= 1
            self.update_line_selection()
    
    def next_line(self):
        """Go to next line"""
        if self.current_line_index < len(self.available_lines) - 1:
            self.current_line_index += 1
            self.update_line_selection()
    
    def update_line_selection(self):
        """Update line selection in dropdown"""
        if self.available_lines and 0 <= self.current_line_index < len(self.available_lines):
            line_type, line_name = self.available_lines[self.current_line_index]
            display_name = f"{'🌟' if line_type == 'sn' else '🌌'} {line_name}"
            self.line_dropdown.setCurrentText(display_name)
            self.update_line_counter()
            self.plot_focused_line()
    
    def update_line_counter(self):
        """Update line counter display"""
        total_lines = len(self.available_lines)
        current = self.current_line_index + 1 if total_lines > 0 else 0
        self.line_counter_label.setText(f"Line {current} of {total_lines}")
    
    def update_line_navigation_buttons(self):
        """Update navigation button states"""
        has_lines = len(self.available_lines) > 0
        self.prev_line_btn.setEnabled(has_lines and self.current_line_index > 0)
        self.next_line_btn.setEnabled(has_lines and self.current_line_index < len(self.available_lines) - 1)
    
    def on_zoom_changed(self, value):
        """Handle zoom range change with fixed zoom value of 100"""
        # Fixed zoom value of 100 Å - always plot focused line
        self.plot_focused_line()
    
    def show_full_spectrum(self):
        """Show full spectrum view with all lines marked"""
        if not PYQTGRAPH_AVAILABLE or not self.parent.plot_item:
            return
        
        # Use parent's full spectrum plotting method
        self.parent._update_plot()
    
    def on_method_changed(self, method_text):
        """Handle analysis method change"""
        self.update_method_visibility()
    
    def update_method_visibility(self):
        """Update visibility of method-specific controls (simplified for Manual Points only)"""
        # Since we only support Manual Points, always show manual controls
        if hasattr(self, 'manual_instructions') and self.manual_instructions:
            self.manual_instructions.setVisible(True)
        if hasattr(self, 'clear_points_btn') and self.clear_points_btn:
            self.clear_points_btn.setVisible(True)
        if hasattr(self, 'auto_contour_btn') and self.auto_contour_btn:
            self.auto_contour_btn.setVisible(True)
        if hasattr(self, 'point_counter_label') and self.point_counter_label:
            self.point_counter_label.setVisible(True)
    
    def clear_selected_points(self):
        """Clear manually selected points"""
        self.selected_manual_points.clear()
        self.update_point_counter()
        self.plot_focused_line()  # Refresh plot
    
    def auto_detect_contour(self):
        """Auto-detect contour points around current line"""
        if not self.available_lines or not SCIPY_AVAILABLE:
            return
        
        try:
            # Get current line info
            line_type, line_name = self.available_lines[self.current_line_index]
            line_collection = self.parent.sn_lines if line_type == 'sn' else self.parent.galaxy_lines
            obs_wavelength, line_data = line_collection[line_name]
            
            # Get spectrum data around the line
            wave = self.spectrum_data.get('wave', np.array([]))
            flux = self.spectrum_data.get('flux', np.array([]))
            
            if len(wave) == 0 or len(flux) == 0:
                return
            
            # Find region around line
            zoom_range = 100  # Fixed zoom value
            mask = (wave >= obs_wavelength - zoom_range) & (wave <= obs_wavelength + zoom_range)
            
            if not np.any(mask):
                return
            
            region_wave = wave[mask]
            region_flux = flux[mask]
            
            # Simple peak detection
            peaks, _ = signal.find_peaks(region_flux, height=np.median(region_flux))
            
            # Add detected points
            self.selected_manual_points.clear()
            for peak_idx in peaks:
                self.selected_manual_points.append((region_wave[peak_idx], region_flux[peak_idx]))
            
            self.update_point_counter()
            self.plot_focused_line()
            
        except Exception as e:
            _LOGGER.error(f"Error in auto contour detection: {e}")
    
    def update_point_counter(self):
        """Update manual point counter"""
        count = len(self.selected_manual_points)
        self.point_counter_label.setText(f"Points: {count}")
    
    def analyze_current_line(self):
        """Analyze the currently selected line using Manual Points method"""
        if not self.available_lines:
            self.current_result_text.setPlainText("No lines available for analysis.")
            return
        
        try:
            # Get current line info
            line_type, line_name = self.available_lines[self.current_line_index]
            line_collection = self.parent.sn_lines if line_type == 'sn' else self.parent.galaxy_lines
            obs_wavelength, line_data = line_collection[line_name]
            
            # Always use Manual Points method (only method available)
            result = self.analyze_manual_points(line_name, obs_wavelength)
            
            # Store and display result
            self.line_analysis_results[line_name] = result
            self.update_current_result_display(result)
            self.refresh_summary()
            
        except Exception as e:
            error_msg = f"Error analyzing line: {e}"
            self.current_result_text.setPlainText(error_msg)
            _LOGGER.error(error_msg)
    
    def analyze_manual_points(self, line_name, obs_wavelength):
        """Analyze line using manual points"""
        if not self.selected_manual_points:
            return {"error": "No manual points selected"}
        
        # Simple analysis of manual points
        wavelengths = [p[0] for p in self.selected_manual_points]
        fluxes = [p[1] for p in self.selected_manual_points]
        
        result = {
            "method": "Manual Points",
            "line_name": line_name,
            "observed_wavelength": obs_wavelength,
            "num_points": len(self.selected_manual_points),
            "wavelength_range": f"{min(wavelengths):.2f} - {max(wavelengths):.2f} Å",
            "flux_range": f"{min(fluxes):.3f} - {max(fluxes):.3f}",
            "peak_flux": max(fluxes),
            "peak_wavelength": wavelengths[fluxes.index(max(fluxes))]
        }
        
        return result
    
    def analyze_auto_detection(self, line_name, obs_wavelength):
        """Analyze line using auto detection"""
        return {
            "method": "Auto Detection",
            "line_name": line_name,
            "observed_wavelength": obs_wavelength,
            "status": "Not implemented yet"
        }
    
    def analyze_gaussian_fit(self, line_name, obs_wavelength):
        """Analyze line using Gaussian fitting"""
        return {
            "method": "Gaussian Fit",
            "line_name": line_name,
            "observed_wavelength": obs_wavelength,
            "status": "Not implemented yet"
        }
    
    def analyze_empirical(self, line_name, obs_wavelength):
        """Analyze line using empirical methods"""
        return {
            "method": "Empirical Analysis",
            "line_name": line_name,
            "observed_wavelength": obs_wavelength,
            "status": "Not implemented yet"
        }
    
    def update_current_result_display(self, result):
        """Update current result display"""
        if "error" in result:
            self.current_result_text.setPlainText(f"Error: {result['error']}")
            return
        
        # Format result for display
        text_lines = [
            f"Line: {result.get('line_name', 'Unknown')}",
            f"Method: {result.get('method', 'Unknown')}",
            f"Observed λ: {result.get('observed_wavelength', 0):.2f} Å"
        ]
        
        if "num_points" in result:
            text_lines.append(f"Points: {result['num_points']}")
        if "wavelength_range" in result:
            text_lines.append(f"λ Range: {result['wavelength_range']}")
        if "peak_flux" in result:
            text_lines.append(f"Peak Flux: {result['peak_flux']:.3f}")
        if "peak_wavelength" in result:
            text_lines.append(f"Peak λ: {result['peak_wavelength']:.2f} Å")
        if "status" in result:
            text_lines.append(f"Status: {result['status']}")
        
        self.current_result_text.setPlainText("\n".join(text_lines))
    
    def copy_summary(self):
        """Copy summary to clipboard"""
        QtWidgets.QApplication.clipboard().setText(self.summary_text.toPlainText())
    
    def refresh_summary(self):
        """Refresh the analysis summary"""
        if not self.line_analysis_results:
            self.summary_text.setPlainText("No analysis results yet.")
            return
        
        summary_lines = ["=== Emission Line Analysis Summary ===\n"]
        
        for line_name, result in self.line_analysis_results.items():
            summary_lines.append(f"• {line_name}:")
            summary_lines.append(f"  Method: {result.get('method', 'Unknown')}")
            if "peak_wavelength" in result:
                summary_lines.append(f"  Peak λ: {result['peak_wavelength']:.2f} Å")
            if "peak_flux" in result:
                summary_lines.append(f"  Peak Flux: {result['peak_flux']:.3f}")
            summary_lines.append("")
        
        summary_lines.append(f"Total lines analyzed: {len(self.line_analysis_results)}")
        
        self.summary_text.setPlainText("\n".join(summary_lines))
    
    def export_results(self):
        """Export analysis results to file"""
        if not self.line_analysis_results:
            QtWidgets.QMessageBox.information(
                self.parent, "No Results",
                "No analysis results to export."
            )
            return
        
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self.parent,
            "Export Analysis Results",
            "emission_line_analysis.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write("Emission Line Analysis Results\n")
                    f.write("=" * 40 + "\n\n")
                    
                    for line_name, result in self.line_analysis_results.items():
                        f.write(f"Line: {line_name}\n")
                        for key, value in result.items():
                            if key != 'line_name':
                                f.write(f"  {key}: {value}\n")
                        f.write("\n")
                
                QtWidgets.QMessageBox.information(
                    self.parent, "Export Complete",
                    f"Results exported to:\n{file_path}"
                )
                
            except Exception as e:
                QtWidgets.QMessageBox.critical(
                    self.parent, "Export Error",
                    f"Failed to export results:\n{str(e)}"
                )
    
    def plot_focused_line(self):
        """Plot focused view of current line with fixed zoom value of 100"""
        if not PYQTGRAPH_AVAILABLE or not self.parent.plot_item or not self.available_lines:
            return
        
        try:
            # Get current line info
            line_type, line_name = self.available_lines[self.current_line_index]
            line_collection = self.parent.sn_lines if line_type == 'sn' else self.parent.galaxy_lines
            obs_wavelength, line_data = line_collection[line_name]
            
            # Fixed zoom value of 100 Å
            zoom_range = 100
            
            # Get spectrum data
            wave = self.spectrum_data.get('wave', np.array([]))
            flux = self.spectrum_data.get('flux', np.array([]))
            
            if len(wave) == 0 or len(flux) == 0:
                return
            
            # Clear and start fresh plot
            self.parent.plot_item.clear()
            
            # Always plot the full spectrum first (in light gray)
            self.parent.plot_item.plot(wave, flux, pen=pg.mkPen(color='lightgray', width=1), name='Full Spectrum')
            
            # Create focused plot region mask
            mask = (wave >= obs_wavelength - zoom_range) & (wave <= obs_wavelength + zoom_range)
            
            if np.any(mask):
                # Plot focused region in darker color
                focused_wave = wave[mask]
                focused_flux = flux[mask]
                self.parent.plot_item.plot(focused_wave, focused_flux, pen=pg.mkPen(color='black', width=2), name='Focused Region')
                
                # Set view range to focused area
                self.parent.plot_widget.setXRange(obs_wavelength - zoom_range, obs_wavelength + zoom_range)
                
                # Set Y range to focused region with some padding
                if len(focused_flux) > 0:
                    flux_min, flux_max = np.min(focused_flux), np.max(focused_flux)
                    flux_padding = (flux_max - flux_min) * 0.1
                    self.parent.plot_widget.setYRange(flux_min - flux_padding, flux_max + flux_padding)
            
            # Plot the central line marker
            line_color = 'red' if line_type == 'sn' else 'blue'
            line_marker = pg.InfiniteLine(
                pos=obs_wavelength,
                angle=90,
                pen=pg.mkPen(color=line_color, width=3),
                label=line_name
            )
            self.parent.plot_item.addItem(line_marker)
            
            # Plot manual points if any
            if self.selected_manual_points:
                point_waves = [p[0] for p in self.selected_manual_points]
                point_fluxes = [p[1] for p in self.selected_manual_points]
                scatter = pg.ScatterPlotItem(
                    x=point_waves, 
                    y=point_fluxes,
                    size=10,
                    brush='orange',
                    pen=pg.mkPen(color='red', width=2)
                )
                self.parent.plot_item.addItem(scatter)
            
        except Exception as e:
            _LOGGER.error(f"Error plotting focused line: {e}") 