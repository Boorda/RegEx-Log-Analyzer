import uuid
from regex_log_analyzer.utils.file_utils import load_json, save_json

class RuleManager:
    def __init__(self):
        """Initialize the RuleManager with a default configuration."""
        self.current_config = {
            "name": "Default Configuration",
            "description": "Default configuration for RegEx Log Analyzer",
            "rules": []
        }

    def get_rules(self):
        """
        Get all rules in the current configuration.
        
        :return: List of rule dictionaries
        """
        return self.current_config["rules"]

    def get_rule_by_name(self, name):
        """
        Get a specific rule by its name.
        
        :param name: Name of the rule to retrieve
        :return: Rule dictionary if found, None otherwise
        """
        return next((rule for rule in self.current_config["rules"] if rule['name'] == name), None)

    def add_rule(self, rule):
        """
        Add a new rule to the current configuration.
        
        :param rule: Rule dictionary to add
        """
        rule['id'] = str(uuid.uuid4())  # Generate a new UUID for the rule
        self.current_config["rules"].append(rule)

    def update_rule(self, updated_rule):
        """
        Update an existing rule in the current configuration.
        
        :param updated_rule: Updated rule dictionary
        """
        self.current_config["rules"] = [updated_rule if r['id'] == updated_rule['id'] else r for r in self.current_config["rules"]]

    def delete_rule(self, rule_id):
        """
        Delete a rule from the current configuration.
        
        :param rule_id: ID of the rule to delete
        """
        self.current_config["rules"] = [r for r in self.current_config["rules"] if r['id'] != rule_id]

    def load_config(self, file_path):
        """
        Load a configuration from a JSON file.
        
        :param file_path: Path to the JSON file
        :raises ValueError: If loading fails
        """
        try:
            self.current_config = load_json(file_path)
        except Exception as e:
            raise ValueError(f"Failed to load configuration: {str(e)}")

    def save_config(self, file_path):
        """
        Save the current configuration to a JSON file.
        
        :param file_path: Path to save the JSON file
        :raises ValueError: If saving fails
        """
        try:
            save_json(file_path, self.current_config)
        except Exception as e:
            raise ValueError(f"Failed to save configuration: {str(e)}")

    def set_config_info(self, name, description):
        """
        Set the name and description of the current configuration.
        
        :param name: Name of the configuration
        :param description: Description of the configuration
        """
        self.current_config["name"] = name
        self.current_config["description"] = description

    def get_config_info(self):
        """
        Get the name and description of the current configuration.
        
        :return: Dictionary with 'name' and 'description' keys
        """
        return {
            "name": self.current_config["name"],
            "description": self.current_config["description"]
        }