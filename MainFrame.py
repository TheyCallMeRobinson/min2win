import os

from MainFrameUI import Ui_MainWindow as MainWindowUI
from game import *

from PyQt5 import QtSvg, QtWidgets
from PyQt5.QtGui import QMouseEvent, QPainter, QStandardItemModel
from PyQt5.QtWidgets import QMainWindow, QItemDelegate, QStyleOptionViewItem
from PyQt5.QtCore import QModelIndex, QRectF, Qt


class MainWindow(QMainWindow, MainWindowUI):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)

        images_dir = os.path.join(os.path.dirname(__file__), 'images')
        self._images = {
            os.path.splitext(f)[0]: QtSvg.QSvgRenderer(os.path.join(images_dir, f))
            for f in os.listdir(images_dir)
        }

        self._game = Game(11, 8)
        self.game_resize(self._game)

        class MyDelegate(QItemDelegate):
            def __init__(self, parent=None, *args):
                QItemDelegate.__init__(self, parent, *args)

            def paint(self, painter: QPainter, option: QStyleOptionViewItem, idx: QModelIndex):
                painter.save()
                self.parent().on_item_paint(idx, painter, option)
                painter.restore()

        self.tableView.setItemDelegate(MyDelegate(self))

        # такие ухищрения, т.к. не предусмотрено сигналов для правой кнопки мыши
        def new_mouse_press_event(e: QMouseEvent) -> None:
            idx = self.tableView.indexAt(e.pos())
            self.on_item_clicked(idx, e)

        self.tableView.mousePressEvent = new_mouse_press_event

        self.restartButton.clicked.connect(self.on_new_game)

    def game_resize(self, game: Game) -> None:
        model = QStandardItemModel(game.get_rows, game.get_columns)
        self.tableView.setModel(model)
        self.update_view()

    def update_view(self):
        self.tableView.viewport().update()

    def on_new_game(self):
        self._game = Game(self._game.get_rows, self._game.get_columns)
        self.game_resize(self._game)
        self.update_view()

    def on_item_paint(self, e: QModelIndex, painter: QPainter, option: QStyleOptionViewItem) -> None:
        item = self._game[e.row(), e.column()]
        if item.value == 1:
            img = self._images['green_circle']
        elif item.value == 2:
            img = self._images['yellow_triangle']
        elif item.value == 3:
            img = self._images['blue_rectangle']
        elif item.value == 4:
            img = self._images['red_star']
        else:
            img = self._images['empty']
        img.render(painter, QRectF(option.rect))

    def on_item_clicked(self, e: QModelIndex, me: QMouseEvent = None) -> None:
        if me.button() == Qt.LeftButton:
            self._game.mouse_click(e.row(), e.column())
            self.minGroupToProceedNumber.display(self._game.get_min_group_size)
            self.lcdNumber.display(self._game.get_score)
            if self._game.check_defeat():
                messagebox = QtWidgets.QMessageBox.question(self, 'You lost!', 'Do you want to restart the game?',
                                                            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if messagebox == QtWidgets.QMessageBox.Yes:
                    self._game.new_game()
                    self.minGroupToProceedNumber.display(self._game.get_min_group_size)
                    self.lcdNumber.display(self._game.get_score)
                else:
                    pass
        self.update_view()
