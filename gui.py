import sys
import random
from PySide6 import QtWidgets, QtGui

class Cell(QtWidgets.QGraphicsRectItem):
    def __init__(self, x, y, size, row, col):
        super().__init__(x, y, size, size)
        self.row = row
        self.col = col
        self.setPen(QtGui.QPen(QtGui.QColor("black")))
        self.setBrush(QtGui.QBrush(QtGui.QColor("grey")))


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.view)

        cell_size = 50
        for row in range(20):
            for col in range(20):
                cell = Cell(col * cell_size, row * cell_size, cell_size, row, col)
                self.scene.addItem(cell)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = Window()
    window.resize(1200, 1200)
    window.show()

    sys.exit(app.exec())