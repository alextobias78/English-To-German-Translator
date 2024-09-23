import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                             QPushButton, QTextEdit, QLabel, QMessageBox, QDialog, QLineEdit, 
                             QSpacerItem, QSizePolicy, QFrame, QScrollArea, QStyleFactory,
                             QGraphicsDropShadowEffect)
from PyQt5.QtGui import QIcon, QFont, QPalette, QColor, QLinearGradient, QRadialGradient, QBrush, QPainter, QPen
from PyQt5.QtCore import Qt, QSize, pyqtSignal, QPropertyAnimation, QEasingCurve, QPoint, QTimer
from translator import Translator
from config_manager import ConfigManager

class CustomButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet("""
            QPushButton {
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
        """)
        self.shadow = QGraphicsDropShadowEffect(self)
        self.shadow.setBlurRadius(15)
        self.shadow.setXOffset(0)
        self.shadow.setYOffset(5)
        self.shadow.setColor(QColor(0, 0, 0, 80))
        self.setGraphicsEffect(self.shadow)
        
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setEasingCurve(QEasingCurve.OutQuad)
        self.animation.setDuration(100)

    def enterEvent(self, event):
        self.animation.setStartValue(self.pos())
        self.animation.setEndValue(self.pos() + QPoint(0, -5))
        self.animation.start()

    def leaveEvent(self, event):
        self.animation.setStartValue(self.pos())
        self.animation.setEndValue(self.pos() + QPoint(0, 5))
        self.animation.start()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        gradient = QLinearGradient(0, 0, 0, self.height())
        gradient.setColorAt(0, QColor("#4a148c"))
        gradient.setColorAt(1, QColor("#7c43bd"))

        painter.setBrush(QBrush(gradient))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(self.rect(), 5, 5)

        painter.setPen(QPen(Qt.white))
        painter.drawText(self.rect(), Qt.AlignCenter, self.text())

class ToggleSwitch(QWidget):
    toggled = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setFixedSize(60, 30)
        self.is_on = False
        self.animation = QPropertyAnimation(self, b"pos")
        self.animation.setDuration(300)
        self.animation.setEasingCurve(QEasingCurve.OutBounce)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        track_color = QColor("#7c43bd") if self.is_on else QColor("#cccccc")
        thumb_color = QColor("#ffffff")
        
        # Draw track
        track_gradient = QLinearGradient(0, 0, self.width(), 0)
        track_gradient.setColorAt(0, track_color.lighter())
        track_gradient.setColorAt(1, track_color.darker())
        painter.setBrush(QBrush(track_gradient))
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 5, 60, 20, 10, 10)
        
        # Draw thumb
        thumb_gradient = QRadialGradient(35 if self.is_on else 25, 15, 13)
        thumb_gradient.setColorAt(0, thumb_color)
        thumb_gradient.setColorAt(1, thumb_color.darker(110))
        painter.setBrush(QBrush(thumb_gradient))
        painter.setPen(QPen(Qt.lightGray, 0.5))
        if self.is_on:
            painter.drawEllipse(35, 2, 26, 26)
        else:
            painter.drawEllipse(0, 2, 26, 26)

    def mousePressEvent(self, event):
        self.is_on = not self.is_on
        self.animation.setStartValue(self.pos())
        self.animation.setEndValue(self.pos() + QPoint(5 if self.is_on else -5, 0))
        self.animation.start()
        QTimer.singleShot(100, self.update)  # Delay update for smooth animation
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
        self.setGeometry(100, 100, 1000, 800)
        
        # Set up the color scheme
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#2c3e50"))
        palette.setColor(QPalette.WindowText, Qt.white)
        palette.setColor(QPalette.Base, QColor("#34495e"))
        palette.setColor(QPalette.AlternateBase, QColor("#7f8c8d"))
        palette.setColor(QPalette.ToolTipBase, Qt.white)
        palette.setColor(QPalette.ToolTipText, Qt.white)
        palette.setColor(QPalette.Text, Qt.white)
        palette.setColor(QPalette.Button, QColor("#3498db"))
        palette.setColor(QPalette.ButtonText, Qt.white)
        palette.setColor(QPalette.BrightText, Qt.red)
        palette.setColor(QPalette.Highlight, QColor("#e74c3c"))
        palette.setColor(QPalette.HighlightedText, Qt.black)
        self.setPalette(palette)

        self.setStyleSheet("""
            QMainWindow {
                background-color: #2c3e50;
            }
            QLabel {
                font-size: 14px;
                color: #ecf0f1;
                font-weight: bold;
            }
            QTextEdit {
                background-color: #34495e;
                border: 2px solid #3498db;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                color: #ecf0f1;
            }
            QTextEdit:focus {
                border: 2px solid #e74c3c;
            }
            QScrollBar:vertical {
                border: none;
                background: #2c3e50;
                width: 10px;
                margin: 0px 0px 0px 0px;
            }
            QScrollBar::handle:vertical {
                background: #3498db;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Header
        header = QWidget()
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(20, 20, 20, 20)
        logo_label = QLabel("🌐 LinguaSwap")
        logo_label.setStyleSheet("font-size: 28px; font-weight: bold; color: #3498db;")
        header_layout.addWidget(logo_label)
        header_layout.addStretch()
        settings_button = CustomButton('⚙️ Settings')
        settings_button.clicked.connect(self.open_settings)
        header_layout.addWidget(settings_button)
        main_layout.addWidget(header)

        # Control panel
        control_panel = QWidget()
        control_layout = QHBoxLayout(control_panel)
        control_layout.setContentsMargins(20, 10, 20, 10)
        self.direction_toggle = ToggleSwitch(self)
        self.direction_toggle.toggled.connect(self.toggle_direction)
        self.en_label = QLabel('🇬🇧 EN')
        self.de_label = QLabel('DE 🇩🇪')
        self.en_label.setStyleSheet("font-size: 18px;")
        self.de_label.setStyleSheet("font-size: 18px;")
        control_layout.addWidget(self.en_label)
        control_layout.addWidget(self.direction_toggle)
        control_layout.addWidget(self.de_label)
        control_layout.addStretch()
        translate_button = CustomButton('Translate')
        translate_button.clicked.connect(self.translate)
        control_layout.addWidget(translate_button)
        clear_button = CustomButton('Clear All')
        clear_button.clicked.connect(self.clear_all)
        control_layout.addWidget(clear_button)
        main_layout.addWidget(control_panel)

        # Text areas
        text_layout = QHBoxLayout()
        text_layout.setContentsMargins(20, 20, 20, 20)
        text_layout.setSpacing(20)

        # Input area
        input_layout = QVBoxLayout()
        input_header = QHBoxLayout()
        input_header.addWidget(QLabel('Original Text:'))
        self.input_char_count = QLabel('Characters: 0')
        self.input_char_count.setStyleSheet("color: #bdc3c7;")
        input_header.addWidget(self.input_char_count)
        input_layout.addLayout(input_header)
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText("Enter text to translate...")
        input_layout.addWidget(self.input_text)
        text_layout.addLayout(input_layout)

        # Output area
        output_layout = QVBoxLayout()
        output_header = QHBoxLayout()
        output_header.addWidget(QLabel('Translated Text:'))
        self.output_char_count = QLabel('Characters: 0')
        self.output_char_count.setStyleSheet("color: #bdc3c7;")
        output_header.addWidget(self.output_char_count)
        output_layout.addLayout(output_header)
        self.output_text = QTextEdit()
        self.output_text.setReadOnly(True)
        self.output_text.setPlaceholderText("Translation will appear here...")
        output_layout.addWidget(self.output_text)
        copy_button = CustomButton('Copy to Clipboard')
        copy_button.clicked.connect(self.copy_to_clipboard)
        output_layout.addWidget(copy_button)
        text_layout.addLayout(output_layout)

        main_layout.addLayout(text_layout)

        # Add animations for text areas
        self.input_text_animation = QPropertyAnimation(self.input_text, b"geometry")
        self.output_text_animation = QPropertyAnimation(self.output_text, b"geometry")

        def animate_focus(widget, animation):
            animation.setDuration(200)
            animation.setStartValue(widget.geometry())
            animation.setEndValue(widget.geometry().adjusted(-5, -5, 5, 5))
            animation.start()

        def animate_blur(widget, animation):
            animation.setDuration(200)
            animation.setStartValue(widget.geometry())
            animation.setEndValue(widget.geometry().adjusted(5, 5, -5, -5))
            animation.start()

        self.input_text.focusInEvent = lambda e: animate_focus(self.input_text, self.input_text_animation)
        self.input_text.focusOutEvent = lambda e: animate_blur(self.input_text, self.input_text_animation)
        self.output_text.focusInEvent = lambda e: animate_focus(self.output_text, self.output_text_animation)
        self.output_text.focusOutEvent = lambda e: animate_blur(self.output_text, self.output_text_animation)

        # Connect text changed signals
        self.input_text.textChanged.connect(self.update_char_count)
        self.output_text.textChanged.connect(self.update_char_count)

        self.update_direction_labels(self.direction_toggle.is_on)

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
            # If is_on is True, we're translating from German to English
            translated_text = self.translator.translate(input_text, to_german=not self.direction_toggle.is_on)
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
            print("Translating from German to English")
        else:
            print("Translating from English to German")
        self.update_direction_labels(is_on)

    def update_direction_labels(self, is_on):
        if is_on:
            self.en_label.setStyleSheet("font-weight: bold;")
            self.de_label.setStyleSheet("font-weight: normal;")
        else:
            self.en_label.setStyleSheet("font-weight: normal;")
            self.de_label.setStyleSheet("font-weight: bold;")

    def update_char_count(self):
        self.input_char_count.setText(f'Characters: {len(self.input_text.toPlainText())}')
        self.output_char_count.setText(f'Characters: {len(self.output_text.toPlainText())}')

    def clear_all(self):
        self.input_text.clear()
        self.output_text.clear()

    def copy_to_clipboard(self):
        clipboard = QApplication.clipboard()
        clipboard.setText(self.output_text.toPlainText())
        
        # Store the original style
        original_style = self.sender().styleSheet()
        
        # Change the button color briefly
        self.sender().setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
                font-weight: bold;
            }
        """)
        
        # Reset the button style after a short delay
        QTimer.singleShot(300, lambda: self.sender().setStyleSheet(original_style))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    translator_app = TranslatorApp()
    translator_app.show()
    sys.exit(app.exec_())
