from PyQt5 import QtWidgets, QtGui, QtCore

import sys
from pathlib import Path

from custom_dialog_test1 import Ui_Dialog
from main import Prepper
from test1 import Ui_MainWindow
from deep_translator import GoogleTranslator


class MyWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        MyWindow.setFixedSize(self, self.size())

        self.last_selected_directory = '/'
        self.ui.run_pushButton.setText('Start')
        self.ui.run_pushButton.setEnabled(False)
        for language in GoogleTranslator.get_supported_languages():
            self.ui.selector_original_language_comboBox.addItem(language)
            self.ui.selector_target_language_comboBox.addItem(language)
        self.ui.selector_original_language_comboBox.setCurrentText('english')
        self.ui.selector_target_language_comboBox.setCurrentText('russian')

        self.ui.game_directory_pushButton.clicked.connect(self.select_game_directory)
        self.ui.original_directory_pushButton.clicked.connect(self.select_original_directory)
        self.ui.previous_directory_pushButton.clicked.connect(self.select_previous_directory)
        self.ui.target_directory_pushButton.clicked.connect(self.select_target_directory)
        self.ui.need_translation_checkBox.stateChanged.connect(self.need_translate_changed)
        self.ui.run_pushButton.clicked.connect(self.run)
        self.ui.game_directory_lineEdit.editingFinished.connect(self.game_directory_changed)
        self.ui.original_directory_lineEdit.editingFinished.connect(self.original_directory_changed)
        self.ui.previous_directory_lineEdit.editingFinished.connect(self.previous_directory_changed)
        self.ui.target_directory_lineEdit.editingFinished.connect(self.target_directory_changed)

        self.prepper = Prepper()

    def select_game_directory(self):
        chosen_path = QtWidgets.QFileDialog.getExistingDirectory(caption='Get Path',
                                                                 directory=self.last_selected_directory)
        self.ui.game_directory_lineEdit.setText(chosen_path)
        self.last_selected_directory = chosen_path

    def game_directory_changed(self):
        self.prepper.set_game_path(self.ui.game_directory_lineEdit.text())

    def select_original_directory(self):
        chosen_path = QtWidgets.QFileDialog.getExistingDirectory(caption='Get Path',
                                                                 directory=self.last_selected_directory)
        self.ui.original_directory_lineEdit.setText(chosen_path)
        self.last_selected_directory = chosen_path
        self.original_directory_changed()

    def original_directory_changed(self):
        self.prepper.set_original_mode_path(self.ui.original_directory_lineEdit.text())
        self.form_checkbox_cascade(self.prepper.get_original_mode_path_validate_result())

    def select_previous_directory(self):
        chosen_path = QtWidgets.QFileDialog.getExistingDirectory(caption='Get Path',
                                                                 directory=self.last_selected_directory)
        self.ui.previous_directory_lineEdit.setText(chosen_path)
        self.last_selected_directory = chosen_path

    def previous_directory_changed(self):
        pass

    def select_target_directory(self):
        chosen_path = QtWidgets.QFileDialog.getExistingDirectory(caption='Get Path',
                                                                 directory=self.last_selected_directory)
        self.ui.target_directory_lineEdit.setText(chosen_path)
        self.last_selected_directory = chosen_path
        self.target_directory_changed()

    def target_directory_changed(self, ):
        self.prepper.set_target_path(self.ui.target_directory_lineEdit.text())
        if not self.prepper.get_target_path_validate_result():
            error = CustomDialog(parent=self.ui.centralwidget,
                                 text='Невозможно получить доступ к диск. Проверьте путь к папке, в которую '
                                      'собираетесь записать перевод')
            error.show()

    def form_checkbox_cascade(self, validate_result: bool):
        match validate_result:
            case True:
                files = self.prepper.get_original_localization_hierarchy()
                vertical_layout_widget = QtWidgets.QWidget()
                vertical_layout = QtWidgets.QVBoxLayout(vertical_layout_widget)
                for file_name in files:
                    file_name: Path
                    check_box = QtWidgets.QCheckBox(str(file_name))
                    check_box.setObjectName(str(file_name))
                    check_box.setChecked(True)
                    vertical_layout.addWidget(check_box)
                vertical_layout_widget.setLayout(vertical_layout)
                self.ui.need_translate_scrollArea.setWidget(vertical_layout_widget)
            case False:
                info_label = QtWidgets.QLabel('Указанная директория с модом\n-\nне существует')
                font = QtGui.QFont()
                font.setBold(True)
                info_label.setFont(font)
                info_label.setAlignment(QtCore.Qt.AlignHCenter)
                self.ui.need_translate_scrollArea.setWidget(info_label)
                error = CustomDialog(parent=self.ui.centralwidget,
                                     text='Указанная директория с модом - не существует')
                error.show()

    def need_translate_changed(self):
        if self.ui.need_translation_checkBox.isChecked():
            self.ui.need_translate_scrollArea.setEnabled(True)
        else:
            self.ui.need_translate_scrollArea.setEnabled(False)

    def run(self):
        pass

    def get_all_checkbox(self):
        for checkbox in self.ui.need_translate_scrollArea.widget().children():
            print(checkbox.objectName())


class CustomDialog(QtWidgets.QDialog):

    def __init__(self, parent=None, text=None):
        super(CustomDialog, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        CustomDialog.setFixedSize(self, self.size())

        self.ui.no_path_error_textBrowser.setText(text)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = MyWindow()
    application.show()

    sys.exit(app.exec_())
