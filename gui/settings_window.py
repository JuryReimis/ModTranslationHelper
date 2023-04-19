from PyQt5 import QtWidgets
from loguru import logger

from main import Settings
from window_ui.SettingsWindow import Ui_Settings


class SettingsWindow(QtWidgets.QDialog):
    @logger.catch()
    def __init__(self, parent=None, settings: Settings = None):
        super(SettingsWindow, self).__init__(parent)
        self.__ui = Ui_Settings()
        self.__ui.setupUi(self)

        self.__settings = settings
        self.__set_initial_values()

        self.__ui.save_settings_pushButton.clicked.connect(self.save_settings)

    @logger.catch()
    def __set_initial_values(self):
        self.__ui.apis_comboBox.addItems(self.__settings.available_apis.keys())

    def save_settings(self):
        self.__settings.save_settings_data()
        self.close()
