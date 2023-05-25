import csv
import os
import sys
from collections.abc import Iterable

from PyQt5.QtGui import QStandardItemModel, QStandardItem

from gui.window_ui.BaseTable import Ui_table_for_stat
from gui.window_ui.StatTableWindow import Ui_StatTable
from PyQt5 import QtWidgets

from info_data import InfoData


class BaseTable(QtWidgets.QWidget):
    def __init__(self, parent=None, data: dict = None, general=False):
        super(BaseTable, self).__init__(parent=parent)
        self.__ui = Ui_table_for_stat()
        self.__ui.setupUi(self)

        self.__ui.link_pushButton.setText('Открыть файл')

        self.data = data

        self.general = general
        self.create_table()

        self.__ui.link_pushButton.clicked.connect(self.open_button_link)

    def create_table(self):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(('Параметр', 'Результат'))
        self.__ui.tableView.setModel(model)
        self.__ui.title_label.setText(str(self.data.get('title', {})))
        if self.general:
            self.__ui.link_pushButton.hide()
        for name_value in self.data.get('expanded_data', {}):
            name, value = name_value.get('name'), name_value.get('value')
            if isinstance(value, Iterable) and not isinstance(value, str):
                value = ", ".join(map(str, value))
            row = QStandardItem(name), QStandardItem(str(value))
            model.appendRow(row)
        self.__ui.tableView.resizeColumnsToContents()
        self.__ui.tableView.resizeRowsToContents()

    def open_button_link(self):
        os.startfile(self.data.get('title'))


class StatTableWindow(QtWidgets.QDialog):
    def __init__(self, parent=None, data: InfoData = None):
        super(StatTableWindow, self).__init__(parent=parent)
        self.__ui = Ui_StatTable()
        self.__ui.setupUi(self)
        if parent:
            self.resize(parent.size() * 0.75)

        self.data = data

        self.vertical_layout_widget = QtWidgets.QWidget()
        self.vertical_layout = QtWidgets.QVBoxLayout()
        self.vertical_layout_widget.setLayout(self.vertical_layout)
        self.__ui.scrollArea.setWidget(self.vertical_layout_widget)

        general_table = BaseTable(parent=self, data=self.data.get_data_for_general(), general=True)
        self.vertical_layout.addWidget(general_table)
        self.create_file_tables()

    def create_file_tables(self):
        for file in self.data.files_info.values():
            file_table = BaseTable(parent=self, data=file.get_file_data())
            self.vertical_layout.addWidget(file_table)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = StatTableWindow()
    application.show()
    sys.exit(app.exec_())
