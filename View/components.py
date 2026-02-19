from PyQt6.QtWidgets import QPushButton, QLineEdit, QTableWidget, QHeaderView, QFrame, QLabel, QComboBox, QHBoxLayout, \
    QWidget, QLayout
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont
from View.colors import *

# ============= UTILITY FUNCTIONS =============

def remove_margins_spacing(layout_or_widget):
    if isinstance(layout_or_widget, QLayout):
        # Remove margins and spacing from the layout
        layout_or_widget.setContentsMargins(0, 0, 0, 0)
        layout_or_widget.setSpacing(0)

        # Process all items in the layout
        for i in range(layout_or_widget.count()):
            item = layout_or_widget.itemAt(i)
            if item.widget():
                remove_margins_spacing(item.widget())
            elif item.layout():
                remove_margins_spacing(item.layout())

    elif isinstance(layout_or_widget, QWidget):
        # Remove widget margins
        layout_or_widget.setContentsMargins(0, 0, 0, 0)

        # Process the widget's layout if it has one
        if layout_or_widget.layout():
            remove_margins_spacing(layout_or_widget.layout())


# ============= BUTTONS =============

class PrimaryButton(QPushButton):
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
                margin: 0px;
            }}
            QPushButton:hover {{
                background-color: #005662;
            }}
            QPushButton:pressed {{
                background-color: #004a54;
            }}
        """)

class DeleteButton(QPushButton):
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
                margin: 0px;
            }
            QPushButton:hover {
                background-color: #D62828;
            }
            QPushButton:pressed {
                background-color: #C11119;
            }
        """)

class ReactivateButton(QPushButton):
    def __init__(self, text="Reactivate"):
        super().__init__(text)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.setMinimumHeight(40)
        self.setMinimumWidth(120)
        self.setStyleSheet("""
            QPushButton {
                background-color: #28a745;
                color: white;
                padding: 1px 1px;
                border-radius: 6px;
                font-family: Poppins;
                font-size: 9pt;
                font-weight: bold;
                border: none;
                margin: 0px;
            }
            QPushButton:hover {
                background-color: #218838;
            }
            QPushButton:pressed {
                background-color: #1e7e34;
            }
        """)

class ViewButton(QPushButton):
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
                margin: 0px;
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
                margin: 0px;
            }
            QLineEdit:focus {
                border: 2px solid #006D77;
                background-color: white;
            }
        """)

class StyledComboBox(QComboBox):
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
                margin: 0px;
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
                margin: 0px;
            }
            QLineEdit:focus {
                border: 2px solid #006D77;
                background-color: white;
            }
        """)

# ============= TABLES =============

class StyledTable(QTableWidget):
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
                border: none;
                margin: 0px;
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
    def __init__(self):
        super().__init__()
        self.setStyleSheet("""
            QFrame {
                background-color: white;
                border-radius: 12px;
                border: 1px solid #E8F4F5;
                margin: 0px;
            }
        """)

class HeaderFrame(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{
                background-color: white;
                border-radius: 12px;
                padding: 15px 25px;
                border: 1px solid #E8F4F5;
                margin: 0px;
            }}
        """)

class TotalCard(QFrame):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {PRIMARY};
                border-radius: 10px;
                padding: 12px;
                border: none;
                margin: 0px;
            }}
        """)

class SectionLabel(QLabel):

    def __init__(self, text, size=16):
        super().__init__(text)
        self.setFont(QFont("Poppins", size, QFont.Weight.Bold))
        self.setStyleSheet(f"color: {PRIMARY}; margin: 0px; border: none;")


class SubtitleLabel(QLabel):

    def __init__(self, text):
        super().__init__(text)
        self.setFont(QFont("Poppins", 9))
        self.setStyleSheet("color: #6c757d; margin: 0px; border: none;")
        self.setWordWrap(True)


class FieldLabel(QLabel):

    def __init__(self, text):
        super().__init__(text)
        self.setFont(QFont("Poppins", 10, QFont.Weight.Medium))
        self.setStyleSheet("color: #2c3e50; margin: 0px; border: none;")

class MonthYearSelector(QFrame):
    month_changed = pyqtSignal(int, int)

    def __init__(self, start_year=2020):
        super().__init__()
        from datetime import datetime

        self.current_date = datetime.now()
        self.start_year = start_year

        self.months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]

        self.init_ui()
        self.set_current_date()

    def init_ui(self):
        self.setStyleSheet(f"""
            QFrame {{
                background-color: {WHITE};
                border-radius: 10px;
                border: 1px solid #E8F4F5;
                margin: 0px;
            }}
        """)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(12, 8, 12, 8)
        layout.setSpacing(12)

        icon_label = QLabel("📅")
        icon_label.setFont(QFont("Segoe UI Emoji", 16))
        icon_label.setStyleSheet("background: transparent; margin: 0px; border: none;")
        layout.addWidget(icon_label)

        self.month_combo = QComboBox()
        self.month_combo.addItems(self.months)
        self.month_combo.setFont(QFont("Poppins", 11, QFont.Weight.Medium))
        self.month_combo.setCursor(Qt.CursorShape.PointingHandCursor)
        self.month_combo.setMinimumWidth(130)
        self.month_combo.setStyleSheet(f"""
            QComboBox {{
                font-family: Poppins;
                font-size: 11pt;
                font-weight: 500;
                color: {PRIMARY};
                padding: 8px 12px;
                background-color: {BACKGROUND};
                border: 2px solid #E1E8ED;
                border-radius: 8px;
                margin: 0px;
            }}
            QComboBox:hover {{
                border: 2px solid {PRIMARY};
                background-color: white;
            }}
            QComboBox:focus {{
                border: 2px solid {PRIMARY};
                background-color: white;
            }}
            QComboBox::drop-down {{
                border: none;
                padding-right: 8px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid {PRIMARY};
                margin-right: 8px;
            }}
            QComboBox QAbstractItemView {{
                background-color: white;
                color: {PRIMARY};
                border: 2px solid {PRIMARY};
                border-radius: 8px;
                selection-background-color: #E8F4F5;
                selection-color: {PRIMARY};
                padding: 5px;
                font-family: Poppins;
                font-size: 11pt;
            }}
        """)
        self.month_combo.currentIndexChanged.connect(self.on_selection_changed)
        layout.addWidget(self.month_combo)

        self.year_combo = QComboBox()
        self.year_combo.addItem(str(self.current_date.year))
        self.year_combo.setFont(QFont("Poppins", 11, QFont.Weight.Medium))
        self.year_combo.setCursor(Qt.CursorShape.PointingHandCursor)
        self.year_combo.setMinimumWidth(90)
        self.year_combo.setStyleSheet(f"""
            QComboBox {{
                font-family: Poppins;
                font-size: 11pt;
                font-weight: 500;
                color: {PRIMARY};
                padding: 8px 12px;
                background-color: {BACKGROUND};
                border: 2px solid #E1E8ED;
                border-radius: 8px;
                margin: 0px;
            }}
            QComboBox:hover {{
                border: 2px solid {PRIMARY};
                background-color: white;
            }}
            QComboBox:focus {{
                border: 2px solid {PRIMARY};
                background-color: white;
            }}
            QComboBox::drop-down {{
                border: none;
                padding-right: 8px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid {PRIMARY};
                margin-right: 8px;
            }}
            QComboBox QAbstractItemView {{
                background-color: white;
                color: {PRIMARY};
                border: 2px solid {PRIMARY};
                border-radius: 8px;
                selection-background-color: #E8F4F5;
                selection-color: {PRIMARY};
                padding: 5px;
                font-family: Poppins;
                font-size: 11pt;
            }}
        """)
        self.year_combo.currentIndexChanged.connect(self.on_selection_changed)
        layout.addWidget(self.year_combo)

    def set_available_years(self, transactions):
        from datetime import datetime

        current_year = self.current_date.year
        years_with_data = set()

        for t in transactions:
            try:
                if hasattr(t, 'date') and t.date:
                    trans_date = datetime.strptime(t.date, "%m-%d-%Y %I:%M %p")
                    years_with_data.add(trans_date.year)
            except Exception:
                pass

        years_with_data.add(current_year)
        sorted_years = sorted(years_with_data)
        currently_selected = self.year_combo.currentText()

        self.year_combo.blockSignals(True)
        self.year_combo.clear()
        self.year_combo.addItems([str(y) for y in sorted_years])

        restore_index = self.year_combo.findText(currently_selected)
        if restore_index >= 0:
            self.year_combo.setCurrentIndex(restore_index)
        else:
            fallback = self.year_combo.findText(str(current_year))
            if fallback >= 0:
                self.year_combo.setCurrentIndex(fallback)

        self.year_combo.blockSignals(False)

    def on_selection_changed(self):
        selected_month = self.month_combo.currentIndex() + 1
        selected_year = int(self.year_combo.currentText())
        self.month_changed.emit(selected_month, selected_year)

    def set_current_date(self):
        current_month = self.current_date.month
        current_year = self.current_date.year

        self.month_combo.blockSignals(True)
        self.year_combo.blockSignals(True)

        self.month_combo.setCurrentIndex(current_month - 1)
        year_index = self.year_combo.findText(str(current_year))
        if year_index >= 0:
            self.year_combo.setCurrentIndex(year_index)

        self.month_combo.blockSignals(False)
        self.year_combo.blockSignals(False)

        self.month_changed.emit(current_month, current_year)

    def get_selected_month(self):
        month = self.month_combo.currentIndex() + 1
        year = int(self.year_combo.currentText())
        return month, year

    def set_month_year(self, month, year):
        self.month_combo.blockSignals(True)
        self.year_combo.blockSignals(True)

        if 1 <= month <= 12:
            self.month_combo.setCurrentIndex(month - 1)

        year_index = self.year_combo.findText(str(year))
        if year_index >= 0:
            self.year_combo.setCurrentIndex(year_index)

        self.month_combo.blockSignals(False)
        self.year_combo.blockSignals(False)

        self.month_changed.emit(month, year)