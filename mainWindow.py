import sys
from PyQt6.QtWidgets import QApplication
from Controller import POSController
from Model.data_model import DataModel
from View.loginView import LoginView
from View.posView.mainPosView import mainPosView

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Create Model
    model = DataModel()

    # Create Views
    login_view = LoginView()
    pos_view = mainPosView()

    # Create Controller
    controller = POSController(model, login_view, pos_view)

    # Run application
    controller.run()
    sys.exit(app.exec())