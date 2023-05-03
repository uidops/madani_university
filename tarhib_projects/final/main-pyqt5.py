#!/usr/bin/env python

from PyQt5 import QtCore, QtWidgets, QtGui
import xml.etree.ElementTree
import asyncio
import aiohttp
import os
import pickle
import webbrowser


class Dialog:
    def __init__(self):
        self.dialog = QtWidgets.QDialog()
        self.res = False
        self.setup_ui()
        self.dialog.exec_()

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
        self.rss_urls, self.data = [], {}

        self.app = QtWidgets.QApplication(['rss'])
        self.MainWindow = QtWidgets.QMainWindow()

        self.setup_ui()
        self.MainWindow.show()

        self.read_urls()
        self.update_ui()

        self.app.exec_()

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

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName('verticalLayout')

        # self.feedLabel = QtWidgets.QLabel(self.listView)
        # self.feedLabel.setObjectName('feedLabel')
        # self.verticalLayout.addWidget(self.feedLabel)

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
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.feedProgressBar = QtWidgets.QProgressBar(self.listView)
        self.feedProgressBar.setAutoFillBackground(False)
        self.feedProgressBar.setProperty('value', 0)
        self.feedProgressBar.setTextVisible(False)
        self.feedProgressBar.setOrientation(QtCore.Qt.Horizontal)
        self.feedProgressBar.setTextDirection(
                QtWidgets.QProgressBar.TopToBottom)
        self.feedProgressBar.setObjectName('feedProgressBar')
        self.verticalLayout.addWidget(self.feedProgressBar)
        self.horizontalLayout_4.addLayout(self.verticalLayout)

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

        self.textBrowser = QtWidgets.QTextBrowser(self.articleView)
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
        self.menuBar.addAction(self.menuEdit.menuAction())

        self.retranslate_ui()

        self.actionNew_RSS_Feed.triggered.connect(self.add_rss)
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
        #self.feedLabel.setText(QtCore.QCoreApplication.translate(
        #    'MainWindow', 'Rss Feeds'))
        self.feedAddBtn.setText(QtCore.QCoreApplication.translate(
            'MainWindow', 'Add'))
        self.feedDeleteBtn.setText(QtCore.QCoreApplication.translate(
            'MainWindow', 'Delete'))
        self.updateAllBtn.setText(QtCore.QCoreApplication.translate(
            'MainWindow', 'Update All'))
        self.menuEdit.setTitle(QtCore.QCoreApplication.translate(
            'MainWindow', 'Edit'))
        self.actionNew_RSS_Feed.setText(
                QtCore.QCoreApplication.translate('MainWindow', 'Add url'))

    def add_rss(self):
        dia = Dialog()
        if dia.res and bool(dia.linkEdit.text()):
            if self.update_url(dia.linkEdit.text().strip()):
                self.rss_urls.append(dia.linkEdit.text().strip())

            self.write_urls()
            self.update_ui()

    def del_rss(self):
        i = self.feedList.currentRow()
        self.data.pop(tuple(self.data.keys())[i])
        self.rss_urls.pop(i)

        self.write_urls()
        self.update_ui()

    def update_ui(self):
        self.feedList.clear()
        for items in self.data.values():
            item = QtWidgets.QListWidgetItem()
            item.setText(items[0])
            self.feedList.addItem(item)

    def show_feeds(self):
        self.entryListWidget.clear()
        for feed in tuple(self.data.items())[self.feedList.currentRow()][1][1]:
            item = QtWidgets.QListWidgetItem()
            item.setText(feed['title'])
            if feed['read']:
                item.setBackground(
                        QtGui.QColor().fromRgb(0x2b2b2b))

            self.entryListWidget.addItem(item)

    def show_feed(self):
        a, b = self.feedList.currentRow(), self.entryListWidget.currentRow()
        self.textBrowser.clear()
        self.textBrowser.append('Title: {0}\n\nDate:{1}\n\n{2}\n'.format(
                        tuple(self.data.items())[a][1][1][b]['title'],
                        tuple(self.data.items())[a][1][1][b]['pubDate'],
                        tuple(self.data.items())[a][1][1][b]['description']))

        self.data = list(self.data.items())
        self.data[a][1][1][b]['read'] = True
        self.data = dict(self.data)
        self.entryListWidget.currentItem().setBackground(
                QtGui.QColor().fromRgb(0x2b2b2b))
        self.write_urls()

    def open_browser(self):
        a, b = self.feedList.currentRow(), self.entryListWidget.currentRow()
        webbrowser.open(tuple(self.data.items())[a][1][1][b]['link'])

    def read_urls(self):
        self.rss_urls.clear()
        try:
            with open(self.url_file, 'r', encoding='utf-8') as f:
                for url in f:
                    self.rss_urls.append(url.strip())
        except FileNotFoundError:
            return

        try:
            with open(self.db_file, 'rb') as f:
                try:
                    self.data = pickle.load(f)
                except Exception:
                    self.update_all_urls()
        except FileNotFoundError:
            return

    def write_urls(self):
        if not os.path.isdir('feeds/'):
            os.mkdir('feeds/')

        with open(self.url_file, 'w', encoding='utf-8') as f:
            for url in self.rss_urls:
                f.write(url + '\n')

        with open(self.db_file, 'wb') as f:
            pickle.dump(self.data, f)

    @staticmethod
    async def get_page(url: str):
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(url, headers={
                    'User-Agent': 'Mozilla/5.0 (X11; OpenBSD i386)'
                }, timeout=aiohttp.ClientTimeout(total=0)) as response:
                    if response.status == 200:
                        return await response.text()

            except aiohttp.ClientError:
                pass

            return None

    async def read_rss(self, url: str, source: str):
        try:
            tree = xml.etree.ElementTree.ElementTree(
                    xml.etree.ElementTree.fromstring(source))
        except xml.etree.ElementTree.ParseError:
            return None

        root = tree.getroot()

        title = root[0].find('title')
        if title is not None:
            title = title.text

        items = list()
        for i in root.iterfind('channel/item'):
            data = dict()
            data['title'] = i.findtext('title')
            data['pubDate'] = i.findtext('pubDate')
            data['link'] = i.findtext('link')
            data['description'] = i.findtext('description')
            data['read'] = False

            if url in self.data and \
                    (data['title'], True) in \
                    map(lambda x: (x['title'], x['read']), self.data[url][1]):
                data['read'] = True

            items.append(data)

        return title, items

    def update_all_urls(self):
        for url in self.rss_urls:
            self.update_url(url)

        self.write_urls()

    def show_error(self, text: str):
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Critical)
        msg.setText('Error')
        msg.setInformativeText('An error has occurred.\n\n' + text)
        msg.setWindowTitle('Error')
        msg.exec_()

    def update_url(self, url: str):
        page = asyncio.get_event_loop().run_until_complete(self.get_page(url))
        if page is None:
            self.show_error(url)
            return False

        item = asyncio.get_event_loop().run_until_complete(
                self.read_rss(url, page))

        if item is None:
            self.show_error(url)
            return False

        self.data[url] = item
        return True


if __name__ == '__main__':
    main = MainWindow()
