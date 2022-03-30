#!/usr/bin/python
# -*- coding:utf-8 -*-

# Url Access Checkers  [UAC]
from PyQt6.QtWidgets import (QWidget, QApplication, QMainWindow, QLabel,
                             QGraphicsDropShadowEffect, QPushButton, QLineEdit, QSizePolicy,
                             QListWidget, QGridLayout)
from PyQt6.QtCore import (Qt, QSize, pyqtSignal, QTimer,QThread)
from PyQt6.QtGui import (QFont, QIcon, QColor, QKeySequence,
                         QShortcut, QMovie, QMouseEvent)
import db_shelter as ds

class Lbel_refresh(QLabel):
    def mouseReleaseEvent(self, QMouseEvent):
        super(QLabel, self).mousePressEvent(QMouseEvent)
        print('refresh')
        mw.movie.start()
        timer = QTimer()
        timer.start(20)
        refresh()
        timer.timeout.connect(lambda: mw.movie.stop())


class Lbel_trash(QLabel):
    def mouseReleaseEvent(self, QMouseEvent):
        super(QLabel, self).mousePressEvent(QMouseEvent)
        mw.movie_1.start()
        delete()
        self.timer = QTimer()
        self.timer.start(200)
        self.timer.timeout.connect(lambda: mw.movie_1.stop())

        print('delete')


class MainWindow(QMainWindow):
    clicked = pyqtSignal(QMouseEvent)

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Url Access Checkers")
        grid = QGridLayout()
        self.setLayout(grid)
        self.setGeometry(600, 30, 700, 1000)
        self.setWindowIcon(QIcon("qt.png"))
        self.setStyleSheet("background: rgba(10, 10, 10, 1)")
        self.font_size = 15

        # Set of widgets with settings

        # Search Field(UNDER CONSTRUCT)
        self.find_line = QLineEdit(self)
        self.find_line.setVisible(True)
        self.find_line.setFont(QFont('Times', self.font_size))
        self.find_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.find_line.setSizePolicy(QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Maximum)

        # Delete button
        self.delete_from_list = Lbel_trash()
        self.delete_from_list.setGeometry(351, 5, 35, 35)
        self.movie_1 = QMovie("world-circle.gif")
        self.movie_1.setScaledSize(QSize(55, 55))
        self.delete_from_list.setMovie(self.movie_1)
        self.movie_1.start()
        self.movie_1.stop()
        self.movie_1.setSpeed(1000)
        self.delete_from_list.setVisible(True)
        self.delete_from_list.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.shortcut_add = QShortcut(QKeySequence(Qt.Key.Key_Delete), self)

        # Refresh button
        self.refresh_list_button = Lbel_refresh()
        self.movie = QMovie("swerik-gif.gif")
        self.movie.setScaledSize(QSize(55, 55))
        self.refresh_list_button.setMovie(self.movie)
        self.movie.start()
        self.movie.stop()
        self.movie.setSpeed(1000)
        self.refresh_list_button.setGeometry(10, 5, 35, 35)
        self.refresh_list_button.setVisible(True)
        self.refresh_list_button.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        self.shortcut_add = QShortcut(QKeySequence(Qt.Key.Key_R), self)
        self.shortcut_add.activated.connect(refresh)

        # Add site field
        self.site_line = QLineEdit(self)
        site_line = self.site_line
        self.site_line.setGeometry(10, 560, 170, 30)
        self.site_line.setVisible(True)
        self.site_line.setFont(QFont('Times', self.font_size))
        self.site_line.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.site_line.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)

        # QListWidget of sites
        self.site_list = QListWidget(self)
        site_list = self.site_list
        self.site_list.setVisible(True)
        self.site_list.setGeometry(0, 40, 400, 510)
        self.site_list.setFont(QFont('Times', self.font_size))
        self.site_list.setFocusPolicy(Qt.FocusPolicy.NoFocus)


        # Add site to list button
        self.add_site_button = QPushButton('+', self)
        self.add_site_button.setFont(QFont('Arial', self.font_size))
        self.add_site_button.setGeometry(280, 560, 30, 30)
        self.add_site_button.setVisible(True)
        self.shadow = QGraphicsDropShadowEffect()
        self.shadow.setColor(QColor("#3F3F3F"))
        self.shadow.setOffset(0, 0)
        self.shadow.setBlurRadius(20)
        self.add_site_button.setGraphicsEffect(self.shadow)
        self.add_site_button.setToolTip('Add new translation')
        self.add_site_button.clicked.connect(insert)
        self.shortcut_add = QShortcut(QKeySequence(Qt.Key.Key_Return), self)
        self.shortcut_add.activated.connect(insert)

        # Layouts
        grid.addWidget(self.refresh_list_button, 0, 0)
        grid.addWidget(self.find_line, 0, 1)
        grid.addWidget(self.delete_from_list, 0, 2)
        grid.addWidget(self.site_list, 1, 0, 2, 3)
        grid.addWidget(self.site_line, 3, 1)
        grid.addWidget(self.add_site_button, 3, 2)
        widget = QWidget()
        self.setCentralWidget(widget)
        widget.setLayout(grid)

        # Styles
        self.find_line.setStyleSheet("border-radius:10px;background: #666666;")

        self.site_line.setStyleSheet(
            """border-radius:10px;box-shadow;background:#666666;selection-background-color: darkgreen;""")

        self.delete_from_list.setStyleSheet('''
        QLabel{
            width:30px;
            height:30px;

            }
        QMovie{
            border-radius:15px;
            boder:2px solid white
        }
        QLabel:pressed{
            backrground-color:black;
            border:2px solid #2a7827;
            }
            ''')

        self.refresh_list_button.setStyleSheet('''
        QLabel{
            border-radius:15px;
            width:30px;
            height:30px;
            border:2px solid #2a7827;
            background-color: rgba( 255, 255, 255, 0% )

            }
        QMovie{
            background-color: rgba( 255, 255, 255, 0% )
            border-radius:15px;
            boder:2px solid white
        }
        QLabel:pressed{
            backrground-color:black;
            border:2px solid #2a7827;
            }
            ''')

        self.site_list.setStyleSheet('''QListWidget{
            color:white;
            border: 2px solid darkgreen;
            border-radius:10px;
            }
            QListWidget:pressed{
            border:2px solid #2a7827;
            }
            QListView::item:selected{
            border-radius:5px;
            color:white;
            background-color:rgba( 255, 255, 255, 0% )
            border : 2px solid white ;
            }
            QScrollBar{
                background:green;border-color:balck solid;
            }''')

        self.add_site_button.setStyleSheet('''
        QPushButton{
            border-radius: 15px;
            border:2px solid #2a7827;
            background:#2a7827;
            margin:5px;
            width:30px;
            height:30px;
            }
        QPushButton:pressed{
            background-color: black;
            border:2px solid #2a7827;
            }
            ''')


# Refunction
def insert():
    ds.insert_site_list(mw.site_line, mw.site_list)
    refresh()


def refresh():
    ds.refresh_site_list(mw.site_list)


def delete():
    ds.delete_site_from_list(mw.site_list)




if __name__ == "__main__":
    import sys

    app = QApplication([])
    mw = MainWindow()
    new_thread = QThread()
    ds.create_db()
    refresh()
    mw.show()

    sys.exit(app.exec())

__Author__ = """Made by: ZekeriasRojoOjo
                Email: Zekeriasrojo@gmail.com
                twitter.com/ZekeriasRojo"""
__Copyright__ = 'Copyright (c) 2022 ZekeriasRojoOjo'
__Version__ = 0.1
