from PyQt5 import QtWidgets
from loguru import logger

from gui.window_ui.CustomDialog import Ui_Dialog, QtGui
from languages.language_constants import LanguageConstants


class CustomDialog(QtWidgets.QDialog):

    @logger.catch()
    def __init__(self, parent=None, text=None, custom_title=None, icon_path: str = None):
        super(CustomDialog, self).__init__(parent)
        self.__ui = Ui_Dialog()
        self.__ui.setupUi(self)
        self.__text = text
        if custom_title:
            self.setWindowTitle(custom_title)
        self.setWindowIcon(QtGui.QIcon(icon_path))

        self.__ui.no_path_error_textBrowser.setText(text)

    @logger.catch()
    def show_path_error(self):
        error_text = f'{LanguageConstants.error_path_not_exists}: {self.__text}'
        self.__ui.no_path_error_textBrowser.setText(error_text)
        self.exec_()
