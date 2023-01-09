import math
import webbrowser

from PyQt5 import QtWidgets, QtGui, QtCore

import sys
from pathlib import Path

from PyQt5.QtCore import pyqtSlot

from CustomDialog import Ui_Dialog
from languages.language_constants import LanguageConstants
from main import Prepper, Performer
from MainWindow import Ui_MainWindow
from deep_translator import GoogleTranslator

BASE_DIR = Path.cwd()
TRANSLATIONS_DIR = BASE_DIR / 'languages'


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.__ui = Ui_MainWindow()
        self.__ui.setupUi(self)
        self.__init_languages()
        MainWindow.setFixedSize(self, self.size())
        self.setWindowIcon(QtGui.QIcon('icons/main icon.jpg'))
        self.__running_thread = None

        self.__last_selected_directory = '/'
        self.__ui.run_pushButton.setEnabled(False)
        for language in GoogleTranslator.get_supported_languages():
            self.__ui.selector_original_language_comboBox.addItem(language)
            self.__ui.selector_target_language_comboBox.addItem(language)
        self.__ui.selector_original_language_comboBox.setCurrentText('english')
        self.__ui.selector_target_language_comboBox.setCurrentText('russian')

        self.__ui.game_directory_pushButton.clicked.connect(self.__select_game_directory)
        self.__ui.original_directory_pushButton.clicked.connect(self.__select_original_directory)
        self.__ui.previous_directory_pushButton.clicked.connect(self.__select_previous_directory)
        self.__ui.target_directory_pushButton.clicked.connect(self.__select_target_directory)
        self.__ui.need_translation_checkBox.stateChanged.connect(self.__need_translate_changed)
        self.__ui.check_all_pushButton.clicked.connect(self.__check_all_checkboxes)
        self.__ui.uncheck_all_pushButton.clicked.connect(self.__unchecked_all_checkboxes)
        self.__ui.run_pushButton.clicked.connect(self.__run)
        self.__ui.donate_pushButton.clicked.connect(self.__donate_clicked)
        self.__ui.game_directory_lineEdit.editingFinished.connect(self.__game_directory_changed)
        self.__ui.original_directory_lineEdit.editingFinished.connect(self.__original_directory_changed)
        self.__ui.previous_directory_lineEdit.editingFinished.connect(self.__previous_directory_changed)
        self.__ui.target_directory_lineEdit.editingFinished.connect(self.__target_directory_changed)
        self.__ui.selector_original_language_comboBox.currentTextChanged.connect(self.__original_language_changed)
        self.__ui.comboBox.currentTextChanged.connect(self.__change_language)

        self.__prepper = Prepper()
        self.__performer: Performer | None = None

    def __init_languages(self):
        self.__translators = []
        languages_list = ['Русский']
        for directory in TRANSLATIONS_DIR.iterdir():
            if directory.is_dir() and directory.name != "__pycache__":
                languages_list.append(directory.name)
        self.__ui.comboBox.addItems(languages_list)
        self.__ui.comboBox.setCurrentIndex(0)
        self.__change_language()

    def __change_language(self):
        def set_translators():
            for _translator in self.__translators:
                app.installTranslator(_translator)

        def del_translators():
            for _translator in self.__translators:
                app.removeTranslator(_translator)

        del_translators()

        self.__translators.clear()
        if self.__ui.comboBox.currentText() != 'Русский':
            current_language = self.__ui.comboBox.currentText()
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

    def __select_game_directory(self):
        chosen_path = QtWidgets.QFileDialog.getExistingDirectory(caption='Get Path',
                                                                 directory=self.__last_selected_directory)
        self.__ui.game_directory_lineEdit.setText(chosen_path)
        self.__last_selected_directory = chosen_path
        self.__game_directory_changed()

    def __game_directory_changed(self):
        self.__prepper.set_game_path(self.__ui.game_directory_lineEdit.text())
        if not self.__prepper.get_game_path_validate_result():
            self.__ui.game_directory_lineEdit.setText('')
            if not str(self.__prepper.get_game_path()) == '.':
                error = CustomDialog(parent=self.__ui.centralwidget,
                                     text=f'{self.__prepper.get_game_path()} '
                                          f'- {LanguageConstants.error_folder_does_not_exist}')
                error.show()
        self.__check_readiness()

    def __select_original_directory(self):
        chosen_path = QtWidgets.QFileDialog.getExistingDirectory(caption='Get Path',
                                                                 directory=self.__last_selected_directory)
        self.__ui.original_directory_lineEdit.setText(chosen_path)
        self.__last_selected_directory = chosen_path
        self.__original_directory_changed()

    def __original_directory_changed(self):
        self.__prepper.set_original_mode_path(
            original_mode_path=self.__ui.original_directory_lineEdit.text(),
            original_language=self.__ui.selector_original_language_comboBox.currentText()
        )
        self.__form_checkbox_cascade(self.__prepper.get_original_mode_path_validate_result())
        if not self.__prepper.get_original_mode_path_validate_result():
            self.__ui.original_directory_lineEdit.setText('')
        self.__check_readiness()

    def __select_previous_directory(self):
        chosen_path = QtWidgets.QFileDialog.getExistingDirectory(caption='Get Path',
                                                                 directory=self.__last_selected_directory)
        self.__ui.previous_directory_lineEdit.setText(chosen_path)
        self.__last_selected_directory = chosen_path
        self.__previous_directory_changed()

    def __previous_directory_changed(self):
        self.__prepper.set_previous_path(previous_path=self.__ui.previous_directory_lineEdit.text())
        if not self.__prepper.get_previous_path_validate_result():
            self.__ui.previous_directory_lineEdit.setText('')
            if not str(self.__prepper.get_previous_path()) == '.':
                error = CustomDialog(parent=self.__ui.centralwidget,
                                     text=f'{self.__prepper.get_previous_path()} - '
                                          f'{LanguageConstants.error_folder_does_not_exist}')
                error.show()

    def __select_target_directory(self):
        chosen_path = QtWidgets.QFileDialog.getExistingDirectory(caption='Get Path',
                                                                 directory=self.__last_selected_directory)
        self.__ui.target_directory_lineEdit.setText(chosen_path)
        self.__last_selected_directory = chosen_path
        self.__target_directory_changed()

    def __target_directory_changed(self):
        self.__prepper.set_target_path(self.__ui.target_directory_lineEdit.text())
        if not self.__prepper.get_target_path_validate_result():
            error = CustomDialog(parent=self.__ui.centralwidget,
                                 text=f'{LanguageConstants.error_drive_not_exist}')
            error.show()
        self.__check_readiness()

    def __original_language_changed(self):
        if self.__ui.original_directory_lineEdit.text():
            self.__original_directory_changed()

    def __need_translate_changed(self):
        if self.__ui.need_translation_checkBox.isChecked():
            self.__ui.need_translate_scrollArea.setEnabled(True)
        else:
            self.__ui.need_translate_scrollArea.setEnabled(False)

    def __check_readiness(self):
        if self.__prepper.get_original_mode_path_validate_result() and self.__prepper.get_game_path_validate_result() \
                and self.__prepper.get_target_path_validate_result():
            self.__ui.run_pushButton.setEnabled(True)
        else:
            self.__ui.run_pushButton.setEnabled(False)

    def __form_checkbox_cascade(self, validate_result: bool):
        match validate_result:
            case True:
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
            case False:
                info_label = QtWidgets.QLabel(
                    f'{self.__prepper.get_original_mode_path()} - {LanguageConstants.error_folder_does_not_exist}')
                font = QtGui.QFont()
                font.setBold(True)
                info_label.setFont(font)
                info_label.setAlignment(QtCore.Qt.AlignHCenter)
                self.__ui.need_translate_scrollArea.setWidget(info_label)
                error = CustomDialog(parent=self.__ui.centralwidget,
                                     text=f'{self.__prepper.get_original_mode_path()} -'
                                          f' {LanguageConstants.error_folder_does_not_exist}')
                error.show()

    def __check_all_checkboxes(self):
        for checkbox in self.__ui.need_translate_scrollArea.widget().children():
            if isinstance(checkbox, QtWidgets.QCheckBox):
                checkbox.setChecked(True)

    def __unchecked_all_checkboxes(self):
        for checkbox in self.__ui.need_translate_scrollArea.widget().children():
            if isinstance(checkbox, QtWidgets.QCheckBox):
                checkbox.setChecked(False)

    def __get_all_checkboxes(self) -> tuple:
        r"""Возвращает кортеж из путей(Path()), отмеченных в ScrollArea"""
        enabled = []
        for checkbox in self.__ui.need_translate_scrollArea.widget().children():
            if isinstance(checkbox, QtWidgets.QCheckBox) and checkbox.isChecked():
                enabled.append(Path(checkbox.objectName()))
        return tuple(enabled)

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

    def __run(self):
        self.__ui.progressBar.setValue(0)
        self.__performer = Performer(
            paths=self.__prepper,
            original_language=self.__ui.selector_original_language_comboBox.currentText(),
            target_language=self.__ui.selector_target_language_comboBox.currentText(),
            need_translate=self.__ui.need_translation_checkBox.isChecked(),
            need_translate_tuple=self.__get_all_checkboxes()
        )

        self.__ui.run_pushButton.setEnabled(False)

        self.__running_thread = QtCore.QThread()

        self.__performer.moveToThread(self.__running_thread)

        # Коннекты сигналов и слотов для межпоточной передачи информации
        self.__performer.info_console_value.connect(self.add_text_in_console)
        self.__performer.info_label_value.connect(self.set_info_label_new_value)
        self.__performer.progress_bar_value.connect(self.set_progressbar_new_value)
        self.__performer.finish_thread.connect(self.stop_thread)

        self.__running_thread.started.connect(self.__performer.run)

        self.__running_thread.start()


class CustomDialog(QtWidgets.QDialog):

    def __init__(self, parent=None, text=None):
        super(CustomDialog, self).__init__(parent)
        self.__ui = Ui_Dialog()
        self.__ui.setupUi(self)
        CustomDialog.setFixedSize(self, self.size())
        self.setWindowIcon(QtGui.QIcon('icons/error icon.jpg'))

        self.__ui.no_path_error_textBrowser.setText(text)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = MainWindow()
    application.show()

    sys.exit(app.exec_())
