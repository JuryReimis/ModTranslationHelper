import csv
import os
import sys
import time
from collections.abc import Iterable

from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QAbstractItemView

import settings
from gui.window_ui.BaseTable import Ui_table_for_stat
from gui.window_ui.StatTableWindow import Ui_StatTable
from PyQt5 import QtWidgets

from info_data import InfoData
from languages.language_constants import StatWindowConstants


class BaseTable(QtWidgets.QWidget):
    def __init__(self, parent=None, data: dict = None, general=False):
        super(BaseTable, self).__init__(parent=parent)
        self.__ui = Ui_table_for_stat()
        self.__ui.setupUi(self)

        self.__ui.link_pushButton.setText(StatWindowConstants.open_file)

        self.data = data

        self.general = general
        self.create_table()

        self.__ui.link_pushButton.clicked.connect(self.open_button_link)

    def create_table(self):
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels((StatWindowConstants.name_column_param, StatWindowConstants.name_column_value))
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
        self.__ui.tableView.setHorizontalScrollMode(QAbstractItemView.ScrollPerPixel)
        self.__ui.tableView.setMaximumHeight(self.getQTableWidgetHeight())
        self.__ui.tableView.setMinimumHeight(self.getQTableWidgetHeight())

    def open_button_link(self):
        os.startfile(self.data.get('title'))

    def getQTableWidgetHeight(self):
        r"""Решение с https://stackoverflow.com/questions/41542934/remove-scrollbar-to-show-full-table"""
        h = self.__ui.tableView.horizontalHeader().height() + 4
        for i in range(self.__ui.tableView.model().rowCount()):
            h += self.__ui.tableView.rowHeight(i)
        return h


class StatTableWindow(QtWidgets.QDialog):
    def __init__(self, parent=None, data: InfoData = None):
        super(StatTableWindow, self).__init__(parent=parent)
        self.__ui = Ui_StatTable()
        self.__ui.setupUi(self)
        if parent:
            self.resize(parent.size() * 0.75)
        self.csv_directory = None
        self.check_statements_directory()

        self.__ui.save_csv_pushButton.clicked.connect(self.save_csv)
        self.__ui.open_statements_pushButton.clicked.connect(self.open_statements_directory)
        self.__ui.close_pushButton.clicked.connect(self.close)

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

    def check_statements_directory(self):
        base_mth_directory = settings.HOME_DIR / 'Documents' / 'ModTranslationHelper'
        if base_mth_directory.exists():
            self.csv_directory = base_mth_directory / 'statements'
        else:
            self.csv_directory = settings.BASE_DIR / 'statements'
        if not self.csv_directory.exists():
            self.csv_directory.mkdir()

    def save_csv(self):
        new_csv = self.csv_directory / f'{self.data.title}_{time.strftime("%H-%M-%S_%y_%m_%d", time.localtime(time.time()))}.csv'
        with new_csv.open(mode='w') as f:
            row_names = ['name', 'value']
            writer = csv.DictWriter(fieldnames=row_names, lineterminator='\r', delimiter=';', f=f)
            for row in self.data.get_data_for_csv():
                writer.writerow(row)
        os.startfile(new_csv)

    def open_statements_directory(self):
        os.startfile(self.csv_directory)


if __name__ == '__main__':
    app = QtWidgets.QApplication([])
    application = StatTableWindow()
    application.show()
    sys.exit(app.exec_())
