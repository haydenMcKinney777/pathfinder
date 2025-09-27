/*
HAYDEN MCKINNEY - 09/27/2025
bindings.cpp is the "binding file" that tells Python how to access the C++ code.
*/

#include <pybind11/pybind11.h>
#include "algorithms.h"

namespace py = pybind11;

PYBIND11_MODULE(pathfinder, m) {
    m.def("dijkstra_run", &dijkstra_run, "Run C++ Dijkstra algorithm");
    m.def("astar_run", &astar_run, "Run C++ A* algorithm");
    m.def("dfs_run", &dfs_run, "Run C++ DFS algorithm");
    m.def("bfs_run", &bfs_run, "Run C++ BFS algorithm");
}