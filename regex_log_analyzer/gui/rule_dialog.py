from PyQt5.QtWidgets import QDialog, QFormLayout, QLineEdit, QTextEdit, QPushButton, QHBoxLayout

class RuleDialog(QDialog):
    def __init__(self, parent=None, rule=None):
        """
        Initialize the RuleDialog.
        
        :param parent: Parent widget
        :param rule: Existing rule data if editing, None if creating new
        """
        super().__init__(parent)
        self.rule = rule
        self.init_ui()

    def init_ui(self):
        """Set up the user interface for the dialog."""
        self.setWindowTitle("Rule Configuration")
        layout = QFormLayout(self)

        # Create input fields
        self.name_edit = QLineEdit(self)
        self.description_edit = QTextEdit(self)
        self.regex_edit = QLineEdit(self)

        # Add input fields to layout
        layout.addRow('Name:', self.name_edit)
        layout.addRow('Description:', self.description_edit)
        layout.addRow('Regex:', self.regex_edit)

        # Create and add buttons
        buttons = QHBoxLayout()
        self.ok_button = QPushButton('OK')
        self.cancel_button = QPushButton('Cancel')
        buttons.addWidget(self.ok_button)
        buttons.addWidget(self.cancel_button)
        layout.addRow(buttons)

        # Connect button signals
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        # Populate fields if editing an existing rule
        if self.rule:
            self.name_edit.setText(self.rule['name'])
            self.description_edit.setText(self.rule['description'])
            self.regex_edit.setText(self.rule['regex'])

    def get_rule(self):
        """
        Retrieve the rule data from the dialog fields.
        
        :return: Dictionary containing rule data
        """
        return {
            'id': self.rule['id'] if self.rule else None,  # ID will be set by RuleManager if it's a new rule
            'name': self.name_edit.text(),
            'description': self.description_edit.toPlainText(),
            'regex': self.regex_edit.text()
        }