#include <iostream>
#include "algorithms.h"
#include <vector>

int dijkstra_run(const std::vector<std::vector<int>>&grid, int start_row, int start_col, int goal_row, int goal_col) {
    std::cout << "Dijkstra run called\n";
    std::cout << "start row:" << " start_row" << "\nstart col:" << " start_col" << std::endl;
    std::cout << "goal row:" << " goal_row" << "\ngoal col:" << " goal_col" << std::endl;
    return 42;
}

int astar_run(const std::vector<std::vector<int>>&grid, int start_row, int start_col, int goal_row, int goal_col) {
    std::cout << "Astar run called\n";
    std::cout << "start row:" << " start_row" << "\nstart col:" << " start_col" << std::endl;
    std::cout << "goal row:" << " goal_row" << "\ngoal col:" << " goal_col" << std::endl;
    return 43;
}

int dfs_run(const std::vector<std::vector<int>>&grid, int start_row, int start_col, int goal_row, int goal_col) {
    std::cout << "dfs run called\n";
    std::cout << "start row:" << " start_row" << "\nstart col:" << " start_col" << std::endl;
    std::cout << "goal row:" << " goal_row" << "\ngoal col:" << " goal_col" << std::endl;
    return 44;
}

int bfs_run(const std::vector<std::vector<int>>&grid, int start_row, int start_col, int goal_row, int goal_col) {
    std::cout << "bfs run called\n";
    std::cout << "start row:" << " start_row" << "\nstart col:" << " start_col" << std::endl;
    std::cout << "goal row:" << " goal_row" << "\ngoal col:" << " goal_col" << std::endl;
    return 45;
}