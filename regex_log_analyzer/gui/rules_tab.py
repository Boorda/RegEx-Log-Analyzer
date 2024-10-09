from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
                             QListWidget, QTextEdit, QLabel, QSplitter, QInputDialog,
                             QMessageBox)
from PyQt5.QtCore import Qt
from regex_log_analyzer.gui.rule_dialog import RuleDialog
from regex_log_analyzer.utils.regex_highlighter import RegexHighlighter
from regex_log_analyzer.utils.file_utils import save_file, browse_file
import json

class RulesTab(QWidget):
    def __init__(self, rule_manager, file_parser, result_processor):
        """
        Initialize the RulesTab.
        
        :param rule_manager: Instance of RuleManager
        :param file_parser: Instance of FileParser
        :param result_processor: Instance of ResultProcessor
        """
        super().__init__()
        self.rule_manager = rule_manager
        self.file_parser = file_parser
        self.result_processor = result_processor
        self.init_ui()

    def init_ui(self):
        """Set up the user interface for the RulesTab."""
        layout = QHBoxLayout(self)

        # Left side: Config info, List and buttons
        left_layout = QVBoxLayout()
        
        self.config_name_label = QLabel("Config Name: ")
        self.config_description_label = QLabel("Description: ")
        left_layout.addWidget(self.config_name_label)
        left_layout.addWidget(self.config_description_label)

        self.rules_list = QListWidget()
        self.rules_list.itemSelectionChanged.connect(self.on_selection_changed)
        left_layout.addWidget(self.rules_list)

        # Button layout
        button_layout = QHBoxLayout()
        self.add_button = QPushButton('Add Rule')
        self.edit_button = QPushButton('Edit Rule')
        self.delete_button = QPushButton('Delete Rule')
        self.run_button = QPushButton('Run Rule')
        self.run_button.setEnabled(False)
        
        button_layout.addWidget(self.add_button)
        button_layout.addWidget(self.edit_button)
        button_layout.addWidget(self.delete_button)
        button_layout.addWidget(self.run_button)
        
        left_layout.addLayout(button_layout)

        # Config button layout
        config_button_layout = QHBoxLayout()
        self.load_config_button = QPushButton('Load Config')
        self.save_config_button = QPushButton('Save Config')
        config_button_layout.addWidget(self.load_config_button)
        config_button_layout.addWidget(self.save_config_button)
        
        left_layout.addLayout(config_button_layout)

        # Right side: Description and Regex
        right_layout = QVBoxLayout()
        self.description_label = QLabel("Description:")
        self.description_text = QTextEdit()
        self.description_text.setReadOnly(True)
        right_layout.addWidget(self.description_label)
        right_layout.addWidget(self.description_text)

        self.regex_label = QLabel("Regular Expression:")
        self.regex_text = QTextEdit()
        self.regex_text.setReadOnly(True)
        self.regex_highlighter = RegexHighlighter(self.regex_text.document())
        right_layout.addWidget(self.regex_label)
        right_layout.addWidget(self.regex_text)

        # Add layouts to main layout
        splitter = QSplitter(Qt.Horizontal)
        left_widget = QWidget()
        left_widget.setLayout(left_layout)
        right_widget = QWidget()
        right_widget.setLayout(right_layout)
        splitter.addWidget(left_widget)
        splitter.addWidget(right_widget)
        layout.addWidget(splitter)

        # Connect buttons to functions
        self.add_button.clicked.connect(self.add_rule)
        self.edit_button.clicked.connect(self.edit_rule)
        self.delete_button.clicked.connect(self.delete_rule)
        self.run_button.clicked.connect(self.run_rule)
        self.load_config_button.clicked.connect(self.load_config)
        self.save_config_button.clicked.connect(self.save_config)

        self.update_list()

    def update_list(self):
        """Update the list of rules displayed in the UI."""
        self.rules_list.clear()
        for rule in self.rule_manager.get_rules():
            self.rules_list.addItem(rule['name'])

    def on_selection_changed(self):
        """Handle changes in rule selection."""
        selected_items = self.rules_list.selectedItems()
        if selected_items:
            rule = self.rule_manager.get_rule_by_name(selected_items[0].text())
            if rule:
                self.description_text.setText(rule['description'])
                self.regex_text.setText(rule['regex'])
            else:
                self.clear_details()
        else:
            self.clear_details()

    def clear_details(self):
        """Clear the description and regex text fields."""
        self.description_text.clear()
        self.regex_text.clear()

    def add_rule(self):
        """Open a dialog to add a new rule."""
        dialog = RuleDialog(self)
        if dialog.exec_():
            new_rule = dialog.get_rule()
            self.rule_manager.add_rule(new_rule)
            self.update_list()

    def edit_rule(self):
        """Open a dialog to edit the selected rule."""
        selected_items = self.rules_list.selectedItems()
        if selected_items:
            rule = self.rule_manager.get_rule_by_name(selected_items[0].text())
            if rule:
                dialog = RuleDialog(self, rule)
                if dialog.exec_():
                    updated_rule = dialog.get_rule()
                    self.rule_manager.update_rule(updated_rule)
                    self.update_list()
                    self.on_selection_changed()

    def delete_rule(self):
        """Delete the selected rule."""
        selected_items = self.rules_list.selectedItems()
        if selected_items:
            rule = self.rule_manager.get_rule_by_name(selected_items[0].text())
            if rule:
                self.rule_manager.delete_rule(rule['id'])
                self.update_list()
                self.clear_details()

    def enable_run_buttons(self, enabled):
        """Enable or disable the run button."""
        self.run_button.setEnabled(enabled)

    def run_rule(self):
        """Run the selected rule on the loaded file."""
        selected_items = self.rules_list.selectedItems()
        if selected_items:
            rule = self.rule_manager.get_rule_by_name(selected_items[0].text())
            if rule:
                results = self.file_parser.apply_rule(rule['regex'])
                self.result_processor.set_results(results)

    def load_config(self):
        file_path = browse_file(self, "Load Configuration", "JSON Files (*.json)")
        if file_path:
            try:
                self.rule_manager.load_config(file_path)
                self.update_config_info()
                self.update_list()
                QMessageBox.information(self, "Success", "Configuration loaded successfully.")
            except json.JSONDecodeError as e:
                QMessageBox.warning(self, "Error", f"Invalid JSON format: {str(e)}")
            except FileNotFoundError:
                QMessageBox.warning(self, "Error", f"File not found: {file_path}")
            except Exception as e:
                QMessageBox.warning(self, "Error", f"Unexpected error: {str(e)}")

    def save_config(self):
        """Save the current configuration to a file."""
        name, ok = QInputDialog.getText(self, "Save Configuration", "Enter configuration name:")
        if ok and name:
            description, ok = QInputDialog.getText(self, "Save Configuration", "Enter configuration description:")
            if ok:
                self.rule_manager.set_config_info(name, description)
                file_path = save_file(self, "Save Configuration", "JSON Files (*.json)", ".json")
                if file_path:
                    try:
                        self.rule_manager.save_config(file_path)
                        self.update_config_info()
                        QMessageBox.information(self, "Success", "Configuration saved successfully.")
                    except Exception as e:
                        QMessageBox.warning(self, "Error", str(e))

    def update_config_info(self):
        """Update the displayed configuration information."""
        config_info = self.rule_manager.get_config_info()
        self.config_name_label.setText(f"Config Name: {config_info['name']}")
        self.config_description_label.setText(f"Description: {config_info['description']}")