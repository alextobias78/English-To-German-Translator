import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTextEdit, QLabel, QMessageBox, QDialog, QLineEdit
from translator import Translator
from config_manager import ConfigManager

class SettingsDialog(QDialog):
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Settings')
        layout = QVBoxLayout(self)
        
        self.api_key_input = QLineEdit(self)
        self.api_key_input.setText(self.config_manager.get_api_key())
        
        save_button = QPushButton('Save', self)
        save_button.clicked.connect(self.save_settings)
        
        layout.addWidget(QLabel('API Key:'))
        layout.addWidget(self.api_key_input)
        layout.addWidget(save_button)

    def save_settings(self):
        api_key = self.api_key_input.text()
        self.config_manager.set_api_key(api_key)
        self.accept()

class TranslatorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.translator = Translator()
        self.config_manager = ConfigManager()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('English-German Translator')
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)

        self.input_text = QTextEdit()
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)

        button_layout = QHBoxLayout()
        translate_button = QPushButton('Translate')
        translate_button.clicked.connect(self.translate)
        settings_button = QPushButton('Settings')
        settings_button.clicked.connect(self.open_settings)
        self.toggle_direction_button = QPushButton('English to German')
        self.toggle_direction_button.clicked.connect(self.toggle_direction)

        button_layout.addWidget(translate_button)
        button_layout.addWidget(self.toggle_direction_button)
        button_layout.addWidget(settings_button)

        layout.addWidget(QLabel('Enter text:'))
        layout.addWidget(self.input_text)
        layout.addLayout(button_layout)
        layout.addWidget(QLabel('Translation:'))
        layout.addWidget(self.output_text)

    def translate(self):
        if not self.config_manager.get_api_key():
            QMessageBox.warning(self, "API Key Missing", "Please set your API key in the settings.")
            return

        input_text = self.input_text.toPlainText()
        if input_text:
            try:
                translated_text = self.translator.translate(input_text, self.toggle_direction_button.text() == "English to German")
                self.output_text.setPlainText(translated_text)
            except Exception as e:
                self.output_text.setPlainText(f"Error: {str(e)}")
        else:
            self.output_text.setPlainText("Please enter some text to translate.")

    def open_settings(self):
        dialog = SettingsDialog(self.config_manager)
        if dialog.exec_():
            self.translator.update_api_key(self.config_manager.get_api_key())

    def toggle_direction(self):
        current_text = self.toggle_direction_button.text()
        if current_text == "English to German":
            self.toggle_direction_button.setText("German to English")
        else:
            self.toggle_direction_button.setText("English to German")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    translator_app = TranslatorApp()
    translator_app.show()
    sys.exit(app.exec_())
