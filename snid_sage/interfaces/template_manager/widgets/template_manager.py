"""
Template Manager Widget
======================

Advanced template management tools for batch operations and editing.
"""

import logging
from typing import Dict, List, Optional, Any
from PySide6 import QtWidgets, QtCore, QtGui

# Import flexible number input widget
from snid_sage.interfaces.gui.components.widgets.flexible_number_input import create_flexible_double_input

# Import layout manager
from ..utils.layout_manager import get_template_layout_manager
from ..services.template_service import get_template_service

# Import logging
try:
    from snid_sage.shared.utils.logging import get_logger
    _LOGGER = get_logger('template_manager.manager')
except ImportError:
    import logging
    _LOGGER = logging.getLogger('template_manager.manager')


class TemplateManagerWidget(QtWidgets.QWidget):
    """Advanced template management tools"""
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout_manager = get_template_layout_manager()
        self.setup_ui()
        try:
            self.update_empty_state()
        except Exception:
            pass
        
    def setup_ui(self):
        """Setup the management interface"""
        layout = QtWidgets.QVBoxLayout(self)
        self.layout_manager.apply_panel_layout(self, layout)
        
        # Batch operations removed
        
        # Template editing
        edit_group = QtWidgets.QGroupBox("Template Editing")
        self.layout_manager.setup_group_box(edit_group)
        edit_layout = QtWidgets.QVBoxLayout(edit_group)
        
        # Metadata editing
        metadata_frame = QtWidgets.QFrame()
        metadata_layout = QtWidgets.QFormLayout(metadata_frame)
        self.layout_manager.setup_form_layout(metadata_layout)
        
        self.edit_name = QtWidgets.QLineEdit()
        self.edit_type = QtWidgets.QComboBox()
        # Populate dynamically from merged index
        try:
            svc = get_template_service()
            by_type = svc.get_merged_index().get('by_type', {})
            dynamic_types = sorted(list(by_type.keys()))
            if dynamic_types:
                self.edit_type.addItems(dynamic_types)
            else:
                self.edit_type.addItems(["Ia", "Ib", "Ic", "II", "AGN", "Galaxy", "Star"])  # minimal fallback
        except Exception:
            self.edit_type.addItems(["Ia", "Ib", "Ic", "II", "AGN", "Galaxy", "Star"])  # fallback
        self.edit_subtype = QtWidgets.QLineEdit()
        self.edit_age = create_flexible_double_input(min_val=-999.9, max_val=999.9, suffix=" days", default=0.0)
        
        metadata_layout.addRow("Name:", self.edit_name)
        metadata_layout.addRow("Type:", self.edit_type)
        metadata_layout.addRow("Subtype:", self.edit_subtype)
        metadata_layout.addRow("Age:", self.edit_age)
        
        edit_layout.addWidget(metadata_frame)
        
        # Action buttons
        action_frame = QtWidgets.QFrame()
        action_layout = QtWidgets.QHBoxLayout(action_frame)
        
        save_btn = self.layout_manager.create_action_button("Save Changes", "💾")
        save_btn.clicked.connect(self.save_template_changes)
        
        delete_btn = self.layout_manager.create_action_button("Delete Template", "🗑️")
        delete_btn.clicked.connect(self.delete_template)
        delete_btn.setStyleSheet("QPushButton { background-color: #dc2626; color: white; }")
        
        action_layout.addWidget(save_btn)
        action_layout.addWidget(delete_btn)
        
        edit_layout.addWidget(action_frame)
        layout.addWidget(edit_group)
        
        # Empty-state label (shown when no user templates exist)
        self.empty_state_label = QtWidgets.QLabel("No user templates available yet. Create one in the 'Create Template' tab.")
        self.empty_state_label.setWordWrap(True)
        self.empty_state_label.setStyleSheet("color: #6b7280; padding: 8px;")
        layout.addWidget(self.empty_state_label)
        
        layout.addStretch()
        
    # Batch operations and related dialogs removed
        
    def save_template_changes(self):
        """Save changes to template metadata"""
        if not self.edit_name.text().strip():
            QtWidgets.QMessageBox.warning(self, "Validation Error", "Template name cannot be empty.")
            return
        svc = get_template_service()
        ok = svc.update_metadata(
            self.edit_name.text().strip(),
            {
                'type': self.edit_type.currentText(),
                'subtype': self.edit_subtype.text().strip(),
                'age': float(self.edit_age.value()),
            }
        )
        if ok:
            QtWidgets.QMessageBox.information(self, "Save", "Template metadata saved successfully!")
            self._emit_refresh()
        else:
            QtWidgets.QMessageBox.critical(self, "Error", "Failed to save template metadata (only user templates are editable).")
        self.update_empty_state()
        
    def delete_template(self):
        """Delete selected template"""
        if not self.edit_name.text().strip():
            QtWidgets.QMessageBox.warning(self, "Selection Error", "No template selected for deletion.")
            return
        
        reply = QtWidgets.QMessageBox.question(
            self, 
            "Delete Template", 
            f"Are you sure you want to delete template '{self.edit_name.text()}'?\n\nThis action cannot be undone.",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No
        )
        if reply == QtWidgets.QMessageBox.Yes:
            svc = get_template_service()
            if svc.delete(self.edit_name.text().strip()):
                QtWidgets.QMessageBox.information(self, "Deleted", f"Template '{self.edit_name.text()}' deleted successfully!")
                self._clear_form()
                self._emit_refresh()
            else:
                QtWidgets.QMessageBox.critical(self, "Error", "Failed to delete (only user templates can be deleted).")
        self.update_empty_state()
            
    # Advanced operations and duplication removed
    
    def set_template_for_editing(self, template_name: str, template_info: Dict[str, Any]):
        """Set a template for editing"""
        self.edit_name.setText(template_name)
        self.edit_type.setCurrentText(template_info.get('type', 'Other'))
        self.edit_subtype.setText(template_info.get('subtype', ''))
        self.edit_age.setValue(template_info.get('age', 0.0))
        # Disable editing controls if this is a built-in template (not in user index)
        try:
            svc = get_template_service()
            user_templates = (svc.get_user_index().get('templates') or {})
            is_user = template_name in user_templates
        except Exception:
            is_user = False
        # Enable/disable inputs and buttons accordingly
        try:
            editable_widgets = [self.edit_type, self.edit_subtype, self.edit_age]
            for w in editable_widgets:
                w.setEnabled(is_user)
            # Find buttons in the action frame by walking children
            for btn in self.findChildren(QtWidgets.QPushButton):
                if btn.text().strip().lower().startswith('save'):
                    btn.setEnabled(is_user)
                if btn.text().strip().lower().startswith('delete'):
                    btn.setEnabled(is_user)
        except Exception:
            pass
    
    def _clear_form(self):
        """Clear the editing form"""
        self.edit_name.clear()
        self.edit_type.setCurrentIndex(0)
        self.edit_subtype.clear()
        self.edit_age.setValue(0.0)

    def _emit_refresh(self) -> None:
        # Notify parent main window to refresh tree and counts if available
        try:
            mw = self.window()
            if hasattr(mw, 'refresh_template_library'):
                mw.refresh_template_library()
        except Exception:
            pass
        try:
            self.update_empty_state()
        except Exception:
            pass
    
    def get_current_template_info(self) -> Dict[str, Any]:
        """Get current template information from the form"""
        return {
            'name': self.edit_name.text(),
            'type': self.edit_type.currentText(),
            'subtype': self.edit_subtype.text(),
            'age': self.edit_age.value()
        }

    def update_empty_state(self) -> None:
        """Show or hide the empty-state message based on presence of user templates."""
        try:
            from ..services.template_service import get_template_service
            has_user = get_template_service().has_user_templates()
            self.empty_state_label.setVisible(not has_user)
        except Exception:
            # If check fails, hide label to avoid blocking UI
            self.empty_state_label.setVisible(False)