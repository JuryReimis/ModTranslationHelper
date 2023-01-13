# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\test_ui\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setWindowModality(QtCore.Qt.NonModal)
        MainWindow.setEnabled(True)
        MainWindow.resize(1281, 808)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setBaseSize(QtCore.QSize(222, 35))
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        MainWindow.setIconSize(QtCore.QSize(24, 24))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_2.setGeometry(QtCore.QRect(530, 680, 741, 81))
        self.horizontalLayoutWidget_2.setObjectName("horizontalLayoutWidget_2")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.info_label = QtWidgets.QLabel(self.horizontalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.info_label.sizePolicy().hasHeightForWidth())
        self.info_label.setSizePolicy(sizePolicy)
        self.info_label.setMinimumSize(QtCore.QSize(250, 0))
        self.info_label.setMaximumSize(QtCore.QSize(250, 16777215))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.info_label.setFont(font)
        self.info_label.setText("")
        self.info_label.setObjectName("info_label")
        self.horizontalLayout_5.addWidget(self.info_label)
        self.progressBar = QtWidgets.QProgressBar(self.horizontalLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy)
        self.progressBar.setMinimumSize(QtCore.QSize(265, 0))
        self.progressBar.setMaximumSize(QtCore.QSize(265, 16777215))
        self.progressBar.setMaximum(100000000)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setTextDirection(QtWidgets.QProgressBar.TopToBottom)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_5.addWidget(self.progressBar)
        self.horizontalLayout_6.addLayout(self.horizontalLayout_5)
        self.run_pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget_2)
        self.run_pushButton.setEnabled(False)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.run_pushButton.sizePolicy().hasHeightForWidth())
        self.run_pushButton.setSizePolicy(sizePolicy)
        self.run_pushButton.setMinimumSize(QtCore.QSize(110, 50))
        self.run_pushButton.setObjectName("run_pushButton")
        self.horizontalLayout_6.addWidget(self.run_pushButton)
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 50, 1261, 381))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.original_directory_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.original_directory_lineEdit.sizePolicy().hasHeightForWidth())
        self.original_directory_lineEdit.setSizePolicy(sizePolicy)
        self.original_directory_lineEdit.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.original_directory_lineEdit.setFont(font)
        self.original_directory_lineEdit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.original_directory_lineEdit.setObjectName("original_directory_lineEdit")
        self.gridLayout_3.addWidget(self.original_directory_lineEdit, 4, 1, 1, 1)
        self.target_directory_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.target_directory_lineEdit.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.target_directory_lineEdit.sizePolicy().hasHeightForWidth())
        self.target_directory_lineEdit.setSizePolicy(sizePolicy)
        self.target_directory_lineEdit.setMaximumSize(QtCore.QSize(16777215, 25))
        self.target_directory_lineEdit.setSizeIncrement(QtCore.QSize(0, 0))
        self.target_directory_lineEdit.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.target_directory_lineEdit.setFont(font)
        self.target_directory_lineEdit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.target_directory_lineEdit.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.target_directory_lineEdit.setObjectName("target_directory_lineEdit")
        self.gridLayout_3.addWidget(self.target_directory_lineEdit, 9, 1, 1, 1)
        self.game_directory_info_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.game_directory_info_label.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.game_directory_info_label.setFont(font)
        self.game_directory_info_label.setObjectName("game_directory_info_label")
        self.gridLayout_3.addWidget(self.game_directory_info_label, 0, 0, 1, 3)
        self.selector_original_language_comboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.selector_original_language_comboBox.setMaximumSize(QtCore.QSize(119, 25))
        self.selector_original_language_comboBox.setPlaceholderText("")
        self.selector_original_language_comboBox.setObjectName("selector_original_language_comboBox")
        self.gridLayout_3.addWidget(self.selector_original_language_comboBox, 5, 2, 1, 1)
        self.game_directory_pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.game_directory_pushButton.sizePolicy().hasHeightForWidth())
        self.game_directory_pushButton.setSizePolicy(sizePolicy)
        self.game_directory_pushButton.setMaximumSize(QtCore.QSize(119, 25))
        self.game_directory_pushButton.setObjectName("game_directory_pushButton")
        self.gridLayout_3.addWidget(self.game_directory_pushButton, 1, 2, 1, 1)
        self.original_directory_info_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.original_directory_info_label.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.original_directory_info_label.setFont(font)
        self.original_directory_info_label.setObjectName("original_directory_info_label")
        self.gridLayout_3.addWidget(self.original_directory_info_label, 3, 0, 1, 3)
        self.previous_directory_pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previous_directory_pushButton.sizePolicy().hasHeightForWidth())
        self.previous_directory_pushButton.setSizePolicy(sizePolicy)
        self.previous_directory_pushButton.setMaximumSize(QtCore.QSize(119, 25))
        self.previous_directory_pushButton.setObjectName("previous_directory_pushButton")
        self.gridLayout_3.addWidget(self.previous_directory_pushButton, 7, 2, 1, 1)
        self.target_directory_label = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.target_directory_label.sizePolicy().hasHeightForWidth())
        self.target_directory_label.setSizePolicy(sizePolicy)
        self.target_directory_label.setMinimumSize(QtCore.QSize(200, 0))
        self.target_directory_label.setMaximumSize(QtCore.QSize(200, 35))
        self.target_directory_label.setBaseSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.target_directory_label.setFont(font)
        self.target_directory_label.setMouseTracking(False)
        self.target_directory_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.target_directory_label.setObjectName("target_directory_label")
        self.gridLayout_3.addWidget(self.target_directory_label, 9, 0, 1, 1)
        self.target_directory_pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.target_directory_pushButton.sizePolicy().hasHeightForWidth())
        self.target_directory_pushButton.setSizePolicy(sizePolicy)
        self.target_directory_pushButton.setMaximumSize(QtCore.QSize(119, 25))
        self.target_directory_pushButton.setObjectName("target_directory_pushButton")
        self.gridLayout_3.addWidget(self.target_directory_pushButton, 9, 2, 1, 1)
        self.original_directory_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.original_directory_label.setEnabled(True)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.original_directory_label.sizePolicy().hasHeightForWidth())
        self.original_directory_label.setSizePolicy(sizePolicy)
        self.original_directory_label.setMinimumSize(QtCore.QSize(200, 0))
        self.original_directory_label.setMaximumSize(QtCore.QSize(200, 35))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.original_directory_label.setFont(font)
        self.original_directory_label.setObjectName("original_directory_label")
        self.gridLayout_3.addWidget(self.original_directory_label, 4, 0, 1, 1)
        self.original_directory_pushButton = QtWidgets.QPushButton(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Maximum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.original_directory_pushButton.sizePolicy().hasHeightForWidth())
        self.original_directory_pushButton.setSizePolicy(sizePolicy)
        self.original_directory_pushButton.setMaximumSize(QtCore.QSize(119, 25))
        self.original_directory_pushButton.setObjectName("original_directory_pushButton")
        self.gridLayout_3.addWidget(self.original_directory_pushButton, 4, 2, 1, 1)
        self.previous_directory_info_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.previous_directory_info_label.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.previous_directory_info_label.setFont(font)
        self.previous_directory_info_label.setObjectName("previous_directory_info_label")
        self.gridLayout_3.addWidget(self.previous_directory_info_label, 6, 0, 1, 3)
        self.target_directory_info_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.target_directory_info_label.setMaximumSize(QtCore.QSize(16777215, 16777215))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.target_directory_info_label.setFont(font)
        self.target_directory_info_label.setObjectName("target_directory_info_label")
        self.gridLayout_3.addWidget(self.target_directory_info_label, 8, 0, 1, 3)
        self.previous_directory_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previous_directory_lineEdit.sizePolicy().hasHeightForWidth())
        self.previous_directory_lineEdit.setSizePolicy(sizePolicy)
        self.previous_directory_lineEdit.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.previous_directory_lineEdit.setFont(font)
        self.previous_directory_lineEdit.setObjectName("previous_directory_lineEdit")
        self.gridLayout_3.addWidget(self.previous_directory_lineEdit, 7, 1, 1, 1)
        self.game_directory_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.game_directory_lineEdit.sizePolicy().hasHeightForWidth())
        self.game_directory_lineEdit.setSizePolicy(sizePolicy)
        self.game_directory_lineEdit.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.game_directory_lineEdit.setFont(font)
        self.game_directory_lineEdit.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.game_directory_lineEdit.setObjectName("game_directory_lineEdit")
        self.gridLayout_3.addWidget(self.game_directory_lineEdit, 1, 1, 1, 1)
        self.previous_directory_label = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.previous_directory_label.sizePolicy().hasHeightForWidth())
        self.previous_directory_label.setSizePolicy(sizePolicy)
        self.previous_directory_label.setMinimumSize(QtCore.QSize(200, 0))
        self.previous_directory_label.setMaximumSize(QtCore.QSize(200, 35))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.previous_directory_label.setFont(font)
        self.previous_directory_label.setObjectName("previous_directory_label")
        self.gridLayout_3.addWidget(self.previous_directory_label, 7, 0, 1, 1)
        self.game_directory_label = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.game_directory_label.sizePolicy().hasHeightForWidth())
        self.game_directory_label.setSizePolicy(sizePolicy)
        self.game_directory_label.setMinimumSize(QtCore.QSize(200, 0))
        self.game_directory_label.setMaximumSize(QtCore.QSize(200, 35))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.game_directory_label.setFont(font)
        self.game_directory_label.setObjectName("game_directory_label")
        self.gridLayout_3.addWidget(self.game_directory_label, 1, 0, 1, 1)
        self.selector_target_language_comboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.selector_target_language_comboBox.setMaximumSize(QtCore.QSize(119, 25))
        self.selector_target_language_comboBox.setObjectName("selector_target_language_comboBox")
        self.gridLayout_3.addWidget(self.selector_target_language_comboBox, 10, 2, 1, 1)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.need_translation_info_label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.need_translation_info_label.setMaximumSize(QtCore.QSize(16777215, 35))
        font = QtGui.QFont()
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        self.need_translation_info_label.setFont(font)
        self.need_translation_info_label.setObjectName("need_translation_info_label")
        self.verticalLayout.addWidget(self.need_translation_info_label)
        self.need_translation_info_label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.need_translation_info_label_2.setStyleSheet("QLabel { color : red; }")
        self.need_translation_info_label_2.setObjectName("need_translation_info_label_2")
        self.verticalLayout.addWidget(self.need_translation_info_label_2)
        self.gridLayout_3.addLayout(self.verticalLayout, 10, 0, 1, 2)
        self.need_translation_checkBox = QtWidgets.QCheckBox(self.gridLayoutWidget)
        self.need_translation_checkBox.setMaximumSize(QtCore.QSize(16777215, 25))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.need_translation_checkBox.setFont(font)
        self.need_translation_checkBox.setIconSize(QtCore.QSize(16, 16))
        self.need_translation_checkBox.setObjectName("need_translation_checkBox")
        self.gridLayout_3.addWidget(self.need_translation_checkBox, 11, 0, 1, 2)
        self.need_translate_scrollArea = QtWidgets.QScrollArea(self.centralwidget)
        self.need_translate_scrollArea.setEnabled(False)
        self.need_translate_scrollArea.setGeometry(QtCore.QRect(10, 440, 511, 311))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.need_translate_scrollArea.setFont(font)
        self.need_translate_scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.need_translate_scrollArea.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.need_translate_scrollArea.setWidgetResizable(True)
        self.need_translate_scrollArea.setObjectName("need_translate_scrollArea")
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 492, 309))
        self.scrollAreaWidgetContents.setObjectName("scrollAreaWidgetContents")
        self.need_translate_scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.console_textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.console_textBrowser.setGeometry(QtCore.QRect(530, 440, 741, 231))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.console_textBrowser.sizePolicy().hasHeightForWidth())
        self.console_textBrowser.setSizePolicy(sizePolicy)
        self.console_textBrowser.setReadOnly(True)
        self.console_textBrowser.setObjectName("console_textBrowser")
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 750, 511, 25))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.check_all_pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.check_all_pushButton.sizePolicy().hasHeightForWidth())
        self.check_all_pushButton.setSizePolicy(sizePolicy)
        self.check_all_pushButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.check_all_pushButton.setObjectName("check_all_pushButton")
        self.horizontalLayout.addWidget(self.check_all_pushButton)
        self.uncheck_all_pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.uncheck_all_pushButton.sizePolicy().hasHeightForWidth())
        self.uncheck_all_pushButton.setSizePolicy(sizePolicy)
        self.uncheck_all_pushButton.setMaximumSize(QtCore.QSize(100, 16777215))
        self.uncheck_all_pushButton.setObjectName("uncheck_all_pushButton")
        self.horizontalLayout.addWidget(self.uncheck_all_pushButton)
        self.horizontalLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayoutWidget_3.setGeometry(QtCore.QRect(10, 10, 221, 31))
        self.horizontalLayoutWidget_3.setObjectName("horizontalLayoutWidget_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label = QtWidgets.QLabel(self.horizontalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setMinimumSize(QtCore.QSize(100, 0))
        self.label.setMaximumSize(QtCore.QSize(100, 16777215))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout_2.addWidget(self.label)
        self.translation_comboBox = QtWidgets.QComboBox(self.horizontalLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.translation_comboBox.sizePolicy().hasHeightForWidth())
        self.translation_comboBox.setSizePolicy(sizePolicy)
        self.translation_comboBox.setMinimumSize(QtCore.QSize(0, 20))
        self.translation_comboBox.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.translation_comboBox.setInsertPolicy(QtWidgets.QComboBox.InsertAtBottom)
        self.translation_comboBox.setObjectName("translation_comboBox")
        self.horizontalLayout_2.addWidget(self.translation_comboBox)
        self.donate_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.donate_pushButton.setGeometry(QtCore.QRect(970, 10, 301, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.donate_pushButton.setFont(font)
        self.donate_pushButton.setObjectName("donate_pushButton")
        self.discord_link__pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.discord_link__pushButton.setGeometry(QtCore.QRect(660, 10, 301, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.discord_link__pushButton.setFont(font)
        self.discord_link__pushButton.setObjectName("discord_link__pushButton")
        self.program_version_label = QtWidgets.QLabel(self.centralwidget)
        self.program_version_label.setGeometry(QtCore.QRect(1070, 766, 201, 20))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.program_version_label.setFont(font)
        self.program_version_label.setText("")
        self.program_version_label.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.program_version_label.setObjectName("program_version_label")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.selector_original_language_comboBox.setCurrentIndex(-1)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "ModTranslationHelper by ReimiS"))
        self.progressBar.setFormat(_translate("MainWindow", "Обработка: %p%"))
        self.run_pushButton.setText(_translate("MainWindow", "Старт"))
        self.game_directory_info_label.setText(_translate("MainWindow", "1)Место, где установлена игра, для которой вы собираетесь переводить. Путь должен вести к папке с локализацией (там где находятся папки english, russian, french и т.д.) \n"
"Стандартный путь для Crusader Kings 3: ../Steam/steamapps/common/Crusader Kings III/game/localization"))
        self.game_directory_pushButton.setText(_translate("MainWindow", "Выбрать директорию"))
        self.original_directory_info_label.setText(_translate("MainWindow", "2)Папка, где хранится локализация мода, на который вы хотите создать перевод. Пример: ../Steam/steamapps/workshop/content/1158310/2507209632/localization"))
        self.previous_directory_pushButton.setText(_translate("MainWindow", "Выбрать директорию"))
        self.target_directory_label.setText(_translate("MainWindow", "Директория перевода"))
        self.target_directory_pushButton.setText(_translate("MainWindow", "Выбрать директорию"))
        self.original_directory_label.setText(_translate("MainWindow", "Директория локализации мода"))
        self.original_directory_pushButton.setText(_translate("MainWindow", "Выбрать директорию"))
        self.previous_directory_info_label.setText(_translate("MainWindow", "3)Если происходит обновление перевода и у вас уже есть готовый перевод предыдущей версии, то стоит указать директорию с предыдущей версией перевода.Программа сама пробежится\n"
"по старым файлам и использует строки, которые там найдет для построения новой версии. При этом все новые строки будут обработаны в обычном режиме и помечены комментарием #NT!"))
        self.target_directory_info_label.setText(_translate("MainWindow", "4)Папка, в которую будут помещены все файлы, созданные в результате работы программы.\n"
"(Точная копия оригинальной локализации по структуре папок и файлов, но с заменой данных о языке и с машинным переводом(если отмечен ниже).\n"
"Пример: Если выбран english, как исходный язык, а russian, как целевой, все l_english будут заменены на l_russian, а машинный перевод будет на русский язык)"))
        self.previous_directory_label.setText(_translate("MainWindow", "Предыдущая версия перевода"))
        self.game_directory_label.setText(_translate("MainWindow", "Директория игры"))
        self.need_translation_info_label.setText(_translate("MainWindow", "5)Если отметить - будет добавлен машинный перевод после оригинальной строки локализации. Строка будет выглядить так: ключ \"строка\" <\"машинный перевод\"> #NT!"))
        self.need_translation_info_label_2.setText(_translate("MainWindow", "Внимание! В таком случае использовать выданные программой файлы сразу - нельзя, машинный перевод будет добавлен сразу после оригинальной строки и не будет скрыт от игрока!"))
        self.need_translation_checkBox.setText(_translate("MainWindow", "Добавить машинный перевод"))
        self.check_all_pushButton.setText(_translate("MainWindow", "Отметить все"))
        self.uncheck_all_pushButton.setText(_translate("MainWindow", "Снять все"))
        self.label.setText(_translate("MainWindow", "Язык:"))
        self.donate_pushButton.setText(_translate("MainWindow", "Отблагодарить автора!"))
        self.discord_link__pushButton.setText(_translate("MainWindow", "Discord Server(обратная связь)"))
