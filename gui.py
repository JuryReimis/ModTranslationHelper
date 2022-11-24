from PyQt5 import QtWidgets
import sys
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
        self.ui.run_pushButton.clicked.connect(self.run)

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

    def run(self):
        pass


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = MyWindow()
    application.show()

    sys.exit(app.exec_())
