from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QLineEdit, QApplication
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPixmap
from View.colors import *
from View.components import *


class LoginView(QWidget):
    login_signal = pyqtSignal(str, str)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setLayout(main_layout)

        # White box container
        white_box = CardFrame()
        white_box.setFixedWidth(400)

        layout = QVBoxLayout(white_box)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(15)

        # Logo
        logo_label = QLabel()
        pixmap = QPixmap(r"C:\Users\kervy\Documents\Coding\T360Project\View\icons\T360logo.png")
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(100, 100, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)

        # Title
        title = QLabel("Terminal 360")
        title.setFont(QFont("Poppins", 22, QFont.Weight.Bold))
        title.setStyleSheet(f"color: {PRIMARY};")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)
        layout.addSpacing(10)

        # Username
        layout.addWidget(FieldLabel("Username"))
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter username")
        self.username_input.setFixedHeight(45)
        self.username_input.setStyleSheet(f"""
            QLineEdit {{
                padding: 10px 15px;
                border: 2px solid {ACCENT};
                border-radius: 8px;
                font-size: 13px;
                font-family: Poppins;
                color: black;
                background-color: {BACKGROUND};
            }}
            QLineEdit:focus {{
                border: 2px solid {PRIMARY};
            }}
        """)
        layout.addWidget(self.username_input)

        layout.addSpacing(5)

        # Password
        layout.addWidget(FieldLabel("Password"))
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setFixedHeight(45)
        self.password_input.setStyleSheet(f"""
            QLineEdit {{
                padding: 10px 15px;
                border: 2px solid {ACCENT};
                border-radius: 8px;
                font-size: 13px;
                font-family: Poppins;
                color: black;
                background-color: {BACKGROUND};
            }}
            QLineEdit:focus {{
                border: 2px solid {PRIMARY};
            }}
        """)
        layout.addWidget(self.password_input)

        layout.addSpacing(15)

        # Login button
        login_btn = PrimaryButton("Login")
        login_btn.setFixedHeight(45)
        login_btn.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY};
                color: white;
                padding: 12px;
                border-radius: 8px;
                font-size: 15px;
                font-weight: bold;
                font-family: Poppins;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #005662;
            }}
            QPushButton:pressed {{
                background-color: #004450;
            }}
        """)
        login_btn.clicked.connect(self.on_login)
        layout.addWidget(login_btn)

        main_layout.addWidget(white_box)

    def showEvent(self, event):
        """Center window on first show"""
        super().showEvent(event)
        if not event.spontaneous():
            self.center_on_screen()

    def center_on_screen(self):
        """Center the window on the screen"""
        # Get the parent window (the actual main window, not just this widget)
        window = self.window()
        screen = window.screen().availableGeometry()
        window_geometry = window.frameGeometry()
        center_point = screen.center()
        window_geometry.moveCenter(center_point)
        window.move(window_geometry.topLeft())

    def on_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        self.login_signal.emit(username, password)

    def clear_fields(self):
        self.username_input.clear()
        self.password_input.clear()