🧭 Pathfinding Visualizer (Python + C++ via PyBind11)

This project is a cross language pathfinding visualizer that connects a Python GUI to C++ algorithms using PyBind11.

The GUI allows users to draw walls, set start and goal nodes, and run multiple pathfinding algorithms (Dijkstra, A*, DFS, BFS) side by side, each running in its own grid visualization.

⚙️ Features

Interactive 20×20 grid where you can:

Left click: Draw or erase walls

Right click: Set the start node

Middle click: Set the goal node

Run multiple algorithms simultaneously, each displayed in its own grid.

C++ back-end provides algorithm performance and Python-friendly bindings via PyBind11.

Scalable layout that automatically adjusts grid sizes based on selected algorithms.


Requirements

Python 3.9+ (must match the .pyd build target)

CMake (for compiling the C++ extension)

Visual Studio Build Tools (MSVC compiler)

PyBind11 (Python–C++ bindings)

PySide6 (GUI framework)


SETUP INSTRUCTIONS
  1. Clone the repo
  2. Create/activate a virtual environment
       python -m venv .venv
       .\.venv\Scripts\activate
  3. Install python dependencies:
       pip install -r requirements.txt
  4. Build the C++ Extension
      mkdir build
      cd build
      cmake .. -DCMAKE_BUILD_TYPE=Release
      cmake --build . --config Release
  5. Launch the GUI!
     cd python
     python gui.py
