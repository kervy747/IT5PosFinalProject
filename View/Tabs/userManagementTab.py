from PyQt6.QtWidgets import *
from PyQt6.QtCore import pyqtSignal
from PyQt6.QtGui import QColor
from View.components import *


class UserManagementTab(QWidget):
    add_user_signal = pyqtSignal(str, str, str)
    delete_user_signal = pyqtSignal(str)
    search_users_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        # Left side
        user_frame = CardFrame()
        user_layout = QVBoxLayout(user_frame)
        user_layout.setContentsMargins(20, 25, 20, 25)
        user_layout.setSpacing(15)

        user_layout.addWidget(SectionLabel("Add New User"))
        user_layout.addWidget(SubtitleLabel("Create a new user account"))

        # Form fields
        user_layout.addWidget(FieldLabel("Username"))
        self.new_username = StyledInput("Enter username")
        user_layout.addWidget(self.new_username)

        user_layout.addWidget(FieldLabel("Password"))
        self.new_password = StyledInput("Enter password")
        self.new_password.setEchoMode(QLineEdit.EchoMode.Password)
        user_layout.addWidget(self.new_password)

        user_layout.addWidget(FieldLabel("Role"))
        self.new_role = StyledComboBox()
        self.new_role.addItems(["admin", "staff"])
        user_layout.addWidget(self.new_role)

        add_btn = PrimaryButton("Add User", "✓")
        add_btn.clicked.connect(self.on_add_user)
        user_layout.addWidget(add_btn)
        user_layout.addStretch()

        # Right side - Manage Users (75%)
        view_frame = CardFrame()
        view_layout = QVBoxLayout(view_frame)
        view_layout.setContentsMargins(25, 25, 25, 25)
        view_layout.setSpacing(15)

        view_layout.addWidget(SectionLabel("Manage Users", 18))

        self.search_input = SearchInput("🔍 Search users by username...")
        self.search_input.textChanged.connect(
            lambda: self.search_users_signal.emit(self.search_input.text()))
        view_layout.addWidget(self.search_input)

        self.users_table = StyledTable(3, ["Username", "Role", "Actions"])
        self.users_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        view_layout.addWidget(self.users_table)

        main_layout.addWidget(user_frame, 25)
        main_layout.addWidget(view_frame, 75)

    def on_add_user(self):
        username = self.new_username.text().strip()
        password = self.new_password.text()
        role = self.new_role.currentText()

        if username and password:
            self.add_user_signal.emit(username, password, role)
            self.new_username.clear()
            self.new_password.clear()
        else:
            QMessageBox.warning(self, "Invalid Input", "Please enter both username and password.")

    def update_users_table(self, users):
        """Update the users table display"""
        self.users_table.setRowCount(len(users))
        for i, user in enumerate(users):
            # Username
            username_item = QTableWidgetItem(user.username)
            username_item.setForeground(QColor("#2c3e50"))
            username_item.setFont(QFont("Poppins", 10, QFont.Weight.Medium))
            self.users_table.setItem(i, 0, username_item)

            # Role
            role_item = QTableWidgetItem(user.role.upper())
            if user.role == "admin":
                role_item.setForeground(QColor("#006D77"))
            else:
                role_item.setForeground(QColor("#6c757d"))
            role_item.setFont(QFont("Poppins", 9, QFont.Weight.Bold))
            role_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.users_table.setItem(i, 1, role_item)

            # Delete button
            delete_btn = DeleteButton()
            delete_btn.clicked.connect(lambda checked, u=user.username: self.delete_user_signal.emit(u))

            btn_container = QWidget()
            btn_layout = QHBoxLayout(btn_container)
            btn_layout.addWidget(delete_btn)
            btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            btn_layout.setContentsMargins(5, 5, 5, 5)
            self.users_table.setCellWidget(i, 2, btn_container)

        self.users_table.setColumnWidth(1, 120)
        self.users_table.setColumnWidth(2, 140)