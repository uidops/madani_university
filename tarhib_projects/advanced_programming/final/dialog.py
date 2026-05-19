from PyQt5 import QtCore, QtWidgets


class Dialog:
    def __init__(self):
        self.dialog = QtWidgets.QDialog()
        self.res = False

        self.setup_ui()
        self.retranslate_ui()

        self.dialog.exec()

    def setup_ui(self):
        self.dialog.resize(400, 70)

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.dialog)
        self.verticalLayout = QtWidgets.QVBoxLayout()

        self.linkEdit = QtWidgets.QLineEdit(self.dialog)
        self.verticalLayout.addWidget(self.linkEdit)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.buttonBox = QtWidgets.QDialogButtonBox(self.dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(
                QtWidgets.QDialogButtonBox.Cancel |
                QtWidgets.QDialogButtonBox.Ok)

        self.horizontalLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

    def retranslate_ui(self):
        self.dialog.setWindowTitle('New RSS Feed')
        self.linkEdit.setPlaceholderText('http://example.com/feeds.xml')

    def accept(self):
        self.res = True
        self.dialog.close()

    def reject(self):
        self.res = False
        self.dialog.close()
