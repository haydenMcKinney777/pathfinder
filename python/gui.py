import sys
import pathfinder       #the link to C++ code
import concurrent.futures
import copy
from PySide6 import QtWidgets, QtGui, QtCore
from PySide6.QtWidgets import QPushButton, QCheckBox

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

        self.scenes = []   #each algorithm gets its own scene
        self.views = []    #each scene gets its own QGraphicsView
        self.cells = []

        self.scene = Scene(self)        #primary scene for initial interaction
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.setMouseTracking(True)

        self.start_cell = None
        self.goal_cell = None
        self.is_drawing = False

        self.num_grids = 0    #default number of grids. if multiple algorithms get selected to run, multiple grids will appear on screen 

        #widgets
        self.run_button = QPushButton("Run Pathfinder", self)
        self.run_button.setFixedSize(100,60)

        self.clear_grid_button = QPushButton("Reset Grid", self)
        self.clear_grid_button.setFixedSize(100,60)

        self.dijkstra_checkbox = QCheckBox(text="Dijkstra")
        self.astar_checkbox = QCheckBox(text="A*")
        self.dfs_checkbox = QCheckBox(text="DFS")
        self.bfs_checkbox = QCheckBox(text="BFS")

        #add widgets to layout
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.view)
        layout.addWidget(self.dijkstra_checkbox)
        layout.addWidget(self.astar_checkbox)
        layout.addWidget(self.dfs_checkbox)
        layout.addWidget(self.bfs_checkbox)
        layout.addWidget(self.run_button)
        layout.addWidget(self.clear_grid_button)

        self.run_button.clicked.connect(self.run_algorithm)

        #create 20x20 grid of 50px cells
        cell_size = 50

        for row in range(20):
            row_cells = []
            for col in range(20):
                cell = Cell(col * cell_size, row * cell_size, cell_size, row, col, self)
                self.scene.addItem(cell)
                row_cells.append(cell)
            self.cells.append(row_cells)

    def run_algorithm(self):
        if not self.start_cell or not self.goal_cell:
            print("Start and goal must be set before running an algorithm.\n")
            return

        selected_algorithms = []

        start_row, start_col = self.start_cell.row, self.start_cell.col
        goal_row, goal_col = self.goal_cell.row, self.goal_cell.col

        """
        UNDERSTAND THIS CODE DIRECTLY UNDER THIS COMMENT.
        IMPLEMENT THE RUN_ALGORITHM FUNCTION IN PYTHON AND UNDERSTAND IT
        UNDERSTAND THE CHANGES WE MADE IN BINDINGS.CPP, ALGORITHMS.H, AND ALGORITHMS.CPP
        UNDERSTAND WHY WE HAD TO REBUILD AFTER MAKING THE ABOVE CHANGES
        """
        #create a snapshot of the current grid state at function run time to send to C++
        grid = []
        for row in range(20):
            row_data = []
            for col in range(20):
                cell = self.cells[row][col]
                if cell.state == "wall":
                    row_data.append(1)
                else:
                    row_data.append(0)
            grid.append(row_data)

        if self.dijkstra_checkbox.isChecked():
            selected_algorithms.append(("Dijkstra", pathfinder.dijkstra_run))

        if self.astar_checkbox.isChecked():
            selected_algorithms.append(("A*", pathfinder.astar_run))

        if self.dfs_checkbox.isChecked():
            selected_algorithms.append(("DFS", pathfinder.dfs_run))

        if self.bfs_checkbox.isChecked():
            selected_algorithms.append(("BFS", pathfinder.bfs_run))

        self.scenes.clear()
        self.views.clear() 

        for algorithm, run_function in selected_algorithms:
            scene = Scene(self)
            view = QtWidgets.QGraphicsView(scene)
            self.scenes.append(scene)
            self.views.append(view)

        self.arrange_views()

    def arrange_views(self):
        count = len(self.views)
        grid_layout = QtWidgets.QGridLayout()
        scale_factor = {1: 1.0, 2: 0.7, 3: 0.6}.get(count, 0.5)     #based on the number of algorithms selected to run, we scale each view

        for i, view in enumerate(self.views):
            view.resetTransform()
            view.scale(scale_factor, scale_factor)
            layout.addWidget(view, i // 2, i % 2)
      
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