from PyQt5 import QtWidgets
from loguru import logger

from gui.add_account_data_window import AddAccountDataWindow
from languages.language_constants import SettingsWindowConstants
from main import Settings, TranslatorAccount
from translators.translator_manager import TranslatorManager
from gui.window_ui.SettingsWindow import Ui_Settings
from utils.gui.info_utils import AddInfoIcons


class SettingsWindow(QtWidgets.QDialog):
    @logger.catch()
    def __init__(self, parent=None, settings: Settings = None, account_data: TranslatorAccount = None):
        super(SettingsWindow, self).__init__(parent)
        self.__ui = Ui_Settings()
        self.__ui.setupUi(self)

        self.__settings = settings
        self.__account_data = account_data
        self.__init_icons()
        self.__set_initial_values()

        self.__ui.apis_comboBox.currentTextChanged.connect(self.__change_current_api)
        self.__ui.save_settings_pushButton.clicked.connect(self.save_settings)
        self.__ui.protection_symbol_lineEdit.textChanged.connect(self.set_protection_symbol)

    def __init_info_layouts(self):
        self.__info_layouts = {
            self.__ui.protection_symbol_horizontalLayout: SettingsWindowConstants.protection_symbol_help,
        }

    def __init_icons(self):
        self.__init_info_layouts()
        AddInfoIcons(self.__info_layouts)

    @logger.catch()
    def __set_initial_values(self):
        self.__ui.apis_comboBox.addItems(TranslatorManager.supported_apis)
        selected_api = self.__settings.get_translator_api()
        self.__ui.apis_comboBox.setCurrentText(selected_api)
        self.__ui.protection_symbol_lineEdit.setText(self.__settings.get_protection_symbol())
        if selected_api in ['GoogleTranslator', ]:
            self.set_protection_symbols_enable(True)
        else:
            self.set_protection_symbols_enable()

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
                self.set_protection_symbols_enable()
            case _:
                self.set_protection_symbols_enable(True)

        self.parent().translator_api_changed()

    def set_protection_symbols_enable(self, enable: bool = False):
        self.__ui.protection_symbol_label.setEnabled(enable)
        self.__ui.protection_symbol_lineEdit.setEnabled(enable)

    def set_protection_symbol(self, symbol: str):
        self.__settings.set_protection_symbol(symbol)

    def set_default(self):
        self.__ui.apis_comboBox.setCurrentText('GoogleTranslator')
        self.__settings.set_translator_api('GoogleTranslator')

    def save_settings(self):
        self.__settings.save_settings_data()
        self.close()
