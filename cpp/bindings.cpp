/*
HAYDEN MCKINNEY - 09/27/2025
bindings.cpp is the "binding file" that tells Python how to access the C++ code.
*/

#include <pybind11/pybind11.h>
#include "algorithms.h"
#include <vector>
#include <pybind11/stl.h>   //enables automatic conversion of Python lists <-> std::vector


namespace py = pybind11;

PYBIND11_MODULE(pathfinder, m) {
    m.def("dijkstra_run", &dijkstra_run, "Run C++ Dijkstra algorithm",
      py::arg("grid"), py::arg("start_row"), py::arg("start_col"),
      py::arg("goal_row"), py::arg("goal_col"));

    m.def("astar_run", &astar_run, "Run C++ Astar algorithm",
      py::arg("grid"), py::arg("start_row"), py::arg("start_col"),
      py::arg("goal_row"), py::arg("goal_col"));

    m.def("dfs_run", &dfs_run, "Run C++ DFS algorithm",
      py::arg("grid"), py::arg("start_row"), py::arg("start_col"),
      py::arg("goal_row"), py::arg("goal_col"));

    m.def("bfs_run", &bfs_run, "Run C++ BFS algorithm",
      py::arg("grid"), py::arg("start_row"), py::arg("start_col"),
      py::arg("goal_row"), py::arg("goal_col"));
}