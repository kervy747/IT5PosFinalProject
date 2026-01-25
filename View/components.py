from PyQt6.QtWidgets import QPushButton, QLineEdit, QTableWidget, QHeaderView, QFrame, QLabel, QComboBox
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QCursor
from View.colors import *


# ============= BUTTONS =============

class PrimaryButton(QPushButton):
    """Primary action button (teal)"""
    def __init__(self, text, icon=""):
        super().__init__(f"{icon} {text}" if icon else text)
        self.setFont(QFont("Poppins", 10, QFont.Weight.Bold))
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY};
                color: white;
                padding: 12px 20px;
                border-radius: 8px;
                font-family: Poppins;
                font-weight: bold;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #005662;
            }}
            QPushButton:pressed {{
                background-color: #004a54;
            }}
        """)


class DeleteButton(QPushButton):
    """Delete button (red)"""
    def __init__(self, text="Delete"):
        super().__init__(text)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(40)
        self.setMinimumWidth(120)
        self.setStyleSheet("""
            QPushButton {
                background-color: #E63946;
                color: white;
                padding: 1px 1px;
                border-radius: 6px;
                font-family: Poppins;
                font-size: 9pt;
                font-weight: bold;
                border: none;
            }
            QPushButton:hover {
                background-color: #D62828;
            }
            QPushButton:pressed {
                background-color: #C11119;
            }
        """)


class ViewButton(QPushButton):
    """View/Details button"""
    def __init__(self, text="View Details"):
        super().__init__(text)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(40)
        self.setMinimumWidth(120)
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {PRIMARY};
                color: white;
                padding: 10px 16px;
                border-radius: 6px;
                font-family: Poppins;
                font-size: 9pt;
                font-weight: bold;
                border: none;
            }}
            QPushButton:hover {{
                background-color: #005662;
            }}
            QPushButton:pressed {{
                background-color: #004a54;
            }}
        """)


# ============= INPUT FIELDS =============

class StyledInput(QLineEdit):
    """Styled input field"""
    def __init__(self, placeholder=""):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
            QLineEdit {
                font-family: Poppins; 
                font-size: 10pt;
                color: black; 
                padding: 10px 12px; 
                background-color: #F8FAFB; 
                border: 2px solid #E1E8ED; 
                border-radius: 8px;
            }
            QLineEdit:focus {
                border: 2px solid #006D77;
                background-color: white;
            }
        """)


class StyledComboBox(QComboBox):
    """Styled combo box / dropdown"""
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QComboBox {
                font-family: Poppins; 
                font-size: 10pt;
                color: black; 
                padding: 10px 12px; 
                background-color: #F8FAFB; 
                border: 2px solid #E1E8ED; 
                border-radius: 8px;
            }
            QComboBox:focus {
                border: 2px solid #006D77;
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
                padding-right: 10px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #006D77;
                margin-right: 8px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: black;
                border: 2px solid #006D77;
                border-radius: 8px;
                selection-background-color: #E8F4F5;
                selection-color: black;
                padding: 5px;
                font-family: Poppins;
            }
        """)


class SearchInput(QLineEdit):
    """Search input field with icon"""
    def __init__(self, placeholder="🔍 Search..."):
        super().__init__()
        self.setPlaceholderText(placeholder)
        self.setStyleSheet("""
            QLineEdit {
                font-family: Poppins; 
                font-size: 11pt;
                color: black; 
                padding: 12px 15px; 
                background-color: #F8FAFB; 
                border: 2px solid #E1E8ED; 
                border-radius: 8px;
            }
            QLineEdit:focus {
                border: 2px solid #006D77;
                background-color: white;
            }
        """)


# ============= TABLES =============

class StyledTable(QTableWidget):
    """Pre-styled table widget"""

    def __init__(self, columns, headers):
        super().__init__()
        self.setColumnCount(columns)
        self.setHorizontalHeaderLabels(headers)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.verticalHeader().setVisible(False)
        self.setAlternatingRowColors(True)
        self.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.setShowGrid(False)

        # Set default row height to accommodate the delete button
        self.verticalHeader().setDefaultSectionSize(60)

        self.setStyleSheet(f"""
            QTableWidget {{
                background-color: white;
                border-radius: 8px;
                color: #2c3e50;
                font-family: Poppins;
                font-size: 10pt;
                gridline-color: #E8F4F5;
            }}
            QTableWidget::item {{
                padding: 8px;
                border-bottom: 1px solid #F0F4F8;
                color: #2c3e50;
            }}
            QTableWidget::item:selected {{
                background-color: #83C5BE;
                color: #2c3e50;
            }}
            QTableWidget::item:hover {{
                background-color: #E8F4F5;
            }}
            QHeaderView::section {{
                background-color: {PRIMARY};
                color: white;
                font-family: Poppins;
                font-weight: bold;
                font-size: 11pt;
                padding: 12px 8px;
                border: none;
                border-right: 1px solid #005662;
            }}
            QHeaderView::section:last {{
                border-right: none;
            }}
            QTableWidget::item:alternate {{
                background-color: #F8FAFB;
            }}
        """)


# ============= CONTAINERS =============

class CardFrame(QFrame):
    """White card container"""
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E8F4F5;
            }
        """)


class HeaderFrame(QFrame):
    """Header container with white background"""
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 12px;
                padding: 15px 25px;
                border: 1px solid #E8F4F5;
            }}
        """)


class TotalCard(QFrame):
    """Total amount card for POS"""
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {PRIMARY};
                border-radius: 10px;
                padding: 12px;
            }}
        """)


class SectionLabel(QLabel):
    """Section title label"""
    def __init__(self, text, size=16):
        super().__init__(text)
        self.setFont(QFont("Poppins", size, QFont.Weight.Bold))
        self.setStyleSheet(f"color: {PRIMARY};")


class SubtitleLabel(QLabel):
    """Subtitle/description label"""
    def __init__(self, text):
        super().__init__(text)
        self.setFont(QFont("Poppins", 9))
        self.setStyleSheet("color: #6c757d;")
        self.setWordWrap(True)


class FieldLabel(QLabel):
    """Form field label"""
    def __init__(self, text):
        super().__init__(text)
        self.setFont(QFont("Poppins", 10, QFont.Weight.Medium))
        self.setStyleSheet("color: #2c3e50;")