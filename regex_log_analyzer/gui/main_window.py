from PyQt5.QtWidgets import QMainWindow, QTabWidget, QVBoxLayout, QWidget
from regex_log_analyzer.gui.view_tab import ViewTab
from regex_log_analyzer.gui.results_tab import ResultsTab
from regex_log_analyzer.gui.rules_tab import RulesTab
from regex_log_analyzer.core.file_parser import FileParser
from regex_log_analyzer.core.rule_manager import RuleManager
from regex_log_analyzer.core.result_processor import ResultProcessor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("RegEx Log Analyzer")
        self.setGeometry(100, 100, 1200, 800)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        self.tab_widget = QTabWidget()
        self.layout.addWidget(self.tab_widget)

        self.file_parser = FileParser()
        self.rule_manager = RuleManager()
        self.result_processor = ResultProcessor()

        self.view_tab = ViewTab(self.file_parser)
        self.tab_widget.addTab(self.view_tab, "View")
        
        self.rules_tab = RulesTab(self.rule_manager, self.file_parser, self.result_processor)
        self.tab_widget.addTab(self.rules_tab, "Rules")
        
        self.results_tab = ResultsTab(self.result_processor)
        self.tab_widget.addTab(self.results_tab, "Results")

        self.view_tab.file_loaded.connect(self.rules_tab.enable_run_buttons)
        self.result_processor.results_updated.connect(self.results_tab.display_results)

    def load_default_config(self):
        # Load the default AVFS Log Analyzer configuration
        default_config = {
            "name": "AVFS Log Analyzer",
            "description": "Analyzes the Autodesk AVFS logs based on RegEx rules",
            "rules": [
                # Add your default rules here
            ]
        }
        self.rule_manager.current_config = default_config
        self.rules_tab.update_config_info()
        self.rules_tab.update_list()

if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    main_window.load_default_config()
    sys.exit(app.exec_())