import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTextEdit, QLabel, QMessageBox, QDialog, QLineEdit, 
                             QSpacerItem, QSizePolicy, QFrame, QScrollArea, QStyleFactory)
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor
from PyQt5.QtCore import Qt, QSize, pyqtSignal
from translator import Translator
from config_manager import ConfigManager

class CustomButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                background-color: #1a237e;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #283593;
            }
            QPushButton:pressed {
                background-color: #0d47a1;
            }
        """)

class ToggleSwitch(QWidget):
    toggled = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 30)
        self.is_on = False

    def paintEvent(self, event):
        from PyQt5.QtGui import QPainter, QColor, QPen, QBrush
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        track_color = QColor("#1a237e") if self.is_on else QColor("#cccccc")
        thumb_color = QColor("#ffffff")
        
        # Draw track
        painter.setPen(Qt.NoPen)
        painter.setBrush(QBrush(track_color))
        painter.drawRoundedRect(0, 5, 60, 20, 10, 10)
        
        # Draw thumb
        painter.setPen(QPen(Qt.black, 1))
        painter.setBrush(QBrush(thumb_color))
        if self.is_on:
            painter.drawEllipse(35, 2, 26, 26)
        else:
            painter.drawEllipse(0, 2, 26, 26)

    def mousePressEvent(self, event):
        self.is_on = not self.is_on
        self.update()
        self.toggled.emit(self.is_on)

class SettingsDialog(QDialog):
    def __init__(self, config_manager):
        super().__init__()
        self.config_manager = config_manager
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Settings')
        self.setStyleSheet("""
            QDialog {
                background-color: #f5f5f5;
            }
            QLabel {
                font-size: 14px;
                color: #333333;
            }
            QLineEdit {
                padding: 5px;
                border: 1px solid #cccccc;
                border-radius: 3px;
            }
        """)
        layout = QVBoxLayout(self)
        
        self.api_key_input = QLineEdit(self)
        self.api_key_input.setText(self.config_manager.get_api_key())
        
        save_button = CustomButton('Save', self)
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
        self.setWindowTitle('LinguaSwap')
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f5f5f5;
            }
            QLabel {
                font-size: 14px;
                color: #333333;
            }
            QTextEdit {
                background-color: white;
                border: 1px solid #cccccc;
                border-radius: 5px;
                padding: 5px;
            }
        """)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Header
        header = QWidget()
        header_layout = QHBoxLayout(header)
        logo_label = QLabel("🌐 LinguaSwap")
        logo_label.setStyleSheet("font-size: 24px; font-weight: bold; color: #1a237e;")
        header_layout.addWidget(logo_label)
        header_layout.addStretch()
        settings_button = CustomButton('⚙️ Settings')
        settings_button.clicked.connect(self.open_settings)
        header_layout.addWidget(settings_button)
        main_layout.addWidget(header)

        # Input area
        input_container = QFrame()
        input_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        input_layout = QVBoxLayout(input_container)
        input_layout.addWidget(QLabel('Original Text:'))
        self.input_text = QTextEdit()
        input_layout.addWidget(self.input_text)
        self.input_char_count = QLabel('Characters: 0')
        input_layout.addWidget(self.input_char_count)
        main_layout.addWidget(input_container)

        # Control panel
        control_panel = QWidget()
        control_layout = QHBoxLayout(control_panel)
        self.direction_toggle = ToggleSwitch(self)
        self.direction_toggle.toggled.connect(self.toggle_direction)
        control_layout.addWidget(QLabel('🇬🇧'))
        control_layout.addWidget(self.direction_toggle)
        control_layout.addWidget(QLabel('🇩🇪'))
        translate_button = CustomButton('Translate')
        translate_button.clicked.connect(self.translate)
        control_layout.addWidget(translate_button)
        clear_button = CustomButton('Clear All')
        clear_button.clicked.connect(self.clear_all)
        control_layout.addWidget(clear_button)
        main_layout.addWidget(control_panel)

        # Output area
        output_container = QFrame()
        output_container.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 10px;
                padding: 10px;
            }
        """)
        output_layout = QVBoxLayout(output_container)
        output_layout.addWidget(QLabel('Translated Text:'))
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        output_layout.addWidget(self.output_text)
        self.output_char_count = QLabel('Characters: 0')
        output_layout.addWidget(self.output_char_count)
        copy_button = CustomButton('Copy to Clipboard')
        copy_button.clicked.connect(self.copy_to_clipboard)
        output_layout.addWidget(copy_button)
        main_layout.addWidget(output_container)

        # Connect text changed signals
        self.input_text.textChanged.connect(self.update_char_count)
        self.output_text.textChanged.connect(self.update_char_count)

    def translate(self):
        api_key = self.config_manager.get_api_key()
        if not api_key:
            QMessageBox.warning(self, "API Key Missing", "Please set your API key in the settings.")
            return

        input_text = self.input_text.toPlainText()
        if not input_text:
            self.output_text.setPlainText("Please enter some text to translate.")
            return

        try:
            translated_text = self.translator.translate(input_text, not self.direction_toggle.is_on)
            self.output_text.setPlainText(translated_text)
        except Exception as e:
            error_message = str(e)
            self.output_text.setPlainText(f"Error: {error_message}")
            if "Network error" in error_message:
                QMessageBox.critical(self, "Network Error", "Unable to connect to the translation service. Please check your internet connection and try again.")
            elif "API key is not set or invalid" in error_message:
                QMessageBox.critical(self, "API Key Error", "Your API key appears to be invalid. Please check your settings and ensure you've entered a valid API key.")
            else:
                QMessageBox.critical(self, "Translation Error", f"An error occurred during translation: {error_message}")

    def open_settings(self):
        dialog = SettingsDialog(self.config_manager)
        if dialog.exec_():
            self.translator.update_api_key(self.config_manager.get_api_key())

    def toggle_direction(self, is_on):
        # Update the translation direction based on the toggle state
        if is_on:
            print("Translating from English to German")
        else:
            print("Translating from German to English")
        # You can add more logic here if needed

    def update_char_count(self):
        self.input_char_count.setText(f'Characters: {len(self.input_text.toPlainText())}')
        self.output_char_count.setText(f'Characters: {len(self.output_text.toPlainText())}')

    def clear_all(self):
        self.input_text.clear()
        self.output_text.clear()

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.output_text.toPlainText())
        QMessageBox.information(self, "Copied", "Text copied to clipboard!")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    translator_app = TranslatorApp()
    translator_app.show()
    sys.exit(app.exec_())
