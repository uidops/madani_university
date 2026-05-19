from typing import List, Tuple
import sqlcipher3 as sqlite3
import base64


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

    def get_urls(self) -> List[Tuple[int, str, str]]:
        res = self.cur.execute('SELECT * FROM rss_urls ORDER BY id DESC;')
        return res.fetchall()

    def get_url_by_id(self, id: int) -> str:
        res = self.cur.execute('SELECT url FROM rss_urls WHERE '
                               f'id={id};')
        url = res.fetchall()
        return url[0][0] if any(url) else ''

    def get_id_by_url(self, url: str) -> int:
        res = self.cur.execute('SELECT id FROM rss_urls WHERE '
                               f"url='{url}';")
        id = res.fetchall()
        return id[0][0] if any(id) else -1

    def insert_url(self, url: str, title: str) -> int:
        id = self.get_id_by_url(url)
        if id != -1:
            return id

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

    def get_feeds(self, id: int = -1) -> List[Tuple[int, str, str, str, str, str, int]]:
        query = 'SELECT * FROM feeds ORDER BY id DESC;'
        if id >= 0:
            query = f'SELECT * FROM feeds WHERE id={id} ORDER BY id DESC;'

        res = self.cur.execute(query)
        return res.fetchall()

    def get_feed(self, hash: str) -> Tuple[int, str, str, str, str, str, str, int]:
        res = self.cur.execute('SELECT * FROM feeds WHERE '
                               f"hash='{hash}';")

        return res.fetchall()[0]

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
        read = int(read)

        self.cur.execute('INSERT INTO feeds VALUES ('
                         f"{id}, '{hash}', '{title}', "
                         f"'{pubdate}', '{link}', "
                         f"'{description}', {read});")

        self.con.commit()

    def set_read(self, hash: str):
        self.cur.execute('UPDATE feeds SET '
                         f'read=1 WHERE '
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

