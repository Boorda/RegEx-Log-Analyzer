import json
import os
from PyQt5.QtWidgets import QFileDialog


def is_valid_log_file(file_path):
    return os.path.basename(file_path).startswith("AVFS-log") and file_path.endswith(".txt")

def browse_file(parent, title="Open File", file_filter="All Files (*)"):
    """
    Open a file dialog to browse for a file.
    
    :param parent: Parent widget
    :param title: Dialog title
    :param file_filter: File filter string
    :return: Selected file path or None if cancelled
    """
    file_path, _ = QFileDialog.getOpenFileName(parent, title, "", file_filter)
    return file_path if file_path else None

def save_file(parent, title="Save File", file_filter="All Files (*)", default_suffix=None):
    """
    Open a file dialog to save a file.
    
    :param parent: Parent widget
    :param title: Dialog title
    :param file_filter: File filter string
    :param default_suffix: Default file suffix (e.g., '.json')
    :return: Selected file path or None if cancelled
    """
    options = QFileDialog.Options()
    if default_suffix:
        options |= QFileDialog.DontConfirmOverwrite
    file_path, _ = QFileDialog.getSaveFileName(parent, title, "", file_filter, options=options)
    if file_path:
        if default_suffix and not file_path.endswith(default_suffix):
            file_path += default_suffix
    return file_path



def load_json(file_path):
    """
    Load JSON data from a file.

    :param file_path: Path to the JSON file
    :return: Loaded JSON data as a Python object
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    if os.path.getsize(file_path) == 0:
        raise ValueError("The file is empty. Please provide a valid JSON file.")

    with open(file_path, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError as e:
            raise ValueError(f"Failed to parse JSON file: {e}")

def save_json(file_path, data):
    """
    Save Python object as JSON to a file.
    
    :param file_path: Path to save the JSON file
    :param data: Python object to be saved as JSON
    """
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def get_supported_file_filters():
    """
    Return a string of supported file filters for the application.
    
    :return: File filter string
    """
    return "Text Files (*.txt);;Log Files (*.log);;XML Files (*.xml);;JSON Files (*.json);;XAML Files (*.xaml);;CSV Files (*.csv);;All Files (*)"