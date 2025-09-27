import sys
import pathfinder       #the link to C++ code
from PySide6 import QtWidgets, QtGui, QtCore

class Cell(QtWidgets.QGraphicsRectItem):
    def __init__(self, x, y, size, row, col, window):
        super().__init__(x, y, size, size)
        self.setAcceptedMouseButtons(QtCore.Qt.AllButtons)
        self.setAcceptHoverEvents(True)
        self.window = window    #give the cell a pointer to the window so it knows about the grid
        
        #keep track of cell position on grid
        self.row = row
        self.col = col

        #define color attributes of cell (outline, fill color)
        self.setPen(QtGui.QPen(QtGui.QColor("black")))
        self.setState("empty")  #default state

    def setState(self, state: str):
        """Set the logical state and update the visual color accordingly."""
        self.state = state
        color = {"wall":"black", "start":"green", "goal":"red"}.get(state, "grey")
        self.setBrush(QtGui.QBrush(QtGui.QColor(color)))

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.window.is_drawing = True   #only set is_drawing on left button presses - we only want to draw walls
            
            if self.state == "wall":
                self.setState("empty")
            elif self.state == "start":
                self.window.start_cell = None
                self.setState("wall")
            elif self.state == "goal":
                self.window.goal_cell = None
                self.setState("wall")
            else:
                self.setState("wall")

        elif event.button() == QtCore.Qt.RightButton:
            if self.state == "goal":
                return
            if self.window.start_cell is None:  #no start yet in grid
                self.setState("start")
                self.window.start_cell = self
            else:
                self.window.start_cell.setState("empty")
                self.setState("start")
                self.window.start_cell = self

        elif event.button() == QtCore.Qt.MiddleButton:
            if self.state == "start":
                return
            if self.window.goal_cell is None:  #no goal yet in grid
                self.setState("goal")
                self.window.goal_cell = self
            else:
                self.window.goal_cell.setState("empty")
                self.setState("goal")
                self.window.goal_cell = self

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:  #if the button that was released over a cell was left mouse, set is_drawing False
            self.window.is_drawing = False


class Scene(QtWidgets.QGraphicsScene):
    def __init__(self, window):
        super().__init__()
        self.window = window

    def mouseMoveEvent(self, event):
        if self.window.is_drawing:
            pos = event.scenePos()
            for item in self.items(pos):
                if isinstance(item, Cell) and item.state not in ("start", "goal"):
                    item.setState("wall")
                    break
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton:
            self.window.is_drawing = False
        super().mouseReleaseEvent(event)

class Window(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.scene = Scene(self)
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.setMouseTracking(True)

        self.start_cell = None
        self.goal_cell = None
        self.is_drawing = False

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.view)

        #create 20x20 grid of 50px cells
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

    #TEST TO MAKE SURE PYTHON CAN TALK WITH CPP FILES:
    print("Calling C++ from Python:")

    print("Dijkstra:", pathfinder.dijkstra_run(0, 10))
    print("A*:", pathfinder.astar_run(0, 10))
    print("DFS:", pathfinder.dfs_run(0, 10))
    print("BFS:", pathfinder.bfs_run(0, 10))

    sys.exit(app.exec())