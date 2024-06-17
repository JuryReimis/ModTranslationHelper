from PyQt5 import QtWidgets
from loguru import logger

from gui.add_account_data_window import AddAccountDataWindow
from main import Settings, TranslatorAccount
from translators.translator_manager import TranslatorManager
from gui.window_ui.SettingsWindow import Ui_Settings


class SettingsWindow(QtWidgets.QDialog):
    @logger.catch()
    def __init__(self, parent=None, settings: Settings = None, account_data: TranslatorAccount = None):
        super(SettingsWindow, self).__init__(parent)
        self.__ui = Ui_Settings()
        self.__ui.setupUi(self)

        self.__settings = settings
        self.__account_data = account_data
        self.__set_initial_values()

        self.__ui.apis_comboBox.currentTextChanged.connect(self.__change_current_api)
        self.__ui.save_settings_pushButton.clicked.connect(self.save_settings)

    @logger.catch()
    def __set_initial_values(self):
        self.__ui.apis_comboBox.addItems(TranslatorManager.supported_apis)
        selected_api = self.__settings.get_translator_api()
        self.__ui.apis_comboBox.setCurrentText(selected_api)
        if selected_api in ['GoogleTranslator', ]:
            self.set_protection_symbols_visible()

    @logger.catch()
    def __change_current_api(self, selected_api):
        self.__settings.set_translator_api(selected_api)
        match selected_api:
            case 'YandexTranslator' | 'DeepLTranslator':
                add_account_data = AddAccountDataWindow(parent=self,
                                                        title=f'{selected_api} Api Key',
                                                        api_name=selected_api,
                                                        account_data=self.__account_data)
                add_account_data.exec_()
                self.set_protection_symbols_visible()
            case _:
                self.set_protection_symbols_visible(True)
        self.parent().translator_api_changed()

    def set_protection_symbols_visible(self, visible: bool = False):
        self.__ui.protection_symbol_label.setVisible(visible)
        self.__ui.protection_symbol_lineEdit.setVisible(visible)

    def set_default(self):
        self.__ui.apis_comboBox.setCurrentText('GoogleTranslator')
        self.__settings.set_translator_api('GoogleTranslator')

    def save_settings(self):
        self.__settings.save_settings_data()
        self.close()
