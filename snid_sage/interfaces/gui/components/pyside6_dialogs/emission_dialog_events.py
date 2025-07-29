"""
Event Handlers for PySide6 Multi-Step Emission Line Analysis Dialog
==================================================================

This module contains all event handling methods for the emission line dialog,
separated from the main dialog class to reduce file size and improve organization.
"""

from typing import Dict, Any
from PySide6 import QtCore, QtWidgets

# Import logging
try:
    from snid_sage.shared.utils.logging import get_logger
    _LOGGER = get_logger('gui.emission_dialog_events')
except ImportError:
    import logging
    _LOGGER = logging.getLogger('gui.emission_dialog_events')

# Import line detection functions
try:
    from snid_sage.shared.utils.line_detection.line_presets import (
        get_type_ia_lines,
        get_type_ii_lines,
        get_type_ibc_lines,
        get_type_iin_lines,
        get_type_iib_lines,
        get_hydrogen_lines,
        get_helium_lines,
        get_silicon_lines,
        get_iron_lines,
        get_calcium_lines,
        get_oxygen_lines,
        get_balmer_lines,
        get_fe_ii_lines,
        get_fe_iii_lines,
        get_early_sn_lines,
        get_maximum_lines,
        get_late_phase_lines,
        get_nebular_lines,
        get_main_galaxy_lines,
        get_very_strong_lines,
        get_strong_lines,
        get_diagnostic_lines,
        get_common_lines,
        get_emission_lines,
        get_flash_lines,
        get_interaction_lines
    )
    LINE_DETECTION_AVAILABLE = True
except ImportError as e:
    LINE_DETECTION_AVAILABLE = False
    _LOGGER.warning(f"Line detection utilities not available: {e}")


class EmissionDialogEventHandlers:
    """Event handler class for emission line dialog actions"""
    
    def __init__(self, dialog):
        """Initialize with reference to the main dialog"""
        self.dialog = dialog
    
    def _get_normalized_spectrum_data(self):
        """Get spectrum data in the format expected by line preset functions"""
        spectrum_data = self.dialog.spectrum_data.copy()
        
        # Ensure the spectrum data has 'wavelength' key for filtering
        if 'wave' in spectrum_data and 'wavelength' not in spectrum_data:
            spectrum_data['wavelength'] = spectrum_data['wave']
        
        return spectrum_data
    
    def on_sn_type_preset_selected(self, text):
        """Handle SN type preset selection"""
        if text == "Select Type..." or text.startswith("Choose"):
            return
            
        try:
            spectrum_data = self._get_normalized_spectrum_data()
            
            if text == "Type Ia":
                lines = get_type_ia_lines(self.dialog.host_redshift, spectrum_data)
                self.dialog._add_lines_to_plot(lines, is_sn=True)
            elif text == "Type II":
                lines = get_type_ii_lines(self.dialog.host_redshift, spectrum_data)
                self.dialog._add_lines_to_plot(lines, is_sn=True)
            elif text == "Type Ib/c":
                lines = get_type_ibc_lines(self.dialog.host_redshift, spectrum_data)
                self.dialog._add_lines_to_plot(lines, is_sn=True)
            elif text == "Type IIn":
                lines = get_type_iin_lines(self.dialog.host_redshift, spectrum_data)
                self.dialog._add_lines_to_plot(lines, is_sn=True)
            elif text == "Type IIb":
                lines = get_type_iib_lines(self.dialog.host_redshift, spectrum_data)
                self.dialog._add_lines_to_plot(lines, is_sn=True)
                
            # Keep selections visible - don't reset dropdown
            
        except Exception as e:
            _LOGGER.error(f"Error applying SN type preset '{text}': {e}")
    
    def on_sn_phase_preset_selected(self, text):
        """Handle SN phase preset selection"""
        if text == "Select Phase..." or text.startswith("Choose"):
            return
            
        try:
            spectrum_data = self._get_normalized_spectrum_data()
            
            if text == "Early Phase":
                lines = get_early_sn_lines(self.dialog.host_redshift, spectrum_data)
                self.dialog._add_lines_to_plot(lines, is_sn=True)
            elif text == "Maximum Light":
                lines = get_maximum_lines(self.dialog.host_redshift, spectrum_data)
                self.dialog._add_lines_to_plot(lines, is_sn=True)
            elif text == "Late Phase":
                lines = get_late_phase_lines(self.dialog.host_redshift, spectrum_data)
                self.dialog._add_lines_to_plot(lines, is_sn=True)
            elif text == "Nebular Phase":
                lines = get_nebular_lines(self.dialog.host_redshift, spectrum_data)
                self.dialog._add_lines_to_plot(lines, is_sn=True)
                
            # Keep selections visible - don't reset dropdown
            
        except Exception as e:
            _LOGGER.error(f"Error applying SN phase preset '{text}': {e}")
    
    def on_element_preset_selected(self, text):
        """Handle element preset selection"""
        if text == "Select Element..." or text.startswith("Choose"):
            return
            
        try:
            spectrum_data = self._get_normalized_spectrum_data()
            
            if text == "Hydrogen":
                lines = get_hydrogen_lines(self.dialog.host_redshift, spectrum_data)
                self.dialog._add_lines_to_plot(lines, is_sn=True)
            elif text == "Helium":
                lines = get_helium_lines(self.dialog.host_redshift, spectrum_data)
                self.dialog._add_lines_to_plot(lines, is_sn=True)
            elif text == "Silicon":
                lines = get_silicon_lines(self.dialog.host_redshift, spectrum_data)
                self.dialog._add_lines_to_plot(lines, is_sn=True)
            elif text == "Iron":
                lines = get_iron_lines(self.dialog.host_redshift, spectrum_data)
                self.dialog._add_lines_to_plot(lines, is_sn=True)
            elif text == "Calcium":
                lines = get_calcium_lines(self.dialog.host_redshift, spectrum_data)
                self.dialog._add_lines_to_plot(lines, is_sn=True)
            elif text == "Oxygen":
                lines = get_oxygen_lines(self.dialog.host_redshift, spectrum_data)
                self.dialog._add_lines_to_plot(lines, is_sn=True)
            elif text == "Balmer Series":
                lines = get_balmer_lines(self.dialog.host_redshift, spectrum_data)
                self.dialog._add_lines_to_plot(lines, is_sn=True)
            elif text == "Fe II":
                lines = get_fe_ii_lines(self.dialog.host_redshift, spectrum_data)
                self.dialog._add_lines_to_plot(lines, is_sn=True)
            elif text == "Fe III":
                lines = get_fe_iii_lines(self.dialog.host_redshift, spectrum_data)
                self.dialog._add_lines_to_plot(lines, is_sn=True)
        except Exception as e:
            _LOGGER.error(f"Error selecting element preset {text}: {e}")
    
    def on_other_preset_selected(self, text):
        """Handle other preset selection"""
        if text == "Select Preset..." or text.startswith("Choose"):
            return
            
        try:
            spectrum_data = self._get_normalized_spectrum_data()
            
            if text == "Main Galaxy Lines":
                lines = get_main_galaxy_lines(self.dialog.host_redshift, spectrum_data)
                self.dialog._add_lines_to_plot(lines, is_sn=False)
            elif text == "Very Strong Lines":
                lines = get_very_strong_lines(self.dialog.host_redshift, spectrum_data)
                self.dialog._add_lines_to_plot(lines, is_sn=False)
            elif text == "Strong Lines":
                lines = get_strong_lines(self.dialog.host_redshift, spectrum_data)
                self.dialog._add_lines_to_plot(lines, is_sn=False)
            elif text == "Diagnostic Lines":
                lines = get_diagnostic_lines(self.dialog.host_redshift, spectrum_data)
                self.dialog._add_lines_to_plot(lines, is_sn=False)
            elif text == "Common Lines":
                lines = get_common_lines(self.dialog.host_redshift, spectrum_data)
                self.dialog._add_lines_to_plot(lines, is_sn=False)
            elif text == "Emission Lines":
                lines = get_emission_lines(self.dialog.host_redshift, spectrum_data)
                self.dialog._add_lines_to_plot(lines, is_sn=False)
            elif text == "Flash Lines":
                lines = get_flash_lines(self.dialog.host_redshift, spectrum_data)
                self.dialog._add_lines_to_plot(lines, is_sn=False)
            elif text == "Interaction Lines":
                lines = get_interaction_lines(self.dialog.host_redshift, spectrum_data)
                self.dialog._add_lines_to_plot(lines, is_sn=False)
                
            # Keep selections visible - don't reset dropdown
            
        except Exception as e:
            _LOGGER.error(f"Error applying other preset '{text}': {e}")

    # Legacy event handlers for backward compatibility
    def on_sn_type_selected(self, sn_type):
        """Handle SN type selection from old dropdown (legacy compatibility)"""
        if not sn_type or sn_type in ["Select SN Type...", "Select..."]:
            return
        
        try:
            # Delegate to the preset handler
            self.on_sn_type_preset_selected(sn_type)
        except Exception as e:
            _LOGGER.error(f"Error selecting SN type {sn_type}: {e}")
    
    def on_sn_phase_selected(self, phase):
        """Handle SN phase selection from old dropdown (legacy compatibility)"""
        if not phase or phase in ["Select Phase...", "Select..."]:
            return
        
        try:
            # Delegate to the preset handler  
            self.on_sn_phase_preset_selected(phase)
        except Exception as e:
            _LOGGER.error(f"Error selecting SN phase {phase}: {e}")
    
    def on_element_selected(self, element):
        """Handle element selection from old dropdown (legacy compatibility)"""
        if not element or element in ["Select Element...", "Select..."]:
            return
        
        try:
            # Delegate to the preset handler
            self.on_element_preset_selected(element)
        except Exception as e:
            _LOGGER.error(f"Error selecting element {element}: {e}")
    
    def on_galaxy_selected(self, galaxy_type):
        """Handle galaxy line selection from old dropdown (legacy compatibility)"""
        if not galaxy_type or galaxy_type in ["Select Galaxy Lines...", "Select..."]:
            return
        
        try:
            # Map to other preset handler
            self.on_other_preset_selected(galaxy_type)
        except Exception as e:
            _LOGGER.error(f"Error selecting galaxy type {galaxy_type}: {e}") 