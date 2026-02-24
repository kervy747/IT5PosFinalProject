import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QStackedWidget
from PyQt6.QtGui import QPalette, QColor
from Controller import POSController
from Model.data_model import DataModel
from View.loginView import LoginView
from View.posView.mainPosView import mainPosView
from View.adminTabbedView import AdminTabbedView
from View.colors import BACKGROUND

if __name__ == "__main__":
    app = QApplication(sys.argv)

    model = DataModel()

    main_window = QMainWindow()
    main_window.setWindowTitle("POS System")
    main_window.setGeometry(100, 100, 1200, 700)

    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor(BACKGROUND))
    main_window.setPalette(palette)

    stack = QStackedWidget()
    main_window.setCentralWidget(stack)

    login_view = LoginView()
    pos_view = mainPosView()
    admin_tabbed_view = AdminTabbedView(model)

    controller = POSController(model, login_view, pos_view, admin_tabbed_view, main_window, stack)

    main_window.showMaximized()
    controller.run()
    sys.exit(app.exec())