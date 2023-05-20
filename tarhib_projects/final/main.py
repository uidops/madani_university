#!/usr/bin/env python

from PyQt5 import QtCore, QtWidgets, QtGui
import xml.etree.ElementTree
import aiohttp
import asyncio
import base64
import datetime
import hashlib
import webbrowser

from database import DataBase
from dialog import Dialog


class Main:
    def __init__(self):
        self.db = DataBase()
        self.app = QtWidgets.QApplication(['rss'])
        self.mainwin = QtWidgets.QMainWindow()

        self.setup_ui()
        self.mainwin.show()

        self.show_urls()

        self.app.exec()
        self.db.con.close()

    def setup_ui(self):
        self.mainwin.setObjectName('MainWindow')
        self.mainwin.resize(899, 579)

        self.centralwidget = QtWidgets.QWidget(self.mainwin)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.centralwidget)

        self.listView = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.listView)

        self.progressBar_1 = QtWidgets.QProgressBar(self.listView)
        self.progressBar_1.setAutoFillBackground(False)
        self.progressBar_1.setProperty('value', 0)
        self.progressBar_1.setTextVisible(False)
        self.progressBar_1.setOrientation(QtCore.Qt.Vertical)
        self.progressBar_1.setTextDirection(
                QtWidgets.QProgressBar.TopToBottom)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.horizontalLayout_4.addWidget(self.progressBar_1)

        self.feedList = QtWidgets.QListWidget(self.listView)
        self.verticalLayout.addWidget(self.feedList)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.feedAddBtn = QtWidgets.QPushButton(self.listView)

        self.horizontalLayout.addWidget(self.feedAddBtn)
        self.feedDeleteBtn = QtWidgets.QPushButton(self.listView)
        self.horizontalLayout.addWidget(self.feedDeleteBtn)

        self.updateAllBtn = QtWidgets.QPushButton(self.listView)
        self.horizontalLayout.addWidget(self.updateAllBtn)

        self.progressBar_1 = QtWidgets.QProgressBar(self.listView)
        self.progressBar_1.setAutoFillBackground(False)
        self.progressBar_1.setProperty('value', 0)
        self.progressBar_1.setTextVisible(False)
        self.progressBar_1.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar_1.setTextDirection(
                QtWidgets.QProgressBar.TopToBottom)
        self.verticalLayout.addWidget(self.progressBar_1)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout()

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.entryListWidget = QtWidgets.QListWidget(self.listView)
        self.verticalLayout_2.addWidget(self.entryListWidget)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.horizontalLayout_5.addWidget(self.listView)

        self.articleView = QtWidgets.QWidget(self.centralwidget)
        self.articleView.setEnabled(True)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.articleView)
        self.verticalLayout_3.setContentsMargins(-1, 0, 9, -1)

        self.progressBar_2 = QtWidgets.QProgressBar(self.listView)
        self.progressBar_2.setAutoFillBackground(False)
        self.progressBar_2.setProperty('value', 0)
        self.progressBar_2.setTextVisible(False)
        self.progressBar_2.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar_2.setTextDirection(
                QtWidgets.QProgressBar.TopToBottom)
        self.verticalLayout_2.addWidget(self.progressBar_2)

        self.textBrowser = QtWidgets.QTextBrowser(self.articleView)
        self.textBrowser.loadResource = self.resource_handler
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.openLinks = self.open_browser
        self.verticalLayout_2.addWidget(self.textBrowser)

        self.horizontalLayout_5.addWidget(self.articleView)
        self.mainwin.setCentralWidget(self.centralwidget)

        self.statusBar = QtWidgets.QStatusBar(self.mainwin)
        self.mainwin.setStatusBar(self.statusBar)

        self.menuBar = QtWidgets.QMenuBar(self.mainwin)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 899, 29))

        self.menuEdit = QtWidgets.QMenu(self.menuBar)

        self.mainwin.setMenuBar(self.menuBar)
        self.actionNew_RSS_Feed = QtWidgets.QAction(self.mainwin)
        self.menuEdit.addAction(self.actionNew_RSS_Feed)

        self.actionQuit = QtWidgets.QAction(self.mainwin)
        self.menuEdit.addAction(self.actionQuit)

        self.menuBar.addAction(self.menuEdit.menuAction())

        self.retranslate_ui()

        self.actionNew_RSS_Feed.triggered.connect(self.add_rss)
        self.actionQuit.triggered.connect(self.mainwin.close)
        self.feedAddBtn.clicked.connect(self.add_rss)
        self.feedDeleteBtn.clicked.connect(self.del_rss)
        self.feedList.itemClicked.connect(self.show_feeds)
        self.entryListWidget.itemClicked.connect(self.show_feed)
        self.entryListWidget.doubleClicked.connect(self.open_browser)
        self.updateAllBtn.clicked.connect(self.update_all_urls)

        QtCore.QMetaObject.connectSlotsByName(self.mainwin)

    def retranslate_ui(self):
        self.mainwin.setWindowTitle(QtCore.QCoreApplication.translate(
            'MainWindow', 'RSS Feed Reader'))
        self.feedAddBtn.setText(QtCore.QCoreApplication.translate(
            'MainWindow', 'Add'))
        self.feedDeleteBtn.setText(QtCore.QCoreApplication.translate(
            'MainWindow', 'Delete'))
        self.updateAllBtn.setText(QtCore.QCoreApplication.translate(
            'MainWindow', 'Update All'))
        self.menuEdit.setTitle(QtCore.QCoreApplication.translate(
            'MainWindow', 'Edit'))
        self.actionNew_RSS_Feed.setText(
                QtCore.QCoreApplication.translate('MainWindow', 'Add'))
        self.actionQuit.setText(
                QtCore.QCoreApplication.translate('MainWindow', 'Quit'))

    def generate_hash(self, *args):
        return hashlib.md5(''.join(args).encode('utf-8')).hexdigest()

    def add_rss(self):
        dia = Dialog()
        if dia.res and bool(dia.linkEdit.text()):
            self.update_url(dia.linkEdit.text().strip())
            self.show_urls()

    def del_rss(self):
        if self.entryListWidget.currentItem() is None:
            self.db.delete_url(self.feedList.currentRow())
            self.show_urls()
            self.entryListWidget.clear()
            self.textBrowser.clear()

        else:
            self.db.delete_feed(
                    self.db.get_feeds(
                        self.feedList.currentRow()
                        )[self.entryListWidget.currentRow()][1])
            self.textBrowser.clear()
            self.show_feeds()

    def show_urls(self):
        self.feedList.clear()
        for x in reversed(self.db.get_urls()):
            item = QtWidgets.QListWidgetItem()
            item.setText(x[2])
            self.feedList.addItem(item)

    def show_feeds(self):
        self.entryListWidget.clear()
        for feed in sorted(self.db.get_feeds(id=self.feedList.currentRow()),
                           key=lambda x: x[-1]):
            item = QtWidgets.QListWidgetItem()
            item.setData(1, feed[1])
            item.setText(base64.b64decode(feed[2]).decode('utf-8'))
            if feed[-1]:
                item.setBackground(
                        QtGui.QColor().fromRgb(0x2b2b2b))

            self.entryListWidget.addItem(item)

    def show_feed(self):
        self.textBrowser.clear()
        feed = self.db.get_feed(self.entryListWidget.currentItem().data(1))
        date = base64.b64decode(feed[3]).decode('utf-8')
        try:
            try:
                date = datetime.datetime.strptime(date, r'%a, %d %B %Y %H:%M:%S %z')
                date = date.astimezone().strftime(r'%Y-%m-%d %H:%M:%S')
                raise

            except ValueError:
                pass

            try:
                date = datetime.datetime.strptime(date, r'%a, %d %B %Y %H:%M:%S %Z')
                date = date.astimezone().strftime(r'%Y-%m-%d %H:%M:%S')
                raise

            except ValueError:
                pass

        except Exception:
            pass

        else:
            pass

        self.textBrowser.append('Title: <a href="{0}">{1}</a><br><br>Date: {2}<br><br>{3}<br>'.format(
                        base64.b64decode(feed[4]).decode('utf-8').replace('"', r'\"'),
                        base64.b64decode(feed[2]).decode('utf-8'),
                        date,
                        base64.b64decode(feed[-2]).decode('utf-8')))

        self.db.set_read(feed[1])
        self.entryListWidget.currentItem().setBackground(
                QtGui.QColor().fromRgb(0x2b2b2b))

    def resource_handler(self, type, obj):
        if type == QtGui.QTextDocument.ImageResource:
            pix = QtGui.QPixmap()
            img = asyncio.get_event_loop().run_until_complete(self.get_page(obj.url()))
            if img is not None:
                pix.loadFromData(img)

            return QtGui.QPixmap('error.png') if pix.isNull() else pix

        return QtGui.QPixmap('error.png')

    def open_browser(self):
        link = self.db.get_feed(self.entryListWidget.currentItem().data(1))[4]
        webbrowser.open_new_tab(base64.b64decode(link).decode())

    @staticmethod
    async def get_page(url: str):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers={
                    'User-Agent': 'Mozilla/5.0 (X11; OpenBSD i386)'
                }, timeout=aiohttp.ClientTimeout(total=0)) as response:
                    if response.status == 200:
                        return await response.read()

            except aiohttp.ClientError:
                pass

            return None

    async def read_rss(self, url: str, source: str):
        try:
            tree = xml.etree.ElementTree.ElementTree(
                    xml.etree.ElementTree.fromstring(source))

        except xml.etree.ElementTree.ParseError:
            return False

        root = tree.getroot()
        title = root[0].find('title')
        if title is not None:
            title = title.text

        id = self.db.insert_url(url, title)

        for item in root.iterfind('channel/item'):
            title = str(item.findtext('title'))
            pubdate = str(item.findtext('pubDate'))
            link = str(item.findtext('link'))
            description = str(item.findtext('description'))
            hash = self.generate_hash(title, pubdate, link, description)
            self.db.insert_feed(id, hash, title, pubdate, link,
                                description, self.db.get_feed_raed(hash))

        return True

    def show_error(self, text: str):
        msg = QtWidgets.QMessageBox()

        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText('Error')
        msg.setInformativeText('An error has occurred.\n\n' + text)
        msg.setWindowTitle('Error')

        msg.exec()

    def update_all_urls(self):
        for item in self.db.get_urls():
            self.update_url(item[1])

    def update_url(self, url: str):
        page = asyncio.get_event_loop().run_until_complete(self.get_page(url))
        if page is None:
            self.show_error(url)
            return False

        ret = asyncio.get_event_loop().run_until_complete(
                self.read_rss(url, page.decode()))

        if not ret:
            self.show_error(url)
            return False

        return True


if __name__ == '__main__':
    main = Main()
