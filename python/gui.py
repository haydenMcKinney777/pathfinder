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

        #containers
        self.scenes = []
        self.views = []
        self.cells = []

        self.scene = Scene(self)
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.setMouseTracking(True)

        #control panel
        self.run_button = QPushButton("Run Pathfinder")
        self.clear_grid_button = QPushButton("Reset Grid")
        self.dijkstra_checkbox = QCheckBox("Dijkstra")
        self.astar_checkbox = QCheckBox("A*")
        self.dfs_checkbox = QCheckBox("DFS")
        self.bfs_checkbox = QCheckBox("BFS")

        #main layout setup
        self.main_layout = QtWidgets.QVBoxLayout(self)

        #top control area
        control_layout = QtWidgets.QVBoxLayout()
        control_layout.addWidget(self.view)
        control_layout.addWidget(self.dijkstra_checkbox)
        control_layout.addWidget(self.astar_checkbox)
        control_layout.addWidget(self.dfs_checkbox)
        control_layout.addWidget(self.bfs_checkbox)
        control_layout.addWidget(self.run_button)
        control_layout.addWidget(self.clear_grid_button)
        self.main_layout.addLayout(control_layout)

        self.run_button.setFixedSize(100,60)
        self.clear_grid_button.setFixedSize(100,60)

        #separate container to hold multiple algorithm grids
        self.grid_display = QtWidgets.QWidget()
        self.grid_display_layout = QtWidgets.QGridLayout(self.grid_display)
        self.main_layout.addWidget(self.grid_display)

        self.run_button.clicked.connect(self.run_algorithm)

        #initial grid creation
        cell_size = 50
        self.start_cell = None
        self.goal_cell = None
        self.is_drawing = False

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
        if self.dijkstra_checkbox.isChecked():
            selected_algorithms.append(("Dijkstra", pathfinder.dijkstra_run))

        if self.astar_checkbox.isChecked():
            selected_algorithms.append(("A*", pathfinder.astar_run))

        if self.dfs_checkbox.isChecked():
            selected_algorithms.append(("DFS", pathfinder.dfs_run))

        if self.bfs_checkbox.isChecked():
            selected_algorithms.append(("BFS", pathfinder.bfs_run))

        if not selected_algorithms:
            print("Algorithm must be selected.\n")
            return

        self.scenes.clear()
        self.views.clear() 
        
        self.view.setParent(None)

        #clear old grid views
        for i in reversed(range(self.grid_display_layout.count())):
            widget = self.grid_display_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        for algorithm, run_function in selected_algorithms:
            scene = Scene(self)
            view = QtWidgets.QGraphicsView(scene)
            self.scenes.append(scene)
            self.views.append(view)

            cell_size = 50
            for row in range(20):
                for col in range(20):
                    cell = Cell(col * cell_size, row * cell_size, cell_size, row, col, self)
                    #copy current grid’s walls/start/goal
                    state = self.cells[row][col].state
                    cell.setState(state)
                    scene.addItem(cell)

        self.arrange_views()

    def arrange_views(self):
        count = len(self.views)
        grid_layout = QtWidgets.QGridLayout()
        scale_factor = {1: 1.0, 2: 0.7, 3: 0.6}.get(count, 0.5)     #based on the number of algorithms selected to run, we scale each view

        for i in reversed(range(self.grid_display_layout.count())):
            widget = self.grid_display_latout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        for i, view in enumerate(self.views):
            view.resetTransform()
            view.scale(scale_factor, scale_factor)
            self.grid_display_layout.addWidget(view, i // 2, i % 2)

        self.setLayout(grid_layout)
      
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