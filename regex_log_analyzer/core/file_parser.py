import re
import json
import csv
import xml.etree.ElementTree as ET

class FileParser:
    def __init__(self):
        self.content = ""
        self.file_type = ""

    def load_file(self, file_path):
        """
        Load and parse the content of a file based on its type.
        
        :param file_path: Path to the file to be loaded
        :raises ValueError: If the file type is unsupported or the file is invalid
        """
        self.file_type = file_path.split('.')[-1].lower()
        
        with open(file_path, 'r', encoding='utf-8') as file:
            if self.file_type in ['txt', 'log', 'csv', 'xml', 'json', 'xaml']:
                self.content = file.read()
            else:
                raise ValueError(f"Unsupported file type: {self.file_type}")

        # Additional parsing for structured formats
        if self.file_type == 'json':
            self._parse_json()
        elif self.file_type in ['xml', 'xaml']:
            self._parse_xml()
        elif self.file_type == 'csv':
            self._parse_csv()

    def get_file_content(self):
        """
        Get the parsed content of the loaded file.
        
        :return: String representation of the file content
        """
        return self.content

    def apply_rule(self, regex):
        """
        Apply a regular expression rule to the file content.
        
        :param regex: Regular expression string
        :return: List of all matches found
        """
        pattern = re.compile(regex, re.MULTILINE | re.DOTALL)
        return pattern.findall(self.content)

    def _parse_json(self):
        """Parse and format JSON content."""
        try:
            parsed = json.loads(self.content)
            self.content = json.dumps(parsed, indent=2)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")

    def _parse_xml(self):
        """Parse and format XML content."""
        try:
            root = ET.fromstring(self.content)
            self.content = ET.tostring(root, encoding='unicode', method='xml')
        except ET.ParseError:
            raise ValueError("Invalid XML format")

    def _parse_csv(self):
        """Parse and format CSV content."""
        try:
            lines = self.content.splitlines()
            reader = csv.reader(lines)
            rows = list(reader)
            self.content = '\n'.join([','.join(row) for row in rows])
        except csv.Error:
            raise ValueError("Invalid CSV format")