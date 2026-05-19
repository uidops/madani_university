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
from qrcode_dialog import QrDialog


class Main:
    def __init__(self):
        self.db = DataBase()
        self.app = QtWidgets.QApplication(['rss'])
        self.mainwin = QtWidgets.QMainWindow()

        self.read_color = 0x050505

        self.setup_ui()
        self.retranslate_ui()
        self.mainwin.show()

        self.show_urls()

        self.app.exec()
        self.db.con.close()

    def setup_ui(self):
        self.mainwin.resize(900, 580)

        self.centralwidget = QtWidgets.QWidget(self.mainwin)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.centralwidget)

        self.listView = QtWidgets.QWidget(self.centralwidget)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.listView)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.horizontalLayout_4.addLayout(self.verticalLayout)

        self.progressBar = QtWidgets.QProgressBar(self.listView)
        self.progressBar.setOrientation(QtCore.Qt.Vertical)
        self.horizontalLayout_4.addWidget(self.progressBar)

        self.urlList = QtWidgets.QListWidget(self.listView)
        self.verticalLayout.addWidget(self.urlList)

        self.horizontalLayout = QtWidgets.QHBoxLayout()

        self.feedAddBtn = QtWidgets.QPushButton(self.listView)
        self.horizontalLayout.addWidget(self.feedAddBtn)

        self.feedDeleteBtn = QtWidgets.QPushButton(self.listView)
        self.horizontalLayout.addWidget(self.feedDeleteBtn)

        self.updateAllBtn = QtWidgets.QPushButton(self.listView)
        self.horizontalLayout.addWidget(self.updateAllBtn)

        self.progressBar = QtWidgets.QProgressBar(self.listView)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.verticalLayout.addWidget(self.progressBar)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.feedList = QtWidgets.QListWidget(self.listView)
        self.verticalLayout_2.addWidget(self.feedList)

        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.horizontalLayout_5.addWidget(self.listView)

        self.progressBar = QtWidgets.QProgressBar(self.listView)
        self.progressBar.setOrientation(QtCore.Qt.Horizontal)
        self.verticalLayout_2.addWidget(self.progressBar)

        self.textBrowser = QtWidgets.QTextBrowser(self.listView)
        self.textBrowser.loadResource = self.resource_handler
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.openLinks = self.open_browser
        self.verticalLayout_2.addWidget(self.textBrowser)

        self.mainwin.setCentralWidget(self.centralwidget)

        self.menuBar = QtWidgets.QMenuBar(self.mainwin)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 899, 29))

        self.menuEdit = QtWidgets.QMenu(self.menuBar)
        self.mainwin.setMenuBar(self.menuBar)

        self.actionNew_RSS_Feed = QtWidgets.QAction(self.mainwin)
        self.menuEdit.addAction(self.actionNew_RSS_Feed)

        self.actionQuit = QtWidgets.QAction(self.mainwin)
        self.menuEdit.addAction(self.actionQuit)

        self.menuBar.addAction(self.menuEdit.menuAction())

        # signals
        self.actionNew_RSS_Feed.triggered.connect(self.add_rss)
        self.actionQuit.triggered.connect(self.mainwin.close)

        self.feedAddBtn.clicked.connect(self.add_rss)
        self.feedDeleteBtn.clicked.connect(self.del_rss)
        self.updateAllBtn.clicked.connect(self.update_all_urls)

        self.urlList.itemClicked.connect(self.show_feeds)

        self.feedList.mouseReleaseEvent = self.show_feed
        self.feedList.itemDoubleClicked.connect(self.open_browser)

    def retranslate_ui(self):
        self.mainwin.setWindowTitle('RSS Feed Reader')
        self.feedAddBtn.setText('Add')
        self.feedDeleteBtn.setText('Delete')
        self.updateAllBtn.setText('Update all')
        self.menuEdit.setTitle('Edit')
        self.actionNew_RSS_Feed.setText('Add')
        self.actionQuit.setText('Quit')

    def generate_hash(self, *args):
        return hashlib.md5(''.join(args).encode('utf-8')).hexdigest()

    def add_rss(self):
        dia = Dialog()
        if dia.res and dia.linkEdit.text():
            self.update_url(dia.linkEdit.text().strip())
            self.show_urls()

    def del_rss(self):
        if self.feedList.currentItem() is None:
            self.db.delete_url(self.urlList.currentRow())
            self.show_urls()
            self.feedList.clear()
            self.textBrowser.clear()

        else:
            self.db.delete_feed(
                    self.db.get_feeds(
                        self.urlList.currentRow()
                        )[self.feedList.currentRow()][1])
            self.textBrowser.clear()
            self.show_feeds()

    def show_urls(self):
        self.urlList.clear()
        for x in reversed(self.db.get_urls()):  # x: (id, url, title)
            item = QtWidgets.QListWidgetItem()
            item.setText(x[2])
            self.urlList.addItem(item)

    def show_feeds(self):
        self.feedList.clear()
        # feed: (id, hash, title, pubdate, link, description, read)
        for feed in sorted(self.db.get_feeds(id=self.urlList.currentRow()),
                           key=lambda x: x[-1]):
            item = QtWidgets.QListWidgetItem()
            item.setData(1, feed[1])
            item.setText(base64.b64decode(feed[2]).decode('utf-8'))
            if feed[-1]:
                item.setBackground(
                        QtGui.QColor().fromRgb(self.read_color))

            self.feedList.addItem(item)

    def show_feed(self, event):
        feed = self.db.get_feed(self.feedList.currentItem().data(1))
        if event.button() == QtCore.Qt.RightButton:
            QrDialog(base64.b64decode(feed[4]).decode('utf-8'))
            return

        date = base64.b64decode(feed[3]).decode('utf-8')
        try:
            try:
                date = datetime.datetime.strptime(date, r'%a, %d %B %Y %H:%M:%S %z').astimezone().strftime(r'%Y-%m-%d %H:%M:%S')
                raise

            except ValueError:
                pass

            try:
                date = datetime.datetime.strptime(date, r'%a, %d %B %Y %H:%M:%S %Z').astimezone().strftime(r'%Y-%m-%d %H:%M:%S')
                raise

            except ValueError:
                pass

        except Exception:
            pass

        else:
            pass

        self.textBrowser.clear()
        self.textBrowser.append('Title: <a href="{0}">{1}</a><br><br>Date: {2}<br><br>{3}<br>'.format(
                        base64.b64decode(feed[4]).decode('utf-8').replace('"', r'\"'),
                        base64.b64decode(feed[2]).decode('utf-8'),
                        date,
                        base64.b64decode(feed[-2]).decode('utf-8')))

        self.db.set_read(feed[1])
        self.feedList.currentItem().setBackground(
                QtGui.QColor().fromRgb(self.read_color))

    def resource_handler(self, typ, obj):
        if typ == QtGui.QTextDocument.ImageResource:
            pix = QtGui.QPixmap()
            img = asyncio.new_event_loop().run_until_complete(
                    self.get_page(obj.url()))
            if img is not None:
                pix.loadFromData(img)

            return QtGui.QPixmap('error.png') if pix.isNull() else pix

        return QtGui.QPixmap('error.png')

    def open_browser(self):
        link = self.db.get_feed(self.feedList.currentItem().data(1))[4]
        webbrowser.open_new_tab(base64.b64decode(link).decode())

    @staticmethod
    async def get_page(url: str):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers={'User-Agent': 'Mozilla/5.0 (X11; OpenBSD i386)'},
                                       timeout=aiohttp.ClientTimeout(total=0)) as response:
                    if response.status == 200:
                        return await response.read()

            except aiohttp.ClientError:
                pass

            return None

    async def parse_rss(self, url: str, source: str):
        try:
            tree = xml.etree.ElementTree.ElementTree(
                    xml.etree.ElementTree.fromstring(source))

        except xml.etree.ElementTree.ParseError:
            return False

        root = tree.getroot()
        title = root[0].find('title')
        if title is not None:
            title = title.text

        url_id = self.db.insert_url(url, title)
        for item in root.iterfind('channel/item'):
            title = str(item.findtext('title'))
            pubdate = str(item.findtext('pubDate'))
            link = str(item.findtext('link'))
            description = str(item.findtext('description'))
            digest = self.generate_hash(title, pubdate, link, description)
            self.db.insert_feed(url_id, digest, title, pubdate, link,
                                description, self.db.get_feed_raed(digest))

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
        page = asyncio.new_event_loop().run_until_complete(
                self.get_page(url))
        if page is None:
            self.show_error('URL: ' + url)
            return False

        ret = asyncio.new_event_loop().run_until_complete(
                self.parse_rss(url, page.decode()))

        if not ret:
            self.show_error('Response data is not XML\n\nURL: ' + url)
            return False

        return True


if __name__ == '__main__':
    Main()
