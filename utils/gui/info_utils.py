from PyQt5 import QtWidgets
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QLabel

import qtawesome as qta


class AddInfoIcons:
    stylesheet = "QToolTip { color: #29ab87;" \
                 " font-size: 18px;" \
                 " font-weight: bold; }"

    def __init__(self, layouts: dict):
        for layout, text in layouts.items():
            layout: QtWidgets.QHBoxLayout
            info_icon = layout.itemAt(1)
            if not info_icon:
                info_icon = self.get_icon()
                info_icon.setToolTip(text)
                info_icon.setStyleSheet(self.stylesheet)
                layout.addWidget(info_icon)

            else:
                widget = info_icon.widget()
                widget.setStyleSheet(self.stylesheet)
                widget.setToolTip(text)

    @staticmethod
    def get_icon():
        icon = QLabel()
        icon.setPixmap(qta.icon('fa5.question-circle').pixmap(QSize(16, 16)))
        return icon
