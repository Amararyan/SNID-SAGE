"""
SNID SAGE - Analysis Results Dialog - PySide6 Version
===================================================

Comprehensive analysis results dialog for displaying SNID classification results.
Based on the Tkinter cluster_summary.py implementation but using modern PySide6.

Features:
- Clean classification summary with key results
- Detailed template match table with sorting
- Subtype statistics and proportions
- Quality and confidence assessment
- Copy/export functionality
- Modern Qt styling
"""

import PySide6.QtCore as QtCore
import PySide6.QtGui as QtGui
import PySide6.QtWidgets as QtWidgets
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import json

try:
    from snid_sage.shared.utils.logging import get_logger
    _LOGGER = get_logger('gui.pyside6_results')
except ImportError:
    import logging
    _LOGGER = logging.getLogger('gui.pyside6_results')

# Import analysis utilities
try:
    from snid_sage.interfaces.gui.features.analysis.cluster_summary import (
        AnalysisResultsAnalyzer, extract_age, format_age_display, is_valid_age
    )
    from snid_sage.shared.utils.math_utils import get_best_metric_value, get_metric_name_for_match
except ImportError:
    _LOGGER.warning("Some analysis utilities not available - results may be limited")


class PySide6AnalysisResultsDialog(QtWidgets.QDialog):
    """
    PySide6 dialog for comprehensive analysis results display.
    
    Shows classification results, template matches, statistics, and quality assessment.
    """
    
    def __init__(self, parent, analysis_results=None, cluster_index=0):
        """
        Initialize analysis results dialog.
        
        Args:
            parent: Parent window
            analysis_results: SNID analysis results object
            cluster_index: Index of the cluster to display (default: 0 for winning cluster)
        """
        super().__init__(parent)
        
        self.parent_gui = parent
        self.analysis_results = analysis_results
        self.cluster_index = cluster_index
        
        # Extract cluster data from SNID results structure
        self.selected_cluster = None
        self.all_candidates = []
        self.analyzer = None
        
        # FIXED: Extract clustering data from the correct SNID results structure
        if analysis_results and hasattr(analysis_results, 'clustering_results') and analysis_results.clustering_results:
            clustering_results = analysis_results.clustering_results
            
            if clustering_results.get('success', False):
                # Get all cluster candidates
                self.all_candidates = clustering_results.get('all_candidates', [])
                
                # Get the winning cluster (user selected or automatic best)
                if 'user_selected_cluster' in clustering_results:
                    self.selected_cluster = clustering_results['user_selected_cluster']
                elif 'best_cluster' in clustering_results:
                    self.selected_cluster = clustering_results['best_cluster']
                elif self.all_candidates and cluster_index < len(self.all_candidates):
                    self.selected_cluster = self.all_candidates[cluster_index]
                
                # Create analyzer with the selected cluster
                if self.selected_cluster and self.all_candidates:
                    try:
                        self.analyzer = AnalysisResultsAnalyzer(self.selected_cluster, self.all_candidates)
                    except Exception as e:
                        _LOGGER.error(f"Failed to create AnalysisResultsAnalyzer: {e}")
                        self.analyzer = None
        
        # Fallback: if no clustering results, try to create a single cluster from best_matches
        if not self.analyzer and analysis_results and hasattr(analysis_results, 'best_matches'):
            try:
                # Create a pseudo-cluster from the best matches
                self.selected_cluster = {
                    'type': getattr(analysis_results, 'consensus_type', 'Unknown'),
                    'matches': analysis_results.best_matches,
                    'size': len(analysis_results.best_matches),
                    'cluster_id': 0
                }
                self.all_candidates = [self.selected_cluster]
                self.analyzer = AnalysisResultsAnalyzer(self.selected_cluster, self.all_candidates)
                _LOGGER.info("Created fallback cluster analysis from best_matches")
            except Exception as e:
                _LOGGER.error(f"Failed to create fallback analyzer: {e}")
                self.analyzer = None
        
        # UI components
        self.summary_text = None
        self.matches_table = None
        self.copy_btn = None
        self.export_btn = None
        
        # Color scheme matching other dialogs
        self.colors = {
            'bg': '#f8fafc',
            'panel_bg': '#ffffff',
            'text_primary': '#1e293b',
            'text_secondary': '#64748b',
            'border': '#e2e8f0',
            'success': '#22c55e',
            'warning': '#f59e0b',
            'danger': '#ef4444',
            'accent': '#3b82f6'
        }
        
        self._setup_dialog()
        self._create_interface()
        self._populate_results()
    
    def _setup_dialog(self):
        """Setup dialog window properties"""
        cluster_type = self.selected_cluster.get('type', 'Unknown') if self.selected_cluster else 'Unknown'
        cluster_num = self.cluster_index + 1
        
        self.setWindowTitle(f"📊 Analysis Results - {cluster_type} (Cluster #{cluster_num})")
        # Made smaller and more compact as requested
        self.setMinimumSize(700, 500)
        self.resize(900, 650)
        self.setModal(False)  # Allow interaction with main window
        
        # Apply styling
        self.setStyleSheet(f"""
            QDialog {{
                background: {self.colors['bg']};
                color: {self.colors['text_primary']};
                font-family: "Segoe UI", Arial, sans-serif;
            }}
            
            QGroupBox {{
                font-weight: bold;
                font-size: 11pt;
                border: 2px solid {self.colors['border']};
                border-radius: 6px;
                margin-top: 8px;
                padding-top: 12px;
                background: {self.colors['panel_bg']};
            }}
            
            QGroupBox::title {{
                subcontrol-origin: margin;
                left: 12px;
                padding: 0 8px 0 8px;
                color: {self.colors['text_primary']};
            }}
            
            QTextEdit {{
                border: 2px solid {self.colors['border']};
                border-radius: 6px;
                background: {self.colors['panel_bg']};
                font-family: "Consolas", "Monaco", monospace;
                font-size: 10pt;
                padding: 8px;
                selection-background-color: {self.colors['accent']};
            }}
            
            QTableWidget {{
                border: 2px solid {self.colors['border']};
                border-radius: 6px;
                background: {self.colors['panel_bg']};
                alternate-background-color: #f1f5f9;
                selection-background-color: {self.colors['accent']};
                gridline-color: {self.colors['border']};
            }}
            
            QTableWidget::item {{
                padding: 6px;
                border: none;
            }}
            
            QHeaderView::section {{
                background: #e2e8f0;
                border: 1px solid {self.colors['border']};
                padding: 8px;
                font-weight: bold;
                font-size: 9pt;
            }}
            
            QPushButton {{
                border: 2px solid {self.colors['border']};
                border-radius: 6px;
                padding: 8px 16px;
                font-weight: bold;
                font-size: 10pt;
                background: {self.colors['panel_bg']};
                min-width: 80px;
            }}
            
            QPushButton:hover {{
                background: #f1f5f9;
            }}
            
            QPushButton:pressed {{
                background: #e2e8f0;
            }}
            
            QPushButton#primary_btn {{
                background: {self.colors['success']};
                border: 2px solid {self.colors['success']};
                color: white;
            }}
            
            QPushButton#primary_btn:hover {{
                background: #16a34a;
            }}
            
            QTabWidget::pane {{
                border: 2px solid {self.colors['border']};
                border-radius: 6px;
                background: {self.colors['panel_bg']};
            }}
            
            QTabBar::tab {{
                background: #e2e8f0;
                border: 1px solid {self.colors['border']};
                padding: 8px 16px;
                margin-right: 2px;
                font-weight: bold;
            }}
            
            QTabBar::tab:selected {{
                background: {self.colors['panel_bg']};
                border-bottom: none;
            }}
        """)
    
    def _create_interface(self):
        """Create the dialog interface"""
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(15)
        
        # Header
        self._create_header(layout)
        
        # Main content with tabs
        self._create_tabbed_content(layout)
        
        # Button bar
        self._create_button_bar(layout)
    
    def _create_header(self, layout):
        """Create dialog header"""
        header_frame = QtWidgets.QFrame()
        header_frame.setObjectName("header_frame")
        header_layout = QtWidgets.QVBoxLayout(header_frame)
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        # Title
        cluster_type = self.selected_cluster.get('type', 'Unknown') if self.selected_cluster else 'Unknown'
        cluster_num = self.cluster_index + 1
        
        title = QtWidgets.QLabel(f"📊 SNID Classification Results")
        title.setAlignment(QtCore.Qt.AlignCenter)
        title.setStyleSheet("""
            font-size: 18pt;
            font-weight: bold;
            color: #3b82f6;
            margin: 10px 0;
        """)
        header_layout.addWidget(title)
        
        subtitle = QtWidgets.QLabel(f"{cluster_type} • Top Cluster #{cluster_num}")
        subtitle.setAlignment(QtCore.Qt.AlignCenter)
        subtitle.setStyleSheet("""
            font-size: 14pt;
            color: #64748b;
            margin-bottom: 10px;
        """)
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header_frame)
    
    def _create_tabbed_content(self, layout):
        """Create main tabbed content area"""
        self.tab_widget = QtWidgets.QTabWidget()
        
        # Summary tab
        self._create_summary_tab()
        
        # Detailed matches tab
        self._create_matches_tab()
        
        # Statistics tab
        self._create_statistics_tab()
        
        layout.addWidget(self.tab_widget, 1)  # Expand to fill space
    
    def _create_summary_tab(self):
        """Create summary tab with key results"""
        summary_widget = QtWidgets.QWidget()
        summary_layout = QtWidgets.QVBoxLayout(summary_widget)
        summary_layout.setContentsMargins(15, 15, 15, 15)
        
        # Summary text display
        self.summary_text = QtWidgets.QTextEdit()
        self.summary_text.setReadOnly(True)
        # Made smaller for more compact dialog
        self.summary_text.setMaximumHeight(300)
        summary_layout.addWidget(self.summary_text)
        
        # Quick actions
        actions_group = QtWidgets.QGroupBox("Quick Actions")
        actions_layout = QtWidgets.QHBoxLayout(actions_group)
        
        copy_summary_btn = QtWidgets.QPushButton("📋 Copy Summary")
        copy_summary_btn.clicked.connect(self._copy_summary)
        actions_layout.addWidget(copy_summary_btn)
        
        save_results_btn = QtWidgets.QPushButton("💾 Save Results")
        save_results_btn.clicked.connect(self._save_results)
        actions_layout.addWidget(save_results_btn)
        
        actions_layout.addStretch()
        summary_layout.addWidget(actions_group)
        
        self.tab_widget.addTab(summary_widget, "📋 Summary")
    
    def _create_matches_tab(self):
        """Create detailed template matches tab"""
        matches_widget = QtWidgets.QWidget()
        matches_layout = QtWidgets.QVBoxLayout(matches_widget)
        matches_layout.setContentsMargins(15, 15, 15, 15)
        
        # Table for template matches
        self.matches_table = QtWidgets.QTableWidget()
        self.matches_table.setAlternatingRowColors(True)
        self.matches_table.setSortingEnabled(True)
        self.matches_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        
        # Set up table columns
        columns = ['Rank', 'Template', 'Type', 'Subtype', 'Metric', 'Redshift', 'z_err', 'Age (days)']
        self.matches_table.setColumnCount(len(columns))
        self.matches_table.setHorizontalHeaderLabels(columns)
        
        # Configure column widths
        header = self.matches_table.horizontalHeader()
        header.setStretchLastSection(True)
        for i, width in enumerate([60, 180, 80, 100, 80, 100, 80, 100]):
            self.matches_table.setColumnWidth(i, width)
        
        matches_layout.addWidget(self.matches_table)
        
        # Table controls
        table_controls = QtWidgets.QHBoxLayout()
        
        show_all_btn = QtWidgets.QPushButton("📊 Show All Matches")
        show_all_btn.clicked.connect(self._show_all_matches)
        table_controls.addWidget(show_all_btn)
        
        export_table_btn = QtWidgets.QPushButton("📤 Export Table")
        export_table_btn.clicked.connect(self._export_table)
        table_controls.addWidget(export_table_btn)
        
        table_controls.addStretch()
        matches_layout.addLayout(table_controls)
        
        self.tab_widget.addTab(matches_widget, "🔍 Template Matches")
    
    def _create_statistics_tab(self):
        """Create statistics tab with detailed analysis"""
        stats_widget = QtWidgets.QWidget()
        stats_layout = QtWidgets.QVBoxLayout(stats_widget)
        stats_layout.setContentsMargins(15, 15, 15, 15)
        
        # Statistics content will be populated later
        self.stats_text = QtWidgets.QTextEdit()
        self.stats_text.setReadOnly(True)
        stats_layout.addWidget(self.stats_text)
        
        self.tab_widget.addTab(stats_widget, "📈 Statistics")
    
    def _create_button_bar(self, layout):
        """Create bottom button bar"""
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addStretch()
        
        # GMM Clustering button
        gmm_btn = QtWidgets.QPushButton("🎯 View GMM Clustering")
        gmm_btn.clicked.connect(self._open_gmm_dialog)
        button_layout.addWidget(gmm_btn)
        
        # Close button
        close_btn = QtWidgets.QPushButton("✅ Close")
        close_btn.setObjectName("primary_btn")
        close_btn.clicked.connect(self.accept)
        close_btn.setDefault(True)
        button_layout.addWidget(close_btn)
        
        layout.addLayout(button_layout)
    
    def _populate_results(self):
        """Populate the dialog with analysis results"""
        if not self.analyzer:
            self._show_no_results()
            return
        
        try:
            # Populate summary
            summary_text = self.analyzer.generate_summary_report()
            self.summary_text.setPlainText(summary_text)
            
            # Populate matches table
            self._populate_matches_table()
            
            # Populate statistics
            self._populate_statistics()
            
        except Exception as e:
            _LOGGER.error(f"Error populating results: {e}")
            self._show_error(f"Error displaying results: {str(e)}")
    
    def _show_no_results(self):
        """Show message when no results are available"""
        no_results_msg = """
🚫 No Analysis Results Available

No SNID analysis results were found to display.
Please run the analysis first to see classification results.
        """.strip()
        
        self.summary_text.setPlainText(no_results_msg)
        self.stats_text.setPlainText(no_results_msg)
    
    def _show_error(self, error_msg):
        """Show error message"""
        error_text = f"""
❌ Error Loading Results

{error_msg}

Please try running the analysis again or check the logs for more details.
        """.strip()
        
        self.summary_text.setPlainText(error_text)
        self.stats_text.setPlainText(error_text)
    
    def _populate_matches_table(self):
        """Populate the template matches table"""
        if not self.analyzer or not self.analyzer.matches:
            return
        
        # Sort matches by best metric value
        sorted_matches = sorted(self.analyzer.matches, key=get_best_metric_value, reverse=True)
        
        # Set table size
        self.matches_table.setRowCount(len(sorted_matches))
        
        # Get metric name from first match
        metric_name = "RLAP"
        if sorted_matches:
            metric_name = get_metric_name_for_match(sorted_matches[0])
        
        # Update metric column header
        self.matches_table.setHorizontalHeaderItem(4, QtWidgets.QTableWidgetItem(metric_name))
        
        # Populate table rows
        for i, match in enumerate(sorted_matches):
            template = match.get('template', {})
            
            # Create table items
            items = [
                QtWidgets.QTableWidgetItem(str(i + 1)),  # Rank
                QtWidgets.QTableWidgetItem(template.get('name', 'Unknown')[:25]),  # Template
                QtWidgets.QTableWidgetItem(template.get('type', 'Unknown')),  # Type
                QtWidgets.QTableWidgetItem(template.get('subtype', 'Unknown')),  # Subtype
                QtWidgets.QTableWidgetItem(f"{get_best_metric_value(match):.1f}"),  # Metric
                QtWidgets.QTableWidgetItem(f"{match.get('redshift', 0):.5f}"),  # Redshift
                QtWidgets.QTableWidgetItem(f"{match.get('redshift_error', 0):.5f}" if match.get('redshift_error', 0) > 0 else "N/A"),  # z_err
                QtWidgets.QTableWidgetItem(format_age_display(extract_age(match, template)))  # Age
            ]
            
            # Set items in table
            for j, item in enumerate(items):
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)  # Make read-only
                self.matches_table.setItem(i, j, item)
        
        # Auto-resize columns to content
        self.matches_table.resizeColumnsToContents()
    
    def _populate_statistics(self):
        """Populate the statistics tab"""
        if not self.analyzer or not self.analyzer.summary_stats:
            return
        
        stats = self.analyzer.summary_stats
        
        # Build detailed statistics report
        lines = [
            "📈 DETAILED STATISTICAL ANALYSIS",
            "=" * 60,
            "",
            "🎯 CLUSTER INFORMATION:",
            f"   Total Templates: {stats['cluster_size']}",
            f"   Supernova Type: {stats['supernova_type']}",
            f"   RLAP Threshold: {self.analyzer.rlapmin}",
            "",
            "📏 REDSHIFT STATISTICS:",
        ]
        
        # Safely access redshift statistics
        redshift_stats = stats.get('redshift', {})
        if redshift_stats:
            lines.extend([
                f"   Weighted Mean: {redshift_stats.get('weighted_mean', 0.0):.6f} ± {redshift_stats.get('weighted_uncertainty', 0.0):.6f}",
                f"   Range: {redshift_stats.get('min', 0.0):.6f} to {redshift_stats.get('max', 0.0):.6f}",
                f"   Cluster Scatter: {redshift_stats.get('cluster_scatter', 0.0):.6f}",
            ])
        else:
            lines.append("   Redshift statistics not available")
        
        lines.extend([
            "",
            "📊 RLAP STATISTICS:",
        ])
        
        # Safely access RLAP statistics  
        rlap_stats = stats.get('rlap', {})
        if rlap_stats:
            lines.extend([
                f"   Mean: {rlap_stats.get('mean', 0.0):.2f}",
                f"   Range: {rlap_stats.get('min', 0.0):.1f} to {rlap_stats.get('max', 0.0):.1f}",
                f"   Weighted Mean: {rlap_stats.get('weighted_mean', 0.0):.2f}",
                f"   Weighted Median: {rlap_stats.get('weighted_median', 0.0):.2f}",
            ])
        else:
            lines.append("   RLAP statistics not available")
        
        lines.append("")
        
        # Age statistics if available
        if stats.get('age') and stats['age'].get('count', 0) > 0:
            age_stats = stats['age']
            lines.extend([
                "⏰ AGE STATISTICS:",
                f"   Templates with Age: {age_stats.get('count', 0)}/{stats.get('cluster_size', 0)}",
                f"   Weighted Mean: {age_stats.get('weighted_mean', 0.0):.1f} ± {age_stats.get('weighted_uncertainty', 0.0):.1f} days",
                f"   Total Uncertainty: {age_stats.get('total_uncertainty', 0.0):.1f} days",
                f"   Range: {age_stats.get('min', 0.0):.1f} to {age_stats.get('max', 0.0):.1f} days",
                f"   Age Scatter: {age_stats.get('cluster_scatter', 0.0):.1f} days",
                ""
            ])
        
        # Subtype breakdown
        if stats.get('subtype_stats'):
            lines.append("🔍 SUBTYPE BREAKDOWN:")
            subtype_data = stats['subtype_stats']
            sorted_subtypes = sorted(subtype_data.items(), key=lambda x: x[1]['proportion'], reverse=True)
            
            for subtype, data in sorted_subtypes:
                proportion = data['proportion'] * 100
                lines.append(f"   {subtype}: {data['count']} templates ({proportion:.1f}%)")
                lines.append(f"      RLAP: {data['rlap_mean']:.1f}")
                lines.append(f"      Redshift: {data['redshift_weighted_mean']:.5f} ± {data['redshift_weighted_uncertainty']:.5f}")
                if data.get('age_count', 0) > 0:
                    lines.append(f"      Age: {data['age_weighted_mean']:.1f} ± {data['age_weighted_uncertainty']:.1f} days")
                lines.append("")
        
        self.stats_text.setPlainText("\n".join(lines))
    
    def _copy_summary(self):
        """Copy summary to clipboard"""
        if self.summary_text:
            QtWidgets.QApplication.clipboard().setText(self.summary_text.toPlainText())
            self._show_status_message("Summary copied to clipboard!")
    
    def _save_results(self):
        """Save results to file"""
        if not self.analyzer:
            return
        
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Save Analysis Results",
            "snid_analysis_results.txt",
            "Text Files (*.txt);;All Files (*)"
        )
        
        if file_path:
            try:
                with open(file_path, 'w') as f:
                    f.write(self.summary_text.toPlainText())
                    f.write("\n\n")
                    f.write(self.stats_text.toPlainText())
                
                self._show_status_message(f"Results saved to {file_path}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(
                    self,
                    "Save Error",
                    f"Failed to save results:\n{str(e)}"
                )
    
    def _show_all_matches(self):
        """Show all matches in table (currently already showing all)"""
        # This could be extended to implement filtering
        self._show_status_message("Showing all template matches")
    
    def _export_table(self):
        """Export matches table to CSV"""
        if not self.matches_table:
            return
        
        file_path, _ = QtWidgets.QFileDialog.getSaveFileName(
            self,
            "Export Template Matches",
            "template_matches.csv",
            "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            try:
                import csv
                
                with open(file_path, 'w', newline='') as f:
                    writer = csv.writer(f)
                    
                    # Write headers
                    headers = []
                    for col in range(self.matches_table.columnCount()):
                        headers.append(self.matches_table.horizontalHeaderItem(col).text())
                    writer.writerow(headers)
                    
                    # Write data
                    for row in range(self.matches_table.rowCount()):
                        row_data = []
                        for col in range(self.matches_table.columnCount()):
                            item = self.matches_table.item(row, col)
                            row_data.append(item.text() if item else "")
                        writer.writerow(row_data)
                
                self._show_status_message(f"Table exported to {file_path}")
            except Exception as e:
                QtWidgets.QMessageBox.critical(
                    self,
                    "Export Error",
                    f"Failed to export table:\n{str(e)}"
                )
    
    def _open_gmm_dialog(self):
        """Open GMM clustering dialog"""
        try:
            from snid_sage.interfaces.gui.components.pyside6_dialogs.gmm_clustering_dialog import PySide6GMMClusteringDialog
            
            gmm_dialog = PySide6GMMClusteringDialog(self, self.analysis_results)
            gmm_dialog.show()
            
        except ImportError:
            QtWidgets.QMessageBox.information(
                self,
                "GMM Clustering",
                "GMM clustering visualization will be implemented soon."
            )
    
    def _show_status_message(self, message):
        """Show a temporary status message"""
        # Could implement a status bar or temporary tooltip
        _LOGGER.info(message)


def show_analysis_results_dialog(parent, analysis_results=None, cluster_index=0):
    """
    Show the analysis results dialog.
    
    Args:
        parent: Parent window
        analysis_results: SNID analysis results object
        cluster_index: Index of cluster to display (default: 0 for winning cluster)
        
    Returns:
        PySide6AnalysisResultsDialog instance
    """
    dialog = PySide6AnalysisResultsDialog(parent, analysis_results, cluster_index)
    dialog.show()
    return dialog 