import sys
from PyQt5.QtWidgets import QApplication
from regex_log_analyzer.gui.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    exit_code = app.exec_()
    sys.exit(min(exit_code, 2147483647))

if __name__ == "__main__":
    main()