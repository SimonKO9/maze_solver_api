import typing as t

from app.maze.models import parse_grid_size, Maze, parse_coords, Coords, Path


def maze_to_matrix(maze: Maze):
    grid = parse_grid_size(maze.gridSize)
    matrix = [["0" for _ in range(grid[0])] for _ in range(grid[1])]
    for wall in maze.walls:
        wall_coords = parse_coords(wall)
        matrix[wall_coords[1]][wall_coords[0]] = "1"

    return matrix


def print_maze(maze: Maze) -> str:
    matrix = maze_to_matrix(maze)
    return '\n'.join([''.join(row) for row in matrix])


def print_coords(coords: Coords) -> str:
    x = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[coords[0]]
    y = coords[1] + 1
    return f"{x}{y}"


def print_path(path: Path) -> str:
    return ' '.join([print_coords(c) for c in path])
