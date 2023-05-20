from PyQt5 import QtCore, QtWidgets, QtGui
from PIL import ImageQt
import qrcode
import qrcode.image.styledpil
import qrcode.image.styles.moduledrawers
import qrcode.image.styles.colormasks


class QrDialog:
    def __init__(self, url: str):
        self.dialog = QtWidgets.QDialog()
        self.url = url

        self.setup_ui()
        self.retranslate_ui()

        self.dialog.exec()

    def setup_ui(self):
        self.dialog.resize(348, 452)

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.dialog)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(40, 360, 279, 80))

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)

        self.pushButton = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.horizontalLayout.addWidget(self.pushButton)

        self.pushButton_2 = QtWidgets.QPushButton(self.horizontalLayoutWidget)
        self.horizontalLayout.addWidget(self.pushButton_2)

        self.label = QtWidgets.QLabel(self.dialog)
        self.label.setGeometry(QtCore.QRect(70, 50, 200, 200))

        self.img = QtGui.QPixmap.fromImage(ImageQt.ImageQt(self.qrcode()))
        self.label.setPixmap(self.img)

        self.label_2 = QtWidgets.QLabel(self.dialog)
        self.label_2.setGeometry(QtCore.QRect(110, 330, 151, 17))

        self.pushButton.clicked.connect(self.copy_clipboard)
        self.pushButton_2.clicked.connect(self.dialog.close)

    def retranslate_ui(self):
        self.dialog.setWindowTitle('Feed')
        self.pushButton.setText('Copy link to clipboard')
        self.pushButton_2.setText('Close')

    def copy_clipboard(self):
        self.cb = QtGui.QGuiApplication.clipboard()
        self.cb.clear(mode=self.cb.Clipboard)
        self.cb.setText(self.url, mode=self.cb.Clipboard)
        self.label_2.setText('Copied to clipboard')

    def qrcode(self):
        self.qr = qrcode.QRCode(
                error_correction=qrcode.constants.ERROR_CORRECT_H,
                version=3,
                box_size=20,
                border=3)

        self.qr.add_data(self.url)
        return self.qr.make_image(image_factory=qrcode.image.styledpil.StyledPilImage,
                                  module_drawer=qrcode.image.styles.moduledrawers.VerticalBarsDrawer(),
                                  embeded_image_path='rss.png',
                                  color_mask=qrcode.image.styles.colormasks.SolidFillColorMask(
                                      front_color=(0xff, 0xff, 0xff),
                                      back_color=(0xf7, 0x84, 0x22))).get_image().resize((200, 200))
