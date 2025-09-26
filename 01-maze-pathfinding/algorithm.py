import heapq
import time
from collections import deque
from graphics import *


def heuristic(cell, goal):
    """
    Computes the heuristic distance between two points using Manhattan distance.
    """
    return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])


def A_star(graph, start, goal, pathMap, ax2, ax3):
    start_time = time.time()
    open_set = []
    heapq.heappush(open_set, (0, start))
    came_from = {}
    g_score = {cell: float('inf') for cell in graph}
    g_score[start] = 0
    f_score = {cell: float('inf') for cell in graph}
    f_score[start] = heuristic(start, goal)
    expanded_nodes = 0
    pathMap[start[0], start[1]] = 70

    while open_set:
        _, current = heapq.heappop(open_set)
        expanded_nodes += 1

        if current == goal:
            path = reconstruct_path(
                came_from, current, pathMap, ax3, "A* Final Path", start, goal)
            elapsed_time = time.time() - start_time
            return len(path), expanded_nodes, elapsed_time

        for neighbor in graph[current]:
            tentative_g_score = g_score[current] + 1
            if tentative_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = tentative_g_score + \
                    heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score[neighbor], neighbor))
                pathMap[neighbor[0], neighbor[1]] = 70  # Mark as searching
                update_visualization(pathMap, ax2, "A* Search Progress")

    elapsed_time = time.time() - start_time
    return None, expanded_nodes, elapsed_time


def bfs(graph, start, goal, pathMap, ax2, ax3):
    start_time = time.time()
    queue = deque([start])
    came_from = {start: None}
    expanded_nodes = 0
    pathMap[start[0], start[1]] = 70

    while queue:
        current = queue.popleft()
        expanded_nodes += 1

        if current == goal:
            path = reconstruct_path(
                came_from, current, pathMap, ax3, "BFS Final Path", start, goal)
            elapsed_time = time.time() - start_time
            return len(path), expanded_nodes, elapsed_time

        for neighbor in graph[current]:
            if neighbor not in came_from:
                came_from[neighbor] = current
                queue.append(neighbor)
                pathMap[neighbor[0], neighbor[1]] = 70  # Mark as searching
                update_visualization(pathMap, ax2, "BFS Search Progress")

    return None, expanded_nodes, time.time() - start_time


def dfs(graph, start, goal, pathMap, ax2, ax3):
    start_time = time.time()
    stack = [start]
    came_from = {start: None}
    expanded_nodes = 0
    pathMap[start[0], start[1]] = 70

    while stack:
        current = stack.pop()
        expanded_nodes += 1

        if current == goal:
            path = reconstruct_path(
                came_from, current, pathMap, ax3, "DFS Final Path", start, goal)
            elapsed_time = time.time() - start_time
            return len(path), expanded_nodes, elapsed_time

        for neighbor in graph[current]:
            if neighbor not in came_from:
                came_from[neighbor] = current
                stack.append(neighbor)
                pathMap[neighbor[0], neighbor[1]] = 70  # Mark as searching
                update_visualization(pathMap, ax2, "DFS Search Progress")

    elapsed_time = time.time() - start_time
    return None, expanded_nodes, elapsed_time


def greedy(graph, start, goal, pathMap, ax2, ax3):
    start_time = time.time()
    open_set = []
    heapq.heappush(open_set, (heuristic(start, goal), start))
    came_from = {start: None}
    expanded_nodes = 0
    pathMap[start[0], start[1]] = 70

    while open_set:
        _, current = heapq.heappop(open_set)
        expanded_nodes += 1

        if current == goal:
            path = reconstruct_path(
                came_from, current, pathMap, ax3, "Greedy Final Path", start, goal)
            elapsed_time = time.time() - start_time
            return len(path), expanded_nodes, elapsed_time

        for neighbor in graph[current]:
            if neighbor not in came_from:
                came_from[neighbor] = current
                heapq.heappush(open_set, (heuristic(neighbor, goal), neighbor))
                pathMap[neighbor[0], neighbor[1]] = 70  # Mark as searching
                update_visualization(pathMap, ax2, "Greedy Search Progress")

    elapsed_time = time.time() - start_time
    return None, expanded_nodes, elapsed_time


def depth_limited_search(graph, current, goal, depth, came_from, pathMap, ax2, expanded_nodes):
    if depth == 0:
        return None
    if current == goal:
        return [current]
    for neighbor in graph[current]:
        if neighbor not in came_from:
            came_from[neighbor] = current
            expanded_nodes += 1
            pathMap[neighbor[0], neighbor[1]] = 70  # Mark as searching
            update_visualization(pathMap, ax2, "IDS Search Progress")
            result = depth_limited_search(
                graph, neighbor, goal, depth - 1, came_from, pathMap, ax2, expanded_nodes)
            if result is not None:
                return [current] + result
    return None


def iterative_deepening_search(graph, start, goal, pathMap, ax2, ax3):
    start_time = time.time()
    depth = 0
    expanded_nodes = 0
    pathMap[start[0], start[1]] = 70

    while True:
        came_from = {start: None}
        expanded_nodes += 1
        result = depth_limited_search(
            graph, start, goal, depth, came_from, pathMap, ax2, expanded_nodes)
        if result is not None:
            path = reconstruct_path(
                came_from, goal, pathMap, ax3, "IDS Final Path", start, goal)
            elapsed_time = time.time() - start_time
            return len(path), expanded_nodes, elapsed_time
        depth += 1
