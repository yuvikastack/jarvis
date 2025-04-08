from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QTextEdit, QPushButton, QLabel, QStackedWidget
from PyQt5.QtCore import QTimer
import sys
import os

# Directory Paths for Temp Data
current_dir = os.getcwd()
TempDirPath = os.path.join(current_dir, "Temp")

# Ensure Temp Directory Exists
os.makedirs(TempDirPath, exist_ok=True)

# File paths for microphone, assistant status, and response data
mic_file = os.path.join(TempDirPath, "Mic.data")
status_file = os.path.join(TempDirPath, "Status.data")
response_file = os.path.join(TempDirPath, "Response.data")

# Functions for Status Handling
def SetMicrophoneStatus(command):
    with open(mic_file, "w", encoding="utf-8") as file:
        file.write(command)

def GetMicrophoneStatus():
    if os.path.exists(mic_file):
        with open(mic_file, "r", encoding="utf-8") as file:
            return file.read()
    return "Unknown"

def SetAssistantStatus(status):
    with open(status_file, "w", encoding="utf-8") as file:
        file.write(status)

def GetAssistantStatus():
    if os.path.exists(status_file):
        with open(status_file, "r", encoding="utf-8") as file:
            return file.read()
    return "Idle"

def GetChatResponse():
    if os.path.exists(response_file):
        with open(response_file, "r", encoding="utf-8") as file:
            return file.read()
    return ""

# Chat Section
class ChatSection(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        
        self.status_label = QLabel("Assistant Status: " + GetAssistantStatus())
        self.mic_status_label = QLabel("Mic Status: " + GetMicrophoneStatus())

        self.toggle_mic_button = QPushButton("Toggle Mic")
        self.toggle_mic_button.clicked.connect(self.toggleMic)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateStatus)
        self.timer.timeout.connect(self.showText)
        self.timer.start(1000)

        layout.addWidget(self.chat_text_edit)
        layout.addWidget(self.status_label)
        layout.addWidget(self.mic_status_label)
        layout.addWidget(self.toggle_mic_button)
        self.setLayout(layout)

    def toggleMic(self):
        current_status = GetMicrophoneStatus()
        new_status = "On" if current_status == "Off" else "Off"
        SetMicrophoneStatus(new_status)
        self.mic_status_label.setText(f"Mic Status: {new_status}")

    def updateStatus(self):
        self.status_label.setText("Assistant Status: " + GetAssistantStatus())
        self.mic_status_label.setText("Mic Status: " + GetMicrophoneStatus())

    def showText(self):
        chat_content = GetChatResponse()
        if chat_content:
            self.chat_text_edit.setPlainText(chat_content)
            self.chat_text_edit.verticalScrollBar().setValue(self.chat_text_edit.verticalScrollBar().maximum())

# Home Section
class HomeSection(QWidget):
    def __init__(self, stacked_widget):
        super().__init__()
        layout = QVBoxLayout()
        self.chat_button = QPushButton("Open Chat")
        self.chat_button.clicked.connect(lambda: stacked_widget.setCurrentIndex(1))
        layout.addWidget(self.chat_button)
        self.setLayout(layout)

# Main Application
class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI Assistant")
        layout = QVBoxLayout()

        self.stacked_widget = QStackedWidget()
        self.home_section = HomeSection(self.stacked_widget)
        self.chat_section = ChatSection()
        
        self.stacked_widget.addWidget(self.home_section)
        self.stacked_widget.addWidget(self.chat_section)
        layout.addWidget(self.stacked_widget)
        self.setLayout(layout)
        self.stacked_widget.setCurrentIndex(0)  # Default to home

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
