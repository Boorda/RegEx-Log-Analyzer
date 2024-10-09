from PyQt5.QtCore import QObject, pyqtSignal
import csv

class ResultProcessor(QObject):
    results_updated = pyqtSignal(list)

    def __init__(self):
        super().__init__()
        self.results = []

    def set_results(self, results):
        self.results = results
        self.results_updated.emit(self.results)

    def save_as_text(self, file_path):
        with open(file_path, 'w') as f:
            for result in self.results:
                f.write(str(result) + '\n')

    def save_as_csv(self, file_path):
        with open(file_path, 'w', newline='') as f:
            writer = csv.writer(f)
            for result in self.results:
                if isinstance(result, tuple):
                    writer.writerow(result)
                else:
                    writer.writerow([result])