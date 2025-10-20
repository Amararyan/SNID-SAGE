"""
Template Creator Widget
======================

Widget for creating new templates from spectra.
"""

import os
import logging
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
import numpy as np
from PySide6 import QtWidgets, QtCore, QtGui

# Import flexible number input widget
from snid_sage.interfaces.gui.components.widgets.flexible_number_input import create_flexible_double_input

# Import layout manager
from ..utils.layout_manager import get_template_layout_manager
from ..services.template_service import get_template_service

# Import main GUI preprocessing dialog if available
try:
    from snid_sage.interfaces.gui.components.pyside6_dialogs.preprocessing_dialog import PySide6PreprocessingDialog
    MAIN_GUI_AVAILABLE = True
except ImportError:
    MAIN_GUI_AVAILABLE = False

# SNID imports
try:
    from snid_sage.snid.snid import preprocess_spectrum
    SNID_AVAILABLE = True
except ImportError:
    SNID_AVAILABLE = False

# Import logging
try:
    from snid_sage.shared.utils.logging import get_logger
    _LOGGER = get_logger('template_manager.creator')
except ImportError:
    import logging
    _LOGGER = logging.getLogger('template_manager.creator')


class TemplateCreatorWidget(QtWidgets.QWidget):
    """Widget for creating new templates from spectra"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_spectrum = None
        self.layout_manager = get_template_layout_manager()
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the template creation interface"""
        layout = QtWidgets.QVBoxLayout(self)
        self.layout_manager.apply_panel_layout(self, layout)
        
        # File selection
        file_group = QtWidgets.QGroupBox("Input Spectrum")
        self.layout_manager.setup_group_box(file_group)
        file_layout = QtWidgets.QHBoxLayout(file_group)
        
        self.file_path_edit = QtWidgets.QLineEdit()
        self.file_path_edit.setPlaceholderText("Select a spectrum file...")
        
        browse_btn = self.layout_manager.create_action_button("Browse", "📁")
        browse_btn.clicked.connect(self.browse_spectrum_file)
        self.file_path_edit.textChanged.connect(self._update_actions_enabled)
        
        file_layout.addWidget(self.file_path_edit)
        file_layout.addWidget(browse_btn)
        
        layout.addWidget(file_group)
        
        # Template metadata
        metadata_group = QtWidgets.QGroupBox("Template Metadata")
        self.layout_manager.setup_group_box(metadata_group)
        metadata_layout = QtWidgets.QFormLayout(metadata_group)
        self.layout_manager.setup_form_layout(metadata_layout)
        
        self.name_edit = QtWidgets.QLineEdit()
        self.name_edit.textChanged.connect(self._update_actions_enabled)
        self.type_combo = QtWidgets.QComboBox()
        self.type_combo.setEditable(True)
        # Populate dynamically from merged index
        try:
            svc = get_template_service()
            by_type = svc.get_merged_index().get('by_type', {})
            dynamic_types = sorted(list(by_type.keys()))
            if dynamic_types:
                self.type_combo.addItems(dynamic_types)
            else:
                self.type_combo.addItems(["Ia", "Ib", "Ic", "II", "AGN", "Galaxy", "Star"])  # minimal fallback
        except Exception:
            self.type_combo.addItems(["Ia", "Ib", "Ic", "II", "AGN", "Galaxy", "Star"])  # fallback
        # Add sentinel option for creating a new type
        self._TYPE_NEW_LABEL = "New Type..."
        if self._TYPE_NEW_LABEL not in [self.type_combo.itemText(i) for i in range(self.type_combo.count())]:
            self.type_combo.addItem(self._TYPE_NEW_LABEL)
        # Start with empty type selection and placeholder
        try:
            self.type_combo.setEditText("")
            if self.type_combo.lineEdit():
                self.type_combo.lineEdit().setPlaceholderText("Select or enter a type")
        except Exception:
            pass
        
        # Build subtype map from built-in index (type -> list of known subtypes)
        self._subtypes_by_type: Dict[str, List[str]] = {}
        try:
            svc = get_template_service()
            builtin = svc.get_builtin_index()
            for name, meta in (builtin.get('templates') or {}).items():
                ttype = (meta or {}).get('type', 'Unknown')
                st = (meta or {}).get('subtype', 'Unknown')
                bucket = self._subtypes_by_type.setdefault(ttype, [])
                if isinstance(st, str) and st not in bucket:
                    bucket.append(st)
            # Sort lists for nicer UX
            for k in list(self._subtypes_by_type.keys()):
                self._subtypes_by_type[k].sort()
        except Exception:
            self._subtypes_by_type = {}

        # Subtype control: editable combo box populated per selected type
        self._SUBTYPE_NEW_LABEL = "New Subtype..."
        self.subtype_combo = QtWidgets.QComboBox()
        self.subtype_combo.setEditable(True)
        self.subtype_combo.currentTextChanged.connect(self._update_actions_enabled)
        # Update subtype options when type changes
        self.type_combo.currentTextChanged.connect(self._on_type_changed)
        # Initially locked until a type is selected
        try:
            self.subtype_combo.setEnabled(False)
            self.subtype_combo.setEditText("")
            if self.subtype_combo.lineEdit():
                self.subtype_combo.lineEdit().setPlaceholderText("Select type first")
        except Exception:
            pass
        self.age_spinbox = create_flexible_double_input(min_val=-999.9, max_val=999.9, suffix="", default=0.0)
        try:
            # Allow empty by default and show a helpful placeholder
            if hasattr(self.age_spinbox, 'setAllowEmpty'):
                self.age_spinbox.setAllowEmpty(True)
            if hasattr(self.age_spinbox, 'setSpecialValueText'):
                self.age_spinbox.setSpecialValueText("Enter age")
        except Exception:
            pass
        self.age_spinbox.valueChanged.connect(lambda *_: self._update_actions_enabled())
        
        self.redshift_spinbox = create_flexible_double_input(min_val=0.0, max_val=5.0, default=0.0)
        self.redshift_spinbox.valueChanged.connect(lambda *_: self._update_actions_enabled())
        
        metadata_layout.addRow("Template Name:", self.name_edit)
        metadata_layout.addRow("Type:", self.type_combo)
        metadata_layout.addRow("Subtype:", self.subtype_combo)
        metadata_layout.addRow("Age [days]:", self.age_spinbox)
        metadata_layout.addRow("Redshift:", self.redshift_spinbox)
        
        layout.addWidget(metadata_group)
        
        # Preprocessing controls
        preprocess_group = QtWidgets.QGroupBox("Preprocessing Options")
        self.layout_manager.setup_group_box(preprocess_group)
        preprocess_layout = QtWidgets.QVBoxLayout(preprocess_group)
        
        self.preprocess_btn = self.layout_manager.create_action_button("Advanced Preprocessing", "🔧")
        self.preprocess_btn.clicked.connect(self.open_preprocessing_dialog)
        
        self.quick_preprocess_btn = self.layout_manager.create_action_button("Quick Preprocessing", "⚡")
        self.quick_preprocess_btn.clicked.connect(self.run_quick_preprocessing)
        
        preprocess_layout.addWidget(self.preprocess_btn)
        preprocess_layout.addWidget(self.quick_preprocess_btn)
        
        layout.addWidget(preprocess_group)
        
        # Create template button
        self.create_btn = self.layout_manager.create_create_button()
        self.create_btn.clicked.connect(self.create_template)
        
        layout.addWidget(self.create_btn)
        layout.addStretch()
        
        # Initialize subtype choices (locked) and enable state
        try:
            self._on_type_changed("")
        except Exception:
            pass
        self._update_actions_enabled()
        
    def browse_spectrum_file(self):
        """Browse for a spectrum file"""
        file_path, _ = QtWidgets.QFileDialog.getOpenFileName(
            self, 
            "Select Spectrum File",
            "",
            "All Supported (*.txt *.dat *.ascii *.asci *.fits *.flm);;Text Files (*.txt *.dat *.ascii *.asci *.flm);;FITS Files (*.fits);;FLM Files (*.flm);;All Files (*.*)"
        )
        
        if file_path:
            self.file_path_edit.setText(file_path)
            # Auto-populate template name from filename
            basename = os.path.splitext(os.path.basename(file_path))[0]
            self.name_edit.setText(basename)
            
    def open_preprocessing_dialog(self):
        """Open the advanced preprocessing dialog"""
        if not self._is_ready_for_preprocessing():
            QtWidgets.QMessageBox.warning(self, "Missing Information", "Please select a spectrum and fill Name, Type, Subtype, Age, and Redshift before preprocessing.")
            return
        if not MAIN_GUI_AVAILABLE:
            QtWidgets.QMessageBox.warning(self, "Feature Unavailable", "Advanced preprocessing requires main GUI components.")
            return
            
        spectrum_file = self.file_path_edit.text()
        if not spectrum_file or not os.path.exists(spectrum_file):
            QtWidgets.QMessageBox.warning(self, "No Spectrum", "Please select a valid spectrum file first.")
            return
            
        try:
            # Load spectrum data
            wave, flux = self._load_spectrum(spectrum_file)
            # Convert to rest frame using user-provided redshift
            try:
                z_input = float(self.redshift_spinbox.value())
            except Exception:
                z_input = 0.0
            if z_input != 0.0 and wave.size > 0:
                wave = wave / (1.0 + z_input)
            
            dialog = PySide6PreprocessingDialog(self, (wave, flux))
            if dialog.exec() == QtWidgets.QDialog.Accepted:
                # Tag as rest-frame so we do not apply de-redshift again on save
                try:
                    result = dict(dialog.result)
                except Exception:
                    result = dialog.result
                if isinstance(result, dict):
                    result['is_rest_frame'] = True
                self.current_spectrum = result
                QtWidgets.QMessageBox.information(self, "Success", "Preprocessing completed. You can now create the template.")
                
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Error in preprocessing: {e}")
            _LOGGER.error(f"Preprocessing error: {e}")
            
    def run_quick_preprocessing(self):
        """Run quick preprocessing with default parameters"""
        if not self._is_ready_for_preprocessing():
            QtWidgets.QMessageBox.warning(self, "Missing Information", "Please select a spectrum and fill Name, Type, Subtype, Age, and Redshift before preprocessing.")
            return
        spectrum_file = self.file_path_edit.text()
        if not spectrum_file or not os.path.exists(spectrum_file):
            QtWidgets.QMessageBox.warning(self, "No Spectrum", "Please select a valid spectrum file first.")
            return
            
        if not SNID_AVAILABLE:
            QtWidgets.QMessageBox.warning(self, "Feature Unavailable", "Preprocessing requires SNID core components.")
            return
            
        try:
            # Load, convert to rest frame, then run quick preprocessing
            wave, flux = self._load_spectrum(spectrum_file)
            try:
                z_input = float(self.redshift_spinbox.value())
            except Exception:
                z_input = 0.0
            if z_input != 0.0 and wave.size > 0:
                wave = wave / (1.0 + z_input)
            processed_spectrum, trace = preprocess_spectrum(
                input_spectrum=(wave, flux),
                verbose=True
            )
            
            # Tag as rest-frame
            if isinstance(processed_spectrum, dict):
                processed_spectrum['is_rest_frame'] = True
            self.current_spectrum = processed_spectrum
            QtWidgets.QMessageBox.information(self, "Success", "Quick preprocessing completed. You can now create the template.")
            
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Error in quick preprocessing: {e}")
            _LOGGER.error(f"Quick preprocessing error: {e}")
            
    def create_template(self):
        """Create the template with current settings"""
        # Validate inputs
        if not self.name_edit.text().strip():
            QtWidgets.QMessageBox.warning(self, "Missing Information", "Please enter a template name.")
            return
        if not self.subtype_combo.currentText().strip() or self.subtype_combo.currentText().strip() == self._SUBTYPE_NEW_LABEL:
            QtWidgets.QMessageBox.warning(self, "Missing Information", "Please enter a subtype.")
            return
            
        if not self.file_path_edit.text() or not os.path.exists(self.file_path_edit.text()):
            QtWidgets.QMessageBox.warning(self, "Missing File", "Please select a valid spectrum file.")
            return
            
        # Prepare template metadata
        template_info = {
            'name': self.name_edit.text().strip(),
            'type': self.type_combo.currentText(),
            'subtype': self.subtype_combo.currentText().strip() or 'Unknown',
            'age': self.age_spinbox.value(),
            'redshift': self.redshift_spinbox.value(),
            'phase': 'Unknown',
            'epochs': 1
        }
        
        try:
            # Use preprocessed spectrum if available, otherwise load and preprocess
            if self.current_spectrum is not None:
                spectrum_data = self.current_spectrum
            else:
                # Load spectrum and apply quick preprocessing
                wave, flux = self._load_spectrum(self.file_path_edit.text())
                
                if SNID_AVAILABLE:
                    processed_spectrum, trace = preprocess_spectrum(
                        input_spectrum=(wave, flux),
                        verbose=False
                    )
                    spectrum_data = processed_spectrum
                else:
                    # Simple dictionary structure if SNID not available
                    spectrum_data = {
                        'wave': wave,
                        'flux': flux,
                        'fluxed': flux,
                        'flat': flux / np.median(flux)
                    }
            
            # Extract wave/flux arrays (support keys from SNID preprocess and dialog)
            wave = (
                spectrum_data.get('log_wave')
                if isinstance(spectrum_data, dict) else None
            )
            if wave is None and isinstance(spectrum_data, dict):
                wave = spectrum_data.get('processed_wave') or spectrum_data.get('wave') or spectrum_data.get('wavelength')

            flux = (
                spectrum_data.get('tapered_flux')
                if isinstance(spectrum_data, dict) else None
            )
            if flux is None and isinstance(spectrum_data, dict):
                flux = (
                    spectrum_data.get('flat_flux')
                    or spectrum_data.get('log_flux')
                    or spectrum_data.get('processed_flux')
                    or spectrum_data.get('flat')
                    or spectrum_data.get('flux')
                )
            if wave is None or flux is None:
                raise ValueError("No valid wave/flux in spectrum data")

            wave = np.asarray(wave, dtype=float)
            flux = np.asarray(flux, dtype=float)

            # De-redshift to rest-frame if needed (skip if already rest frame)
            already_rest = False
            try:
                if isinstance(self.current_spectrum, dict) and self.current_spectrum.get('is_rest_frame', False):
                    already_rest = True
            except Exception:
                already_rest = False
            if not already_rest:
                try:
                    z_input = float(template_info.get('redshift', 0.0) or 0.0)
                except Exception:
                    z_input = 0.0
                if z_input != 0.0 and wave.size > 0:
                    wave = wave / (1.0 + z_input)

            # Persist via HDF5-only service
            svc = get_template_service()
            success = svc.add_template_from_arrays(
                name=template_info['name'],
                ttype=template_info['type'],
                subtype=template_info['subtype'],
                age=float(template_info['age']),
                redshift=float(template_info['redshift']),
                phase=template_info['phase'],
                wave=wave,
                flux=flux,
            )
            
            if success:
                QtWidgets.QMessageBox.information(
                    self, 
                    "Success", 
                    f"Template '{template_info['name']}' created successfully!\n\n"
                    f"Type: {template_info['type']}/{template_info['subtype']}\n"
                    f"Age: {template_info['age']} days\n"
                    f"Redshift: {template_info['redshift']}"
                )
                # Refresh left template list in the main window
                try:
                    mw = self.window()
                    if hasattr(mw, 'refresh_template_library'):
                        mw.refresh_template_library()
                except Exception:
                    pass
                
                # Clear form for next template
                self._clear_form()
            else:
                QtWidgets.QMessageBox.critical(self, "Error", "Failed to create template. Check logs for details.")
                
        except Exception as e:
            QtWidgets.QMessageBox.critical(self, "Error", f"Error creating template: {str(e)}")
            _LOGGER.error(f"Template creation error: {e}")
        finally:
            self._update_actions_enabled()
            
    def _save_template(self, template_info: Dict[str, Any], spectrum_data: Dict[str, np.ndarray]) -> bool:
        """Deprecated: LNW saving removed. Use TemplateService instead."""
        _LOGGER.error("_save_template legacy path invoked; this method is deprecated in HDF5-only mode.")
        return False
            
    def _clear_form(self):
        """Clear the template creation form"""
        self.file_path_edit.clear()
        self.name_edit.clear()
        try:
            self.subtype_combo.setCurrentText("")
        except Exception:
            pass
        self.age_spinbox.setValue(0.0)
        self.redshift_spinbox.setValue(0.0)
        self.current_spectrum = None
        self._update_actions_enabled()
        
    def _load_spectrum(self, file_path: str) -> Tuple[np.ndarray, np.ndarray]:
        """Load spectrum from file"""
        try:
            # Try different file formats (LNW removed)
            if file_path.endswith('.fits'):
                return self._load_fits_spectrum(file_path)
            elif file_path.endswith('.flm'):
                return self._load_ascii_spectrum(file_path)  # FLM files are text-based
            else:
                return self._load_ascii_spectrum(file_path)
        except Exception as e:
            _LOGGER.error(f"Error loading spectrum: {e}")
            # Return dummy data on error
            wave = np.linspace(3000, 9000, 1000)
            flux = np.random.normal(1, 0.1, 1000)
            return wave, flux
            
    def _load_fits_spectrum(self, file_path: str) -> Tuple[np.ndarray, np.ndarray]:
        """Load spectrum from FITS file"""
        try:
            from astropy.io import fits
            with fits.open(file_path) as hdul:
                # Try to find spectrum data in different extensions
                for hdu in hdul:
                    if hdu.data is not None:
                        data = hdu.data
                        if len(data.shape) == 1:
                            # 1D spectrum - assume wavelength is indices
                            flux = data
                            wave = np.arange(len(flux)) + 1
                            return wave, flux
                        elif len(data.shape) == 2:
                            # 2D - assume first column is wavelength, second is flux
                            wave = data[:, 0]
                            flux = data[:, 1]
                            return wave, flux
        except ImportError:
            raise ImportError("astropy required for FITS files: pip install astropy")
            
    # LNW loading removed
        
    def _load_ascii_spectrum(self, file_path: str) -> Tuple[np.ndarray, np.ndarray]:
        """Load spectrum from ASCII file"""
        try:
            # Try to load as two-column ASCII
            data = np.loadtxt(file_path)
            if data.shape[1] >= 2:
                wave = data[:, 0]
                flux = data[:, 1]
                return wave, flux
            else:
                # Single column - assume flux only
                flux = data
                wave = np.arange(len(flux)) + 1
                return wave, flux
        except Exception as e:
            raise ValueError(f"Could not load ASCII spectrum: {e}")
    
    def set_spectrum_file(self, file_path: str):
        """Set the spectrum file path programmatically"""
        if os.path.exists(file_path):
            self.file_path_edit.setText(file_path)
            basename = os.path.splitext(os.path.basename(file_path))[0]
            self.name_edit.setText(basename)
    
    def get_current_template_info(self) -> Dict[str, Any]:
        """Get the current template information from the form"""
        return {
            'name': self.name_edit.text().strip(),
            'type': self.type_combo.currentText(),
            'subtype': self.subtype_combo.currentText().strip() or 'Unknown',
            'age': self.age_spinbox.value(),
            'redshift': self.redshift_spinbox.value(),
            'spectrum_file': self.file_path_edit.text()
        }
    
    def validate_form(self) -> Tuple[bool, str]:
        """Validate the current form state"""
        if not self.name_edit.text().strip():
            return False, "Template name is required"
        if not self.subtype_combo.currentText().strip() or self.subtype_combo.currentText().strip() == self._SUBTYPE_NEW_LABEL:
            return False, "Subtype is required"
        
        if not self.file_path_edit.text():
            return False, "Spectrum file is required"
        
        if not os.path.exists(self.file_path_edit.text()):
            return False, "Spectrum file does not exist"
        
        return True, "Form is valid"

    # ---- helpers ----
    def _is_ready_for_preprocessing(self) -> bool:
        """Check that required fields are filled before preprocessing."""
        if not (self.file_path_edit.text() and os.path.exists(self.file_path_edit.text())):
            return False
        if not self.name_edit.text().strip():
            return False
        if not self.subtype_combo.currentText().strip():
            return False
        # type combo always has a selection; ensure text is not empty
        # type combo must be non-empty and not the sentinel
        if not self.type_combo.currentText().strip() or self.type_combo.currentText().strip() == self._TYPE_NEW_LABEL:
            return False
        # age/redshift are numeric; just ensure widgets exist
        try:
            _ = float(self.age_spinbox.value())
            _ = float(self.redshift_spinbox.value())
        except Exception:
            return False
        return True

    def _update_actions_enabled(self) -> None:
        """Enable/disable preprocessing and create buttons based on form state."""
        ready = self._is_ready_for_preprocessing()
        try:
            self.preprocess_btn.setEnabled(ready)
            self.quick_preprocess_btn.setEnabled(ready)
            # Allow create when ready as well
            self.create_btn.setEnabled(ready)
        except Exception:
            pass

    def _on_type_changed(self, ttype: str) -> None:
        """Update subtype combo items based on selected type."""
        normalized = (ttype or "").strip()
        try:
            current_text = self.subtype_combo.currentText().strip()
        except Exception:
            current_text = ""
        try:
            self.subtype_combo.blockSignals(True)
            self.subtype_combo.clear()
            # Lock subtype if no type chosen
            if not normalized:
                self.subtype_combo.setEnabled(False)
                if self.subtype_combo.lineEdit():
                    self.subtype_combo.lineEdit().setPlaceholderText("Select type first")
                return
            # Enable subtype once a type is present
            self.subtype_combo.setEnabled(True)
            # If the user selected the sentinel for new type, encourage entering new subtype
            if normalized == self._TYPE_NEW_LABEL or normalized not in self._subtypes_by_type:
                self.subtype_combo.addItem(self._SUBTYPE_NEW_LABEL)
                if self.subtype_combo.lineEdit():
                    self.subtype_combo.lineEdit().setPlaceholderText("Enter new subtype")
                self.subtype_combo.setEditText("")
                return
            options = list(self._subtypes_by_type.get(normalized, []))
            if options:
                self.subtype_combo.addItems(options)
            # Preserve user-entered text if any
            if current_text and current_text not in options:
                self.subtype_combo.setEditText(current_text)
        finally:
            try:
                self.subtype_combo.blockSignals(False)
            except Exception:
                pass
        # Also if user picked the 'New Type...' sentinel, focus edit for typing
        if normalized == self._TYPE_NEW_LABEL:
            try:
                self.type_combo.setEditText("")
            except Exception:
                pass
        # Update action enablement after type change
        self._update_actions_enabled()