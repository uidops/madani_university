#!/usr/bin/env python

from PyQt5 import QtCore, QtWidgets, QtGui
from typing import List, Tuple
import sqlcipher3 as sqlite3
import xml.etree.ElementTree
import asyncio
import aiohttp
import requests
import base64
import datetime
import hashlib
import webbrowser


class Dialog:
    def __init__(self):
        self.dialog = QtWidgets.QDialog()
        self.res = False
        self.setup_ui()
        self.dialog.exec()

    def setup_ui(self):
        self.dialog.setObjectName('Dialog')
        self.dialog.resize(400, 70)

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.dialog)
        self.horizontalLayout.setObjectName('horizontalLayout')

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName('verticalLayout')

        self.linkEdit = QtWidgets.QLineEdit(self.dialog)
        self.linkEdit.setObjectName('linkEdit')

        self.verticalLayout.addWidget(self.linkEdit)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.buttonBox = QtWidgets.QDialogButtonBox(self.dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Vertical)
        self.buttonBox.setStandardButtons(
                QtWidgets.QDialogButtonBox.Cancel |
                QtWidgets.QDialogButtonBox.Ok)

        self.buttonBox.setObjectName('buttonBox')
        self.horizontalLayout.addWidget(self.buttonBox)

        self.retranslate_ui()

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)
        QtCore.QMetaObject.connectSlotsByName(self.dialog)

    def retranslate_ui(self):
        self.dialog.setWindowTitle(QtCore.QCoreApplication.translate(
            'Dialog', 'New RSS Feed'))
        self.linkEdit.setPlaceholderText(QtCore.QCoreApplication.translate(
            'Dialog', 'http://example.com/feed.rss'))

    def accept(self):
        self.res = True
        self.dialog.close()

    def reject(self):
        self.res = False
        self.dialog.close()


class MainWindow:
    def __init__(self):
        self.url_file, self.db_file = 'feeds/urls', 'feeds/db'

        self.db = DataBase()
        self.app = QtWidgets.QApplication(['rss'])
        self.MainWindow = QtWidgets.QMainWindow()

        self.setup_ui()
        self.MainWindow.show()

        # self.read_urls()
        self.update_ui()

        self.app.exec()
        self.db.con.close()

    def setup_ui(self):
        self.MainWindow.setObjectName('MainWindow')
        self.MainWindow.resize(899, 579)

        self.centralwidget = QtWidgets.QWidget(self.MainWindow)
        self.centralwidget.setObjectName('centralwidget')
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_5.setObjectName('horizontalLayout_5')

        self.listView = QtWidgets.QWidget(self.centralwidget)
        self.listView.setObjectName('listView')
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.listView)
        self.horizontalLayout_4.setObjectName('horizontalLayout_4')

        self.progressBar_1 = QtWidgets.QProgressBar(self.listView)
        self.progressBar_1.setAutoFillBackground(False)
        self.progressBar_1.setProperty('value', 0)
        self.progressBar_1.setTextVisible(False)
        self.progressBar_1.setOrientation(QtCore.Qt.Vertical)
        self.progressBar_1.setTextDirection(
                QtWidgets.QProgressBar.TopToBottom)
        self.progressBar_1.setObjectName('progressBar_1')

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.horizontalLayout_4.addWidget(self.progressBar_1)
        self.verticalLayout.setObjectName('verticalLayout')

        self.feedList = QtWidgets.QListWidget(self.listView)
        self.feedList.setObjectName('feedList')
        self.verticalLayout.addWidget(self.feedList)

        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName('horizontalLayout')
        self.feedAddBtn = QtWidgets.QPushButton(self.listView)
        self.feedAddBtn.setObjectName('feedAddBtn')

        self.horizontalLayout.addWidget(self.feedAddBtn)
        self.feedDeleteBtn = QtWidgets.QPushButton(self.listView)
        self.feedDeleteBtn.setObjectName('feedDeleteBtn')
        self.horizontalLayout.addWidget(self.feedDeleteBtn)

        self.updateAllBtn = QtWidgets.QPushButton(self.listView)
        self.updateAllBtn.setObjectName('updateAllBtn')
        self.horizontalLayout.addWidget(self.updateAllBtn)

        self.progressBar_1 = QtWidgets.QProgressBar(self.listView)
        self.progressBar_1.setAutoFillBackground(False)
        self.progressBar_1.setProperty('value', 0)
        self.progressBar_1.setTextVisible(False)
        self.progressBar_1.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar_1.setTextDirection(
                QtWidgets.QProgressBar.TopToBottom)
        self.progressBar_1.setObjectName('progressBar_1')
        self.verticalLayout.addWidget(self.progressBar_1)
        #  self.verticalLayout.addLayout(self.verticalLayout)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName('verticalLayout_2')

        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName('horizontalLayout_2')
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)

        self.entryListWidget = QtWidgets.QListWidget(self.listView)
        self.entryListWidget.setObjectName('entryListWidget')
        self.verticalLayout_2.addWidget(self.entryListWidget)
        self.horizontalLayout_4.addLayout(self.verticalLayout_2)
        self.horizontalLayout_5.addWidget(self.listView)

        self.articleView = QtWidgets.QWidget(self.centralwidget)
        self.articleView.setEnabled(True)
        self.articleView.setObjectName('articleView')
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.articleView)
        self.verticalLayout_3.setContentsMargins(-1, 0, 9, -1)
        self.verticalLayout_3.setObjectName('verticalLayout_3')

        self.progressBar_2 = QtWidgets.QProgressBar(self.listView)
        self.progressBar_2.setAutoFillBackground(False)
        self.progressBar_2.setProperty('value', 0)
        self.progressBar_2.setTextVisible(False)
        self.progressBar_2.setOrientation(QtCore.Qt.Horizontal)
        self.progressBar_2.setTextDirection(
                QtWidgets.QProgressBar.TopToBottom)
        self.progressBar_2.setObjectName('progressBar_2')
        self.verticalLayout_2.addWidget(self.progressBar_2)

        self.textBrowser = QtWidgets.QTextBrowser(self.articleView)
        self.textBrowser.loadResource = self.resource_handler
        self.textBrowser.setOpenExternalLinks(True)
        self.textBrowser.setObjectName('textBrowser')
        self.verticalLayout_2.addWidget(self.textBrowser)

        self.horizontalLayout_5.addWidget(self.articleView)
        self.MainWindow.setCentralWidget(self.centralwidget)

        self.statusBar = QtWidgets.QStatusBar(self.MainWindow)
        self.statusBar.setObjectName('statusBar')
        self.MainWindow.setStatusBar(self.statusBar)

        self.menuBar = QtWidgets.QMenuBar(self.MainWindow)
        self.menuBar.setGeometry(QtCore.QRect(0, 0, 899, 29))
        self.menuBar.setObjectName('menuBar')

        self.menuEdit = QtWidgets.QMenu(self.menuBar)
        self.menuEdit.setObjectName('menuEdit')

        self.MainWindow.setMenuBar(self.menuBar)
        self.actionNew_RSS_Feed = QtWidgets.QAction(self.MainWindow)
        self.actionNew_RSS_Feed.setObjectName('actionNew_RSS_Feed')
        self.menuEdit.addAction(self.actionNew_RSS_Feed)

        self.actionQuit = QtWidgets.QAction(self.MainWindow)
        self.actionQuit.setObjectName('actionQuit')
        self.menuEdit.addAction(self.actionQuit)

        self.menuBar.addAction(self.menuEdit.menuAction())

        self.retranslate_ui()

        self.actionNew_RSS_Feed.triggered.connect(self.add_rss)
        self.actionQuit.triggered.connect(self.MainWindow.close)
        self.feedAddBtn.clicked.connect(self.add_rss)
        self.feedDeleteBtn.clicked.connect(self.del_rss)
        self.feedList.itemClicked.connect(self.show_feeds)
        self.entryListWidget.itemClicked.connect(self.show_feed)
        self.entryListWidget.doubleClicked.connect(self.open_browser)
        self.updateAllBtn.clicked.connect(self.update_all_urls)

        QtCore.QMetaObject.connectSlotsByName(self.MainWindow)

    def retranslate_ui(self):
        self.MainWindow.setWindowTitle(QtCore.QCoreApplication.translate(
            'MainWindow', 'RSS Feed Reader'))
        #  self.feedLabel.setText(QtCore.QCoreApplication.translate(
        #      'MainWindow', 'Rss Feeds'))
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
        return hashlib.sha256(''.join(args).encode('utf-8')).hexdigest()

    def add_rss(self):
        dia = Dialog()
        if dia.res and bool(dia.linkEdit.text()):
            self.update_url(dia.linkEdit.text().strip())
            self.update_ui()

    def del_rss(self):
        if self.entryListWidget.currentItem() is None:
            self.db.delete_url(self.feedList.currentRow())
            self.update_ui()
            self.entryListWidget.clear()
            self.textBrowser.clear()

        else:
            self.db.delete_feed(
                    self.db.get_feeds(
                        self.feedList.currentRow()
                        )[self.entryListWidget.currentRow()][1])
            self.textBrowser.clear()
            self.show_feeds()

        # self.db.delete_url(self.feedList.currentRow())
        # self.update_ui()
        # self.entryListWidget.clear()
        # self.textBrowser.clear()

    def update_ui(self):
        self.feedList.clear()
        for x in reversed(self.db.get_urls()):
            item = QtWidgets.QListWidgetItem()
            item.setText(x[2])  # title
            self.feedList.addItem(item)

    def show_feeds(self):
        self.entryListWidget.clear()
        for feed in self.db.get_feeds(id=self.feedList.currentRow()):
            item = QtWidgets.QListWidgetItem()
            item.setText(base64.b64decode(feed[2]).decode('utf-8'))  # title
            if feed[-1]:  # status
                item.setBackground(
                        QtGui.QColor().fromRgb(0x2b2b2b))

            self.entryListWidget.addItem(item)

    def show_feed(self):
        self.textBrowser.clear()

        feed = self.db.get_feeds(id=self.feedList.currentRow())[self.entryListWidget.currentRow()]
        date = base64.b64decode(feed[3]).decode('utf-8')  # pubdate
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
                        base64.b64decode(feed[4]).decode('utf-8').replace('"', r'\"'),  # url
                        base64.b64decode(feed[2]).decode('utf-8'),  # title
                        date,
                        base64.b64decode(feed[-2]).decode('utf-8')))  # description

        self.db.set_read(feed[1])  # hash
        self.entryListWidget.currentItem().setBackground(
                QtGui.QColor().fromRgb(0x2b2b2b))
        # self.write_urls()

    def resource_handler(self, type, obj):
        image = QtGui.QPixmap()
        image.loadFromData(asyncio.get_event_loop().run_until_complete(self.get_page(obj.url())))
        return image

    def open_browser(self):
        webbrowser.open(self.db.get_feeds(id=self.feedList.currentRow())[self.entryListWidget.currentRow()][4])  # link

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

    def update_all_urls(self):
        for item in self.db.get_urls():
            self.update_url(item[1])

    def show_error(self, text: str):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText('Error')
        msg.setInformativeText('An error has occurred.\n\n' + text)
        msg.setWindowTitle('Error')
        msg.exec()

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


class DataBase:
    def __init__(self):
        self.con = sqlite3.connect('database.db')
        self.cur = self.con.cursor()
        self.__setup()

    def __setup(self):
        self.cur.execute('pragma key="___$2sfdkljsdkljfki3__$32";')
        res = self.cur.execute('SELECT name FROM sqlite_master WHERE '
                               "type='table' AND "
                               "name='rss_urls';")

        if not any(res.fetchall()):
            self.cur.execute('CREATE TABLE rss_urls'
                             '(id, url, title);')

        res = self.cur.execute('SELECT name FROM sqlite_master WHERE '
                               "type='table' AND "
                               "name='feeds';")

        if not any(res.fetchall()):
            self.cur.execute('CREATE TABLE feeds'
                             '(id, hash, title, pubdate, link, description, read);')

    def get_urls(self) -> List[Tuple[int, str]]:
        res = self.cur.execute('SELECT * FROM rss_urls ORDER BY id DESC;')
        return res.fetchall()

    def get_url_by_id(self, id: int) -> str:
        res = self.cur.execute('SELECT url FROM rss_urls WHERE '
                               f'id={id};')
        url = res.fetchall()
        return url[0] if any(url) else ''

    def get_id_by_url(self, url: str) -> int:
        res = self.cur.execute('SELECT id FROM rss_urls WHERE '
                               f"url='{url}';")
        id = res.fetchall()
        return id[0] if any(id) else -1

    def exists_url(self, url: str) -> True:
        res = self.cur.execute('SELECT id FROM rss_urls WHERE '
                               f"url='{url}'")
        return True if any(res.fetchall()) else False

    def insert_url(self, url: str, title: str) -> int:
        if self.exists_url(url):
            return

        urls = self.get_urls()
        id = urls[0][0] + 1 if any(urls) else 0
        self.cur.execute('INSERT INTO rss_urls VALUES '
                         f"({id}, '{url}', '{title}');")

        self.con.commit()
        return id

    def delete_url(self, id: int) -> None:
        if not self.get_url_by_id(id):
            return

        self.cur.execute('DELETE FROM rss_urls WHERE '
                         f"id={id};")
        self.delete_feeds(id)

        self.con.commit()
        self.fix_database()

    def get_feeds(self, id: int = -1) -> List[Tuple[int, str, str, str, str, int]]:
        query = 'SELECT * FROM feeds ORDER BY id DESC;'
        if id >= 0:
            query = f'SELECT * FROM feeds WHERE id={id} ORDER BY id DESC;'

        res = self.cur.execute(query)
        return res.fetchall()

    def get_feed_raed(self, hash: str) -> bool:
        res = self.cur.execute('SELECT read FROM feeds WHERE '
                               f"hash='{hash}';")
        read = res.fetchall()
        return True if any(read) and read[0] else False

    def exists_feed(self, hash: str) -> bool:
        res = self.cur.execute('SELECT id FROM feeds WHERE '
                               f"hash='{hash}';")
        return True if any(res.fetchall()) else False

    def insert_feed(self, id: int, hash: str, title: str, pubdate: str,
                    link: str, description: str, read: bool) -> None:
        if self.exists_feed(hash):
            return

        title = base64.b64encode(title.encode('utf-8')).decode()
        pubdate = base64.b64encode(pubdate.encode('utf-8')).decode()
        link = base64.b64encode(link.encode('utf-8')).decode()
        description = base64.b64encode(description.encode('utf-8')).decode()

        self.cur.execute('INSERT INTO feeds VALUES ('
                         f"{id}, '{hash}', '{title}', "
                         f"'{pubdate}', '{link}', "
                         f"'{description}', {read});")

        self.con.commit()

    def set_read(self, hash: str):
        self.cur.execute('UPDATE feeds SET '
                         f'read=True WHERE '
                         f"hash='{hash}';")

        self.con.commit()

    def delete_feed(self, hash: str) -> bool:
        if not self.exists_feed(hash):
            return

        self.cur.execute('DELETE FROM feeds WHERE '
                         f"hash='{hash}';")

        self.con.commit()
        self.fix_database()

    def delete_feeds(self, id: int) -> bool:
        self.cur.execute('DELETE FROM feeds WHERE '
                         f"id={id};")

        self.con.commit()
        self.fix_database()

    def fix_database(self) -> None:
        urls = self.get_urls()
        max_id = len(urls) - 1

        for column in urls:
            self.cur.execute('UPDATE rss_urls SET '
                             f'id={max_id} WHERE '
                             f'id={column[0]};')

            self.cur.execute('UPDATE feeds SET '
                             f'id={max_id} WHERE '
                             f'id={column[0]};')

            max_id -= 1

        self.con.commit()


if __name__ == '__main__':
    main = MainWindow()
