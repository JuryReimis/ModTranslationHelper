import json
import math
import os
import webbrowser

from PyQt5 import QtWidgets, QtGui, QtCore

import sys
from pathlib import Path

from PyQt5.QtCore import pyqtSlot
from loguru import logger

from CustomDialog import Ui_Dialog
from languages.language_constants import LanguageConstants
from main import Prepper, Performer, Settings
from MainWindow import Ui_MainWindow
from SettingsWindow import Ui_Settings
import ctypes

BASE_DIR = Path.cwd()
TRANSLATIONS_DIR = BASE_DIR / 'languages'
HOME_DIR = Path.home()

PROGRAM_VERSION = '1.3.0_beta'

if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        logger.add(sink='logs/debug.log', rotation='10 MB', compression="zip")

        super(MainWindow, self).__init__(parent=parent)
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
        self.__init_settings()
        self.__init_app_position()
        self.__init_languages()
        self.__init_menubar()
        self.__init_languages_dict()
        self.setWindowIcon(QtGui.QIcon('icons/main icon.jpg'))
        self.__running_thread = None

        self.__ui.run_pushButton.setEnabled(False)

        for language in self.__languages_dict.get(self.__settings.get_translator_api()).keys():
            self.__ui.selector_original_language_comboBox.addItem(language)
            self.__ui.selector_target_language_comboBox.addItem(language)
        self.__ui.selector_original_language_comboBox.setCurrentText('english')
        self.__ui.selector_target_language_comboBox.setCurrentText('russian')

        self.__ui.game_directory_pushButton.clicked.connect(self.__select_game_directory)
        self.__ui.game_directory_open_pushButton.clicked.connect(self.__open_game_directory)
        self.__ui.original_directory_pushButton.clicked.connect(self.__select_original_directory)
        self.__ui.original_directory_open_pushButton.clicked.connect(self.__open_original_directory)
        self.__ui.previous_directory_pushButton.clicked.connect(self.__select_previous_directory)
        self.__ui.previous_directory_open_pushButton.clicked.connect(self.__open_previous_directory)
        self.__ui.target_directory_pushButton.clicked.connect(self.__select_target_directory)
        self.__ui.target_directory_open_pushButton.clicked.connect(self.__open_target_directory)
        self.__ui.need_translation_checkBox.stateChanged.connect(self.__need_translate_changed)
        self.__ui.check_all_pushButton.clicked.connect(self.__check_all_checkboxes)
        self.__ui.uncheck_all_pushButton.clicked.connect(self.__unchecked_all_checkboxes)
        self.__ui.run_pushButton.clicked.connect(self.__run)
        self.__ui.discord_link_pushButton.clicked.connect(self.__discord_clicked)
        self.__ui.donate_pushButton.clicked.connect(self.__donate_clicked)
        self.__ui.game_directory_lineEdit.editingFinished.connect(self.__game_directory_changed)
        self.__ui.original_directory_lineEdit.editingFinished.connect(self.__original_directory_changed)
        self.__ui.previous_directory_lineEdit.editingFinished.connect(self.__previous_directory_changed)
        self.__ui.target_directory_lineEdit.editingFinished.connect(self.__target_directory_changed)
        self.__ui.selector_original_language_comboBox.currentTextChanged.connect(self.__original_language_changed)
        self.__ui.program_language_comboBox.currentTextChanged.connect(self.__change_language)

        self.__ui.disable_original_line_checkBox.stateChanged.connect(self.__show_warning)

        self.__prepper = Prepper()
        self.__performer: Performer | None = None

        self.__preset_values()
        self.__check_readiness()

    @logger.catch()
    def __init_languages(self):
        self.__translators = []
        languages_list = ['Русский']
        for directory in TRANSLATIONS_DIR.iterdir():
            if directory.is_dir() and directory.name != "__pycache__":
                languages_list.append(directory.name)
        self.__ui.program_language_comboBox.addItems(languages_list)
        self.__ui.program_language_comboBox.setCurrentText(self.__settings.get_app_language())
        self.__change_language()

    @logger.catch()
    def __init_settings(self):
        if (HOME_DIR / 'Documents').exists():
            local_data_path = (HOME_DIR / 'Documents' / 'ModTranslationHelper')
            self.__settings = Settings(local_data_path)
        else:
            logger.warning(f'{HOME_DIR} / Documents - not exists')
            local_data_path = BASE_DIR / 'Settings'
            self.__settings = Settings(local_data_path)
            self.__init_languages()
            error = CustomDialog(parent=self.__ui.centralwidget, text=LanguageConstants.error_settings_file_not_exist)
            error.show()

    @logger.catch()
    def __init_app_position(self):
        position = self.__settings.get_app_position()
        self.move(*position)
        size = self.__settings.get_app_size()
        ResizeWindow(self, QtCore.QSize(*size)).resize_window()

    @logger.catch()
    def __init_menubar(self):
        def open_settings():
            settings = SettingsWindow(parent=self, settings=self.__settings)
            settings.exec_()
            self.__ui.program_language_comboBox.setCurrentText(self.__settings.get_app_language())
            self.__change_language()

        menu = QtWidgets.QMenuBar()
        main_menu = QtWidgets.QMenu(LanguageConstants.menu, self)
        open_settings_action = QtWidgets.QAction(LanguageConstants.settings, self)
        open_settings_action.triggered.connect(open_settings)
        main_menu.addAction(open_settings_action)

        menu.addMenu(main_menu)

        self.setMenuBar(menu)

    @logger.catch()
    def __init_languages_dict(self):
        with (BASE_DIR / 'language_names.json').open(mode='r') as language_dict:
            self.__languages_dict = json.load(language_dict)

    @logger.catch()
    def __preset_values(self):
        last_game_path = self.__settings.get_last_game_directory()
        last_original_path = self.__settings.get_last_original_mode_directory()
        last_previous_path = self.__settings.get_last_previous_directory()
        last_target_path = self.__settings.get_last_target_directory()

        last_original_language = self.__settings.get_last_original_language()
        last_target_language = self.__settings.get_last_target_language()

        self.__ui.game_directory_lineEdit.setText(last_game_path)
        self.__ui.original_directory_lineEdit.setText(last_original_path)
        self.__ui.previous_directory_lineEdit.setText(last_previous_path)
        self.__ui.target_directory_lineEdit.setText(last_target_path)

        self.__ui.selector_original_language_comboBox.setCurrentText(last_original_language)
        self.__ui.selector_target_language_comboBox.setCurrentText(last_target_language)

        self.__game_directory_changed()
        self.__original_directory_changed()
        self.__previous_directory_changed()
        self.__target_directory_changed()

    def __change_language(self):
        def set_translators():
            for _translator in self.__translators:
                app.installTranslator(_translator)

        def del_translators():
            for _translator in self.__translators:
                app.removeTranslator(_translator)

        del_translators()
        self.__settings.set_app_language(self.__ui.program_language_comboBox.currentText())

        self.__translators.clear()
        if self.__ui.program_language_comboBox.currentText() != 'Русский':
            current_language = self.__ui.program_language_comboBox.currentText()
            translation_files = [TRANSLATIONS_DIR / current_language / file for file in
                                 (TRANSLATIONS_DIR / current_language).iterdir() if
                                 (TRANSLATIONS_DIR / current_language).exists() and file.is_file()]

            for file in translation_files:
                translator = QtCore.QTranslator()
                translator.load(str(file))
                self.__translators.append(translator)
            set_translators()
        self.__ui.retranslateUi(self)
        LanguageConstants.retranslate()
        self.__ui.program_version_label.setText(f'{LanguageConstants.program_version} {PROGRAM_VERSION}')
        self.__init_menubar()

    def __select_game_directory(self):
        chosen_path = QtWidgets.QFileDialog.getExistingDirectory(caption='Get Path',
                                                                 directory=self.__settings.get_last_game_directory())
        self.__ui.game_directory_lineEdit.setText(chosen_path)
        self.__game_directory_changed()

    def __game_directory_changed(self):
        self.__prepper.set_game_path(self.__ui.game_directory_lineEdit.text())
        if not self.__prepper.get_game_path_validate_result():
            self.__ui.game_directory_lineEdit.clear()
            if str(self.__prepper.get_game_path()) != '.':
                error = CustomDialog(parent=self.__ui.centralwidget,
                                     text=f'{self.__prepper.get_game_path()} '
                                          f'- {LanguageConstants.error_folder_does_not_exist}')
                error.show()
        else:
            self.__settings.set_last_game_directory(self.__prepper.get_game_path())
        self.__check_readiness()

    def __open_game_directory(self):
        if self.__prepper.get_game_path_validate_result():
            os.startfile(self.__prepper.get_game_path())
        else:
            error = CustomDialog(parent=self, text=self.__prepper.get_game_path())
            error.show_path_error()

    def __select_original_directory(self):
        chosen_path = QtWidgets.QFileDialog.getExistingDirectory(caption='Get Path',
                                                                 directory=self.__settings.get_last_original_mode_directory())
        self.__ui.original_directory_lineEdit.setText(chosen_path)
        self.__original_directory_changed()

    def __original_directory_changed(self):
        self.__prepper.set_original_mode_path(
            original_mode_path=self.__ui.original_directory_lineEdit.text(),
            original_language=self.__languages_dict['GoogleTranslator'].get(
                self.__ui.selector_original_language_comboBox.currentText(), None)
        )
        if not self.__prepper.get_original_mode_path_validate_result():
            if str(self.__prepper.get_original_mode_path()) != '.':
                error = CustomDialog(parent=self.__ui.centralwidget,
                                     text=f'{self.__prepper.get_original_mode_path() / self.__ui.selector_original_language_comboBox.currentText()} -'
                                          f' {LanguageConstants.error_folder_does_not_exist}')
                error.show()
            self.__ui.original_directory_lineEdit.clear()
        else:
            self.__form_checkbox_cascade()
            self.__settings.set_last_original_mode_directory(self.__prepper.get_original_mode_path())
        self.__check_readiness()

    def __open_original_directory(self):
        if self.__prepper.get_original_mode_path_validate_result():
            os.startfile(self.__prepper.get_original_mode_path())
        else:
            error = CustomDialog(parent=self, text=self.__prepper.get_original_mode_path())
            error.show_path_error()

    def __select_previous_directory(self):
        chosen_path = QtWidgets.QFileDialog.getExistingDirectory(caption='Get Path',
                                                                 directory=self.__settings.get_last_previous_directory())
        self.__ui.previous_directory_lineEdit.setText(chosen_path)
        self.__previous_directory_changed()

    def __previous_directory_changed(self):
        self.__prepper.set_previous_path(previous_path=self.__ui.previous_directory_lineEdit.text(),
                                         target_language=self.__ui.selector_target_language_comboBox.currentText())
        if not self.__prepper.get_previous_path_validate_result():
            self.__ui.previous_directory_lineEdit.clear()
            if str(self.__prepper.get_previous_path()) != '.':
                error = CustomDialog(parent=self.__ui.centralwidget,
                                     text=f'{self.__prepper.get_previous_path() / self.__ui.selector_target_language_comboBox.currentText()} - '
                                          f'{LanguageConstants.error_folder_does_not_exist}')
                error.show()
            else:
                self.__settings.set_last_previous_directory(Path(''))
        else:
            self.__settings.set_last_previous_directory(self.__prepper.get_previous_path())

    def __open_previous_directory(self):
        if self.__prepper.get_previous_path_validate_result():
            os.startfile(self.__prepper.get_previous_path())
        else:
            error = CustomDialog(parent=self, text=self.__prepper.get_previous_path())
            error.show_path_error()

    def __select_target_directory(self):
        chosen_path = QtWidgets.QFileDialog.getExistingDirectory(caption='Get Path',
                                                                 directory=self.__settings.get_last_target_directory())
        self.__ui.target_directory_lineEdit.setText(chosen_path)
        self.__target_directory_changed()

    def __target_directory_changed(self):
        self.__prepper.set_target_path(self.__ui.target_directory_lineEdit.text())
        if not self.__prepper.get_target_path_validate_result():
            if str(self.__prepper.get_target_path()) != '.':
                error = CustomDialog(parent=self.__ui.centralwidget,
                                     text=f'{LanguageConstants.error_drive_not_exist}')
                error.show()
            self.__ui.target_directory_lineEdit.clear()
        else:
            self.__settings.set_last_target_directory(self.__prepper.get_target_path())
        self.__check_readiness()

    def __open_target_directory(self):
        if self.__prepper.get_target_path_validate_result() and self.__prepper.get_target_path().exists():
            os.startfile(self.__prepper.get_target_path())
        else:
            error = CustomDialog(parent=self, text=self.__prepper.get_target_path())
            error.show_path_error()

    def __original_language_changed(self):
        if self.__ui.original_directory_lineEdit.text():
            self.__original_directory_changed()

    def __need_translate_changed(self):
        if self.__ui.need_translation_checkBox.isChecked():
            self.__ui.need_translate_scrollArea.setEnabled(True)
        else:
            self.__ui.need_translate_scrollArea.setEnabled(False)

    @logger.catch()
    def __check_readiness(self):
        if self.__prepper.get_original_mode_path_validate_result() and self.__prepper.get_game_path_validate_result() \
                and self.__prepper.get_target_path_validate_result():
            self.__ui.run_pushButton.setEnabled(True)
        else:
            self.__ui.run_pushButton.setEnabled(False)

    @logger.catch()
    def __form_checkbox_cascade(self):
        files = self.__prepper.get_file_hierarchy()
        vertical_layout_widget = QtWidgets.QWidget()
        vertical_layout = QtWidgets.QVBoxLayout(vertical_layout_widget)
        for file_name in files:
            file_name: Path
            check_box = QtWidgets.QCheckBox(str(file_name))
            check_box.setObjectName(str(file_name))
            check_box.setChecked(True)
            vertical_layout.addWidget(check_box)
        vertical_layout_widget.setLayout(vertical_layout)
        self.__ui.need_translate_scrollArea.setWidget(vertical_layout_widget)

    def __show_warning(self):
        if self.__ui.disable_original_line_checkBox.isChecked():
            window = CustomDialog(parent=self, text=LanguageConstants.warning_disable_original_line,
                                  custom_title=LanguageConstants.warning_disable_original_line_title)
            window.exec_()

    def __check_all_checkboxes(self):
        for checkbox in self.__ui.need_translate_scrollArea.widget().children():
            if isinstance(checkbox, QtWidgets.QCheckBox):
                checkbox.setChecked(True)

    def __unchecked_all_checkboxes(self):
        for checkbox in self.__ui.need_translate_scrollArea.widget().children():
            if isinstance(checkbox, QtWidgets.QCheckBox):
                checkbox.setChecked(False)

    @logger.catch()
    def __get_all_checkboxes(self) -> tuple:
        r"""Возвращает кортеж из путей(Path()), отмеченных в ScrollArea"""
        enabled = []
        for checkbox in self.__ui.need_translate_scrollArea.widget().children():
            if isinstance(checkbox, QtWidgets.QCheckBox) and checkbox.isChecked():
                enabled.append(Path(checkbox.objectName()))
        return tuple(enabled)

    @staticmethod
    def __discord_clicked():
        webbrowser.open('https://discord.gg/zcAbHfUSCt')

    @staticmethod
    def __donate_clicked():
        webbrowser.open('https://boosty.to/reimis')

    @pyqtSlot(str)
    def add_text_in_console(self, text: str):
        self.__ui.console_textBrowser.append(text)

    @pyqtSlot(str)
    def set_info_label_new_value(self, info: str):
        self.__ui.info_label.setText(info)

    @pyqtSlot(float)
    def set_progressbar_new_value(self, progress: float):
        value = self.__ui.progressBar.value() + progress * self.__ui.progressBar.maximum()
        if value > self.__ui.progressBar.maximum():
            self.__ui.progressBar.setValue(self.__ui.progressBar.maximum())
        else:
            self.__ui.progressBar.setValue(math.ceil(value))

    @pyqtSlot()
    def stop_thread(self):
        self.__ui.run_pushButton.setEnabled(True)
        self.__running_thread.exec_()

    # Events:

    def keyPressEvent(self, button: QtGui.QKeyEvent) -> None:
        if button.key() == QtCore.Qt.Key_R:
            self.__ui.run_pushButton.click()
        else:
            super(MainWindow, self).keyPressEvent(button)

    def resizeEvent(self, resize_event: QtGui.QResizeEvent) -> None:
        ResizeWindow(self, resize_event.size())
        new_size = resize_event.size()
        self.__settings.set_app_size(new_size.width(), new_size.height())
        super(MainWindow, self).resizeEvent(resize_event)

    def moveEvent(self, a0: QtGui.QMoveEvent) -> None:
        new_position = a0.pos()
        self.__settings.set_app_position(new_position.x(), new_position.y())
        super(MainWindow, self).moveEvent(a0)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        self.__settings.save_settings_data()
        super(MainWindow, self).closeEvent(a0)

    ###

    def __run(self):
        self.__ui.run_pushButton.setEnabled(False)
        self.__settings.set_last_languages(original=self.__ui.selector_original_language_comboBox.currentText(),
                                           target=self.__ui.selector_target_language_comboBox.currentText())
        self.__settings.save_settings_data()
        self.__ui.progressBar.setValue(0)
        self.__performer = Performer(
            paths=self.__prepper,
            original_language=self.__ui.selector_original_language_comboBox.currentText(),
            target_language=self.__ui.selector_target_language_comboBox.currentText(),
            languages_dict=self.__languages_dict.get(self.__settings.get_translator_api()),
            need_translate=self.__ui.need_translation_checkBox.isChecked(),
            need_translate_tuple=self.__get_all_checkboxes(),
            disable_original_line=self.__ui.disable_original_line_checkBox.isChecked(),
        )

        self.__running_thread = QtCore.QThread()

        self.__performer.moveToThread(self.__running_thread)

        # Коннекты сигналов и слотов для межпоточной передачи информации
        self.__performer.info_console_value.connect(self.add_text_in_console)
        self.__performer.info_label_value.connect(self.set_info_label_new_value)
        self.__performer.progress_bar_value.connect(self.set_progressbar_new_value)
        self.__performer.finish_thread.connect(self.stop_thread)

        self.__running_thread.started.connect(self.__performer.run)

        self.__running_thread.start()


class ResizeWindow:
    default_font_sizes = {
        QtWidgets.QPushButton: 8,
        QtWidgets.QCheckBox: 10,
        QtWidgets.QProgressBar: 10,
        QtWidgets.QLabel: 10,
        QtWidgets.QTextBrowser: 8,
        QtWidgets.QLineEdit: 10,
        QtWidgets.QComboBox: 8,
    }

    special_font_sizes = {
        'discord_link_pushButton': 14,
        'donate_pushButton': 14,
        'game_directory_info_label': 8,
        'change_program_language_label': 14,
        'need_translation_info_label': 8,
        'need_translation_info_label_2': 8,
        'original_directory_info_label': 8,
        'previous_directory_info_label': 8,
        'program_version_label': 12,
        'target_directory_info_label': 8,

    }

    # RATES:

    EXTRA_SMALL = -4.5
    VERY_SMALL = -3
    SMALL = -1.5
    NORMAL = 0
    BIG = 1.5
    VERY_BIG = 3

    def __init__(self, main_window: MainWindow, size: QtCore.QSize):
        self.main_window = main_window
        self.new_width = size.width()
        self.new_height = size.height()

        self.scale_factor = ctypes.windll.shcore.GetScaleFactorForDevice(0) / 100

        self._validate_screen_size()

        if self.new_width >= 1900 * self.scale_factor:
            self.change_font(self.VERY_BIG)
        elif self.new_width > 1700 * self.scale_factor:
            self.change_font(self.BIG)
        elif self.new_width >= 1500 * self.scale_factor:
            self.change_font(self.NORMAL)
        elif self.new_width >= 1300 * self.scale_factor:
            self.change_font(self.SMALL)
        elif self.new_width >= 1000 * self.scale_factor:
            self.change_font(self.VERY_SMALL)
        else:
            self.change_font(self.EXTRA_SMALL)

    def _validate_screen_size(self):
        if self.new_width > SCREEN_SIZE.width() or self.new_height > SCREEN_SIZE.height():
            if self.new_width > SCREEN_SIZE.width():
                self.new_width = SCREEN_SIZE.width() * 0.7
            if self.new_height > SCREEN_SIZE.height():
                self.new_height = SCREEN_SIZE.height() * 0.7
            self.main_window.move(0, 0)
            self.main_window.resize(int(self.new_width), int(self.new_height))

    def change_font(self, rate):

        for name, size in self.default_font_sizes.items():
            for widget in self.main_window.findChildren(name):
                widget: QtWidgets.QWidget
                special_size = self.special_font_sizes.get(widget.objectName())
                if special_size:
                    font = widget.font()
                    font.setPointSizeF(special_size + rate)
                    widget.setFont(font)
                else:
                    font = widget.font()
                    font.setPointSizeF(size + rate)
                    widget.setFont(font)

    def resize_window(self):
        if self.new_width and self.new_height:
            self.main_window.resize(int(self.new_width), int(self.new_height))


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


class CustomDialog(QtWidgets.QDialog):

    @logger.catch()
    def __init__(self, parent=None, text=None, custom_title=None):
        super(CustomDialog, self).__init__(parent)
        self.__ui = Ui_Dialog()
        self.__ui.setupUi(self)
        self.__text = text
        if custom_title:
            self.setWindowTitle(custom_title)
        self.setWindowIcon(QtGui.QIcon('icons/error icon.jpg'))

        self.__ui.no_path_error_textBrowser.setText(text)

    @logger.catch()
    def show_path_error(self):
        error_text = f'{LanguageConstants.error_path_not_exists}: {self.__text}'
        self.__ui.no_path_error_textBrowser.setText(error_text)
        self.exec_()


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    SCREEN_SIZE = app.primaryScreen().size()
    application = MainWindow()
    application.show()

    sys.exit(app.exec_())
