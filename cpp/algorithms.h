#pragma once
#include <vector>

int dijkstra_run(const std::vector<std::vector<int>>&grid, int start_row, int start_col, int goal_row, int goal_col);
int astar_run(const std::vector<std::vector<int>>&grid, int start_row, int start_col, int goal_row, int goal_col);
int dfs_run(const std::vector<std::vector<int>>&grid, int start_row, int start_col, int goal_row, int goal_col);
int bfs_run(const std::vector<std::vector<int>>&grid, int start_row, int start_col, int goal_row, int goal_col);