from PyQt6.QtWidgets import (
    QMainWindow,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsEllipseItem,
    QGraphicsTextItem,
    QMenu,
    QDialog,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QMessageBox,
    QLabel,
    QVBoxLayout,
)
from PyQt6.QtGui import QPen
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFontMetricsF, QFont
from avl_tree import AVLTree, Grade
import re

pattern = r"[А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+ [А-ЯЁ][а-яё]+"
pattern2 = (
    r"(0[1-9]|[12][0-9]|3[01]) (янв|фев|мар|апр|май|июн|июл|авг|сен|окт|ноя|дек) \d{4}"
)


class AVLGraphicsView(QGraphicsView):
    def __init__(self, tree, main_window, table):
        super().__init__()
        self.tree = tree
        self.table = table
        self.main_window = main_window
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        self.draw_tree()

    def draw_tree(self):
        self.scene.clear()
        if self.tree._root:
            self._draw_node(self.tree._root, 400, 50, 200)

    def _draw_node(self, node, x, y, offset):
        radius = 25
        ellipse = QGraphicsEllipseItem(x - radius, y - radius, radius * 2, radius * 2)
        self.scene.addItem(ellipse)

        font = QFont()
        font.setPointSize(8)

        key_str = str(node._key)
        metrics = QFontMetricsF(font)
        max_width = radius * 3

        if metrics.horizontalAdvance(key_str) > max_width:
            while (
                metrics.horizontalAdvance(key_str + "…") > max_width
                and len(key_str) > 1
            ):
                key_str = key_str[:-1]
            key_str += "…"

        key_text = QGraphicsTextItem(key_str)
        key_text.setFont(font)
        key_text.setTextWidth(radius * 2)
        key_text.setPos(x - radius + 4, y - radius + 4)
        self.scene.addItem(key_text)

        indices = []
        cur = node.get_list()._head
        while cur:
            indices.append(str(cur._data))
            cur = cur._next
        indices_str = ", ".join(indices)

        list_font = QFont()
        list_font.setPointSize(7)

        list_text = QGraphicsTextItem(f"[{indices_str}]")
        list_text.setFont(list_font)
        list_text.setTextWidth(radius * 2 + 10)
        list_text.setPos(x - radius, y + radius + 2)
        self.scene.addItem(list_text)

        # Рекурсивно рисуем потомков
        if node._left:
            self.scene.addLine(
                x, y + radius, x - offset, y + 100 - radius, QPen(Qt.GlobalColor.black)
            )
            self._draw_node(node._left, x - offset, y + 100, offset / 2)

        if node._right:
            self.scene.addLine(
                x, y + radius, x + offset, y + 100 - radius, QPen(Qt.GlobalColor.black)
            )
            self._draw_node(node._right, x + offset, y + 100, offset / 2)


class AVLWindow(QMainWindow):
    def __init__(self, tree, main_window, table):
        super().__init__()
        self.setWindowTitle("AVL дерево")
        self.setGeometry(100, 100, 1000, 700)
        self.view = AVLGraphicsView(tree, main_window, table)
        self.setCentralWidget(self.view)
