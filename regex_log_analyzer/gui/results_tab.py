from PyQt5.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QFileDialog
import re

class ResultsTab(QWidget):
    def __init__(self, result_processor):
        super(ResultsTab, self).__init__()
        self.result_processor = result_processor
        self.init_ui()
        print("Initialized ResultsTab UI")

    def init_ui(self):
        # Set up the layout for the results tab
        self.layout = QVBoxLayout(self)

        # Create a QTableWidget to display regex results
        self.results_table = QTableWidget()
        self.layout.addWidget(self.results_table)
        print("Created results table")

        # Create buttons for saving results as text or CSV
        button_layout = QHBoxLayout()
        self.save_text_button = QPushButton("Save as Text")
        self.save_csv_button = QPushButton("Save as CSV")
        button_layout.addWidget(self.save_text_button)
        button_layout.addWidget(self.save_csv_button)
        self.layout.addLayout(button_layout)
        print("Created save buttons")

        # Connect buttons to their respective functions
        self.save_text_button.clicked.connect(self.save_as_text)
        self.save_csv_button.clicked.connect(self.save_as_csv)
        print("Connected save buttons to functions")

        # Connect the result_processor to update results when new results are available
        self.result_processor.results_updated.connect(self.display_results)
        print("Connected result processor to update results")

    def display_results(self, matches):
        if not matches:
            print("No matches to display")
            return

        # Determine the columns from the first match
        first_match = matches[0]
        if isinstance(first_match, re.Match):
            group_names = first_match.re.groupindex.keys()
            if group_names:
                columns = list(group_names)
            else:
                columns = [f"Regex Match {i+1}" for i in range(len(first_match.groups()))]
        else:
            columns = ["Regex Match"]

        print(f"Determined columns: {columns}")

        # Set the number of columns in the table
        self.results_table.setColumnCount(len(columns))
        self.results_table.setHorizontalHeaderLabels(columns)
        print(f"Set table column count to {len(columns)}")

        # Set the number of rows in the table to match the number of regex results
        self.results_table.setRowCount(len(matches))
        print(f"Set table row count to {len(matches)}")
        
        # Iterate through each match and add it to a new row in the results table
        for row_index, match in enumerate(matches):
            if isinstance(match, re.Match):
                for col_index, group_name in enumerate(columns):
                    if group_name in match.re.groupindex:
                        item = QTableWidgetItem(match.group(group_name))
                    elif col_index < len(match.groups()):
                        item = QTableWidgetItem(match.group(col_index + 1))
                    else:
                        item = QTableWidgetItem("")
                    self.results_table.setItem(row_index, col_index, item)
                    print(f"Set item at row {row_index}, column {col_index}: {item.text()}")
            else:
                item = QTableWidgetItem(match)
                self.results_table.setItem(row_index, 0, item)
                print(f"Set item at row {row_index}, column 0: {item.text()}")

    def save_as_text(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Results", "", "Text Files (*.txt)")
        if file_name:
            print(f"Saving results as text to {file_name}")
            self.result_processor.save_as_text(file_name)

    def save_as_csv(self):
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Results", "", "CSV Files (*.csv)")
        if file_name:
            print(f"Saving results as CSV to {file_name}")
            self.result_processor.save_as_csv(file_name)