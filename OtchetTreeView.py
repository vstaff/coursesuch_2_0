from PyQt6.QtWidgets import (
    QMainWindow,
    QGraphicsView,
    QGraphicsScene,
    QGraphicsEllipseItem,
    QGraphicsTextItem,
)
from PyQt6.QtGui import QPen
from PyQt6.QtCore import Qt


class OtchetGraphicsView(QGraphicsView):
    def __init__(self, avlt, tree, arr):
        super().__init__()
        self.tree = tree
        self.avlt = avlt
        self.arr = arr
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        self.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.draw_tree()

    def draw_tree(self):
        self.scene.clear()
        if self.tree._root:
            self._draw_node(self.tree._root, 400, 50, 200)

    def _draw_node(self, node, x, y, offset):
        radius = 30
        ellipse = QGraphicsEllipseItem(x - radius, y - radius, radius * 2, radius * 2)
        self.scene.addItem(ellipse)

        key_text = QGraphicsTextItem(str(node.key))
        key_text.setPos(x - radius / 2, y - radius / 2)
        self.scene.addItem(key_text)

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


class AVL2Window(QMainWindow):
    def __init__(self, tree, arr2):
        super().__init__()
        self.setWindowTitle("AVL дерево")
        self.setGeometry(100, 100, 1000, 700)
        self.view = OtchetGraphicsView(tree, tree, arr2)
        self.setCentralWidget(self.view)
