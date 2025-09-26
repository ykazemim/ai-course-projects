import matplotlib.pyplot as plt
import random
from typing import List, Tuple
import math


def read_dataset(filename: str) -> List[Tuple[float, float]]:
    """
    Reads a .tsp file and extracts city coordinates.

    Args:
        filename (str): Name of the file (without path or extension).

    Returns:
        List[Tuple[float, float]]: List of city coordinates as (x, y) tuples.
    """
    with open("data/" + filename + ".tsp", 'r') as f:
        cities: List[Tuple[float, float]] = []
        for line in f:
            parts = line.split()
            if len(parts) == 3 and ":" not in parts:
                cities.append((float(parts[1]), float(parts[2])))
    return cities


def create_distance_matrix(cities: List[Tuple[float, float]]) -> List[List[float]]:
    """
    Builds an N×N matrix of pairwise Euclidean distances.

    Args:
        cities (List[Tuple[float, float]]): List of city coordinates.

    Returns:
        List[List[float]]: Distance matrix where element [i][j] is the distance from city i to city j.
    """
    n = len(cities)
    # Initialize an n x n matrix with zeros
    matrix = [[0.0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dx = cities[i][0] - cities[j][0]
                dy = cities[i][1] - cities[j][1]
                # Calculate Euclidean distance
                matrix[i][j] = math.hypot(dx, dy)
    return matrix


def calculate_route_distance(
    route: List[int], distance_matrix: List[List[float]]
) -> float:
    """
    Sums distances along the closed tour defined by `route`.

    Args:
        route (List[int]): A permutation representing a tour.
        distance_matrix (List[List[float]]): Precomputed pairwise distance matrix.

    Returns:
        float: Total distance of the closed tour.
    """
    distance = 0.0
    for i in range(len(route)):
        from_city = route[i]
        to_city = route[(i + 1) % len(route)]
        distance += distance_matrix[from_city][
            to_city
        ]  # Calculate distance from current city to next city
    return distance


def fitness(route: List[int], distance_matrix: List[List[float]]) -> float:
    """
    Defines fitness as the inverse of the total route distance.

    Args:
        route (List[int]): A permutation representing a tour.
        distance_matrix (List[List[float]]): Precomputed pairwise distance matrix.

    Returns:
        float: Fitness value, higher is better.
    """

    total_distance = calculate_route_distance(route, distance_matrix)
    return 1.0 / total_distance if total_distance > 0 else float('inf')


def generate_initial_population(
    num_individuals: int, num_cities: int
) -> List[List[int]]:
    """
    Generates `num_individuals` random tours over `num_cities` cities.

    Args:
        num_individuals (int): Number of individuals in the population.
        num_cities (int): Number of cities in each tour.

    Returns:
        List[List[int]]: Initial population, a list of random permutations.
    """

    population = []
    for _ in range(num_individuals):
        individual = list(range(num_cities)) # Create a list of city indices
        random.shuffle(individual) # Shuffle the list to create a random tour
        population.append(individual)
    return population


def plot_route(cities, route=None):
    plt.figure(figsize=(10, 6))

    if route is not None:
        for i in range(len(route)):
            start = cities[route[i]]
            end = cities[route[(i + 1) % len(route)]]
            plt.plot([start[0], end[0]], [start[1], end[1]], 'r-')

        # Highlight start and end nodes
        start_node = cities[route[0]]
        end_node = cities[route[-1]]
        plt.scatter(*start_node, c='blue', s=150, marker='*', label='Start')
        # plt.text(start_node[0] + 0.1, start_node[1] + 0.02, "Start", fontsize=9, color='green')

        plt.scatter(*end_node, c='red', s=150, marker='X', label='End')
        # plt.text(end_node[0] + 0.1, end_node[1] + 0.02, "End", fontsize=9, color='red')

    # Plot all cities and their indices
    xs = [pt[0] for pt in cities]
    ys = [pt[1] for pt in cities]
    plt.scatter(xs, ys, c='blue', marker='o')
    for i, (x, y) in enumerate(cities):
        plt.text(x + 0.02, y + 0.02, str(i), fontsize=9, color='black')

    plt.title("2D Map of Points")
    plt.xlabel("Longitude")
    plt.ylabel("Latitude")
    plt.grid(True)
    plt.legend()
    plt.show()
