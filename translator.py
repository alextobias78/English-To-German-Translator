from openai import OpenAI
from config_manager import ConfigManager

class Translator:
    def __init__(self):
        self.config_manager = ConfigManager()
        self.client = OpenAI(api_key=self.config_manager.get_api_key())

    def translate(self, text, to_german=True):
        try:
            system_content = "You are the perfect English to German translator." if to_german else "You are the perfect German to English translator."
            response = self.client.chat.completions.create(
                model="chatgpt-4o-latest",
                messages=[
                    {
                        "role": "system",
                        "content": [
                            {
                                "type": "text",
                                "text": system_content
                            }
                        ]
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": f"Translate the following:\n\n{text}"
                            }
                        ]
                    }
                ],
                temperature=0,
                max_tokens=16383,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0,
                response_format={
                    "type": "text"
                }
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise Exception(f"Translation error: {str(e)}")

    def update_api_key(self, api_key):
        self.client = OpenAI(api_key=api_key)
