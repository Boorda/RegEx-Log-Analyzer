from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QTextEdit
from PyQt5.QtCore import pyqtSignal
from regex_log_analyzer.utils.file_utils import browse_file, get_supported_file_filters

class ViewTab(QWidget):
    file_loaded = pyqtSignal(bool)

    def __init__(self, log_parser):
        super().__init__()
        self.log_parser = log_parser
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_file)
        layout.addWidget(self.browse_button)

        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

    def browse_file(self):
        file_name = browse_file(self, "Open Log File", get_supported_file_filters())
        if file_name:
            try:
                self.log_parser.load_file(file_name)
                self.text_edit.setText(self.log_parser.get_file_content())
                self.file_loaded.emit(True)
            except Exception as e:
                self.text_edit.setText(f"Error loading file: {str(e)}")
                self.file_loaded.emit(False)
        else:
            self.file_loaded.emit(False)

    def get_loaded_content(self):
        return self.text_edit.toPlainText()