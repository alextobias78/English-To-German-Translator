from openai import OpenAI
from config_manager import ConfigManager
import requests

class Translator:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.client = None
        self.update_api_key(self.config_manager.get_api_key())

    def translate(self, text, to_german=True):
        if not self.client:
            raise Exception("API key is not set or invalid.")

        try:
            system_content = "You are the perfect English to German translator." if to_german else "You are the perfect German to English translator."
            response = self.client.chat.completions.create(
                model="gpt-4",  # Changed from "chatgpt-4o-latest" to "gpt-4"
                messages=[
                    {"role": "system", "content": system_content},
                    {"role": "user", "content": f"Translate the following:\n\n{text}"}
                ],
                temperature=0,
                max_tokens=1000,  # Reduced from 16383 to a more reasonable number
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            return response.choices[0].message.content.strip()
        except requests.exceptions.RequestException as e:
            raise Exception(f"Network error: {str(e)}. Please check your internet connection.")
        except Exception as e:
            raise Exception(f"Translation error: {str(e)}. Please check your API key and try again.")

    def update_api_key(self, api_key):
        if api_key:
            self.client = OpenAI(api_key=api_key)
        else:
            self.client = None
