import json
import os
from typing import Any, Dict, Optional


class Config:
    """
    Read configuration json file

    Attributes:
        config_path (str): The path of the configuration file
        config_data (Dict): The configuration attributes

    Methods:
        load(): Load attributes from configuration
        get(key, default): Get one attribute
        has(key): Check if the attribute is loaded
        get_all(): Get all attributes
    """
    def __init__(self, config_path="config/example.json") -> None:
        self.config_path = config_path
        self.config_data: Dict[str, Any] = {}
        self.load()

    def load(self):
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    self.config_data = json.load(f)
                return True
            else:
                print(f"File not found: {self.config_path}")
                return False
        except Exception as e:
            print(f"Config load failed: {e}")
            return False

    def get(self, key, default=None):
        return self.config_data.get(key, default)

    def has(self, key):
        return key in self.config_data

    def get_all(self):
        return self.config_data.copy()
