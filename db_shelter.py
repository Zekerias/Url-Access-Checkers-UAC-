import sqlite3
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import (QListWidgetItem)
from PyQt6.QtCore import Qt, QThread, QObject
import aiohttp
import asyncio


conn = sqlite3.connect('data.db')
cur = conn.cursor()
loop = asyncio.get_event_loop()

def create_db():
    cur.execute("""CREATE TABLE IF NOT EXISTS sites(
                    url TEXT);
                """)
    conn.commit()


def insert_site_list(site_line, site_list):
    url = site_line.text()
    if url != '':
        site_list.addItem(url)
        cur.execute(f"""INSERT INTO sites(url)
                         VALUES('{url}');""")
        conn.commit()
    else:
        print('Wrong word')
        return


def refresh_site_list(site_list):
    site_list.clear()
    cur.execute("""SELECT url FROM sites;""")
    data_sql = cur.fetchall()
    for row in data_sql:
        data_row = list(row)
        for item_text in data_row:
            print(item_text)
            item = QListWidgetItem(item_text)
            item.setBackground(loop.run_until_complete(requests_bool(item_text)))
            item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter)
            site_list.addItem(item)


def delete_site_from_list(site_list):
    listItems = site_list.selectedItems()
    if not listItems:
        return
    if listItems != '':
        for item in listItems:
            site_list.takeItem(site_list.row(item))
            url = item.text()
            cur.execute("""SELECT url FROM sites;""")
            cur.execute(f"DELETE FROM sites WHERE url = '{url}';")
            conn.commit()
    else:
        return


async def requests_bool(url):
    try:
        await aiohttp.ClientSession().get(url)
        print('Success!')
        return QColor('DarkGreen')
    except:
        print('An error has occurred.')
        return QColor('Red')
