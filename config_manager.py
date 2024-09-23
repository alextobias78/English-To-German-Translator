import json
import os

class ConfigManager:
    def __init__(self):
        self.config_file = 'config.json'
        self.config = self.load_config()

    def load_config(self):
        if os.path.exists(self.config_file):
            with open(self.config_file, 'r') as f:
                return json.load(f)
        return {"api_key": ""}

    def save_config(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.config, f)

    def get_api_key(self):
        return self.config.get("api_key", "")

    def set_api_key(self, api_key):
        self.config["api_key"] = api_key
        self.save_config()
