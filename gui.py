from PyQt5 import QtWidgets
import sys

from main import get_original_localization_hierarchy
from test1 import Ui_MainWindow
from deep_translator import GoogleTranslator


class MyWindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent=parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

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
        self.ui.original_directory_lineEdit.editingFinished.connect(self.original_directory_changed)

        MyWindow.setFixedSize(self, self.size())

    def select_game_directory(self):
        chosen_path = QtWidgets.QFileDialog.getExistingDirectory(caption='Get Path',
                                                                 directory=self.last_selected_directory)
        self.ui.game_directory_lineEdit.setText(chosen_path)
        self.last_selected_directory = chosen_path

    def select_original_directory(self):
        chosen_path = QtWidgets.QFileDialog.getExistingDirectory(caption='Get Path',
                                                                 directory=self.last_selected_directory)
        self.ui.original_directory_lineEdit.setText(chosen_path)
        self.last_selected_directory = chosen_path
        self.original_directory_changed()

    def original_directory_changed(self):
        self.form_checkbox_cascade(self.ui.original_directory_lineEdit.text())

    def select_previous_directory(self):
        chosen_path = QtWidgets.QFileDialog.getExistingDirectory(caption='Get Path',
                                                                 directory=self.last_selected_directory)
        self.ui.previous_directory_lineEdit.setText(chosen_path)
        self.last_selected_directory = chosen_path

    def select_target_directory(self):
        chosen_path = QtWidgets.QFileDialog.getExistingDirectory(caption='Get Path',
                                                                 directory=self.last_selected_directory)
        self.ui.target_directory_lineEdit.setText(chosen_path)
        self.last_selected_directory = chosen_path

    def form_checkbox_cascade(self, path: str):
        files = get_original_localization_hierarchy(path)
        vertical_layout_widget = QtWidgets.QWidget()
        vertical_layout = QtWidgets.QVBoxLayout(vertical_layout_widget)
        for file_name in files:
            check_box = QtWidgets.QCheckBox(file_name)
            check_box.setChecked(True)
            vertical_layout.addWidget(check_box)
        vertical_layout_widget.setLayout(vertical_layout)
        self.ui.need_translate_scrollArea.setWidget(vertical_layout_widget)

    def need_translate_changed(self):
        if self.ui.need_translation_checkBox.isChecked():
            self.ui.need_translate_scrollArea.setEnabled(True)
        else:
            self.ui.need_translate_scrollArea.setEnabled(False)

    def run(self):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = MyWindow()
    application.show()

    sys.exit(app.exec_())
