from typing import Any
from PyQt5 import QtCore, QtWidgets


class QrDialog:
    def __init__(self, url: str, pic: Any):
        self.dialog = QtWidgets.QDialog()

        self.url = url
        self.pic = pic

        self.setup_ui()
        self.dialog.exec()

    def setup_ui(self):
        self.dialog.setObjectName('QrDialog')
        self.dialog.resize(348, 452)
        self.horizontalLayoutWidget = QtWidgets.QWidget(self.dialog)

        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(40, 360, 279, 80))
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)

        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.horizontalLayout.addWidget(self.pushButton_2)

        self.label = QtWidgets.QLabel(self.dialog)
        self.label.setGeometry(QtCore.QRect(130, 130, 69, 21))

        self.retranslate_ui(self.dialog)
        QtCore.QMetaObject.connectSlotsByName(self.dialog)


    def retranslate_ui(self):
        self.dialog.setWindowTitle(QtCore.QCoreApplication.translate('QrDialog', 'Feed'))
        self.pushButton.setText(QtCore.QCoreApplication.translate('QrDialog', 'Copy link to clipboard'))
        self.pushButton_2.setText(QtCore.QCoreApplication.translate('QrDialog', 'Close'))
        self.label.setText(QtCore.QCoreApplication.translate('QrDialog', 'TextLabel'))
