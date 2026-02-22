import os
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QColor, QPixmap, QIcon, QAction
from View.components import *

class UserManagementTab(QWidget):
    add_user_signal = pyqtSignal(str, str, str)
    delete_user_signal = pyqtSignal(str)
    reactivate_user_signal = pyqtSignal(str)
    search_users_signal = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(25, 25, 25, 25)
        main_layout.setSpacing(20)

        user_frame = CardFrame()
        user_layout = QVBoxLayout(user_frame)
        user_layout.setContentsMargins(20, 25, 20, 25)
        user_layout.setSpacing(15)

        user_layout.addWidget(SectionLabel("Add New User"))
        user_layout.addWidget(SubtitleLabel("Create a new user account"))

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

        view_frame = CardFrame()
        view_layout = QVBoxLayout(view_frame)
        view_layout.setContentsMargins(25, 25, 25, 25)
        view_layout.setSpacing(15)

        header_layout = QHBoxLayout()
        header_layout.setSpacing(16)

        logo_label = QLabel()
        icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "Assets", "userLogo.svg")
        pixmap = QPixmap(icon_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(35, 35, Qt.AspectRatioMode.KeepAspectRatio,
                                          Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
        header_layout.addWidget(logo_label)

        header_layout.addWidget(SectionLabel("Manage Users", 18))

        header_layout.addStretch()
        view_layout.addLayout(header_layout)

        self.search_input = SearchInput("Search users by username...")

        search_icon_path = os.path.join(os.path.dirname(__file__), "..", "..", "Assets", "searchIcon.svg")
        search_icon = QIcon(search_icon_path)
        search_action = QAction(search_icon, "", self.search_input)
        self.search_input.addAction(search_action, QLineEdit.ActionPosition.LeadingPosition)

        self.search_input.textChanged.connect(
            lambda: self.search_users_signal.emit(self.search_input.text()))
        view_layout.addWidget(self.search_input)

        self.users_table = StyledTable(3, ["Username", "Role", "Actions"])
        self.users_table.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        view_layout.addWidget(self.users_table)

        main_layout.addWidget(user_frame, 25)
        main_layout.addWidget(view_frame, 75)

    def show_error(self, title, message):
        QMessageBox.warning(self, title, message)

    def show_info(self, title, message):
        QMessageBox.information(self, title, message)

    def show_question(self, title, message):
        reply = QMessageBox.question(
            self,
            title,
            message,
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        return reply == QMessageBox.StandardButton.Yes

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

    def update_users_table(self, users, current_username=None):
        self.users_table.setRowCount(len(users))
        for i, user in enumerate(users):
            is_current_user = (current_username and user.username == current_username)
            is_inactive = (user.active == 0)

            if is_current_user:
                display_name = f"{user.username} (You)"
            elif is_inactive:
                display_name = f"{user.username} (Inactive)"
            else:
                display_name = user.username

            username_item = QTableWidgetItem(display_name)

            if is_inactive:
                username_item.setForeground(QColor("#999999"))
            elif is_current_user:
                username_item.setForeground(QColor("#006D77"))
            else:
                username_item.setForeground(QColor("#2c3e50"))

            username_item.setFont(QFont("Poppins", 10,
                                        QFont.Weight.Bold if is_current_user else QFont.Weight.Medium))
            self.users_table.setItem(i, 0, username_item)

            role_item = QTableWidgetItem(user.role.upper())
            if is_inactive:
                role_item.setForeground(QColor("#999999"))
            elif user.role == "admin":
                role_item.setForeground(QColor("#006D77"))
            else:
                role_item.setForeground(QColor("#6c757d"))
            role_item.setFont(QFont("Poppins", 9, QFont.Weight.Bold))
            role_item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)
            self.users_table.setItem(i, 1, role_item)

            btn_container = QWidget()
            btn_layout = QHBoxLayout(btn_container)
            btn_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
            btn_layout.setContentsMargins(5, 5, 5, 5)

            if is_current_user:
                disabled_btn = QPushButton("You")
                disabled_btn.setEnabled(False)
                disabled_btn.setMinimumHeight(40)
                disabled_btn.setMinimumWidth(120)
                disabled_btn.setStyleSheet("""
                    QPushButton {
                        background-color: #D0D0D0;
                        color: #888888;
                        padding: 1px 1px;
                        border-radius: 6px;
                        font-family: Poppins;
                        font-size: 9pt;
                        font-weight: bold;
                        border: none;
                    }
                """)
                btn_layout.addWidget(disabled_btn)
            elif is_inactive:
                reactivate_btn = ReactivateButton()
                reactivate_btn.clicked.connect(
                    lambda checked, u=user.username: self.reactivate_user_signal.emit(u))
                btn_layout.addWidget(reactivate_btn)
            else:
                delete_btn = DeleteButton("Deactivate")
                delete_btn.clicked.connect(
                    lambda checked, u=user.username: self.delete_user_signal.emit(u))
                btn_layout.addWidget(delete_btn)

            self.users_table.setCellWidget(i, 2, btn_container)

        self.users_table.setColumnWidth(1, 120)
        self.users_table.setColumnWidth(2, 140)