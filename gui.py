import sys
from PySide6 import QtWidgets, QtGui, QtCore

class Cell(QtWidgets.QGraphicsRectItem):
    def __init__(self, x, y, size, row, col, window):
        super().__init__(x, y, size, size)
        self.setAcceptedMouseButtons(QtCore.Qt.AllButtons)
        self.window = window    #give the cell a pointer to the window so the cell has knowledge on what cells exist
        
        #keep track of cell position on grid
        self.row = row
        self.col = col

        #define color attributes of cell (outline, fill color)
        self.setPen(QtGui.QPen(QtGui.QColor("black")))
        self.setColor("grey")

        #set the default state of the cell (empty, wall, start, goal)
        self.state = "empty"

    def setColor(self, color):
        self.setBrush(QtGui.QBrush(QtGui.QColor(color)))
        if(color == "black"):
            self.state = "wall"
        elif(color == "green"):
            self.state = "start"
        elif(color == "red"):
            self.state = "goal"
        else:
            self.state = "empty"


    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            if(self.state == "wall"):
                self.setColor("grey")
            else:
                self.setColor("black")

        elif event.button() == QtCore.Qt.RightButton:
            if(self.state == "goal"):
                return
            elif(self.window.start_cell is None): #if there does not already exist a starting cell
                self.setColor("green")
                self.window.start_cell = self
            else:
                self.window.start_cell.setColor("grey")
                self.setColor("green")
                self.window.start_cell = self

        elif event.button() == QtCore.Qt.MiddleButton:
            if(self.state == "start"):
                return
            elif(self.window.goal_cell is None):  #if there does not already exist a goal cell
                self.setColor("red")
                self.window.goal_cell = self
            else:
                self.window.goal_cell.setColor("grey")
                self.setColor("red")
                self.window.goal_cell = self


class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.scene = QtWidgets.QGraphicsScene()
        self.view = QtWidgets.QGraphicsView(self.scene)

        self.start_cell = None
        self.goal_cell = None

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.view)

        #create 10x10 grid of size 50 cells
        cell_size = 50
        for row in range(20):
            for col in range(20):
                cell = Cell(col * cell_size, row * cell_size, cell_size, row, col, self)
                self.scene.addItem(cell)

if __name__ == "__main__":
    app = QtWidgets.QApplication([])

    window = Window()
    window.resize(1200, 1200)
    window.show()

    sys.exit(app.exec())