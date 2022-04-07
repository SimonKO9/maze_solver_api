import pytest

from app.maze.maze_solver import MazeSolver, MazeException
from app.maze.models import Maze
from app.maze.utils import print_coords, print_maze


def test_should_find_path__when_single_path_exists():
    maze = Maze(
        entrance="A1",
        gridSize="8x8",
        walls=["C1", "G1", "A2", "C2", "E2", "G2", "C3", "E3", "B4", "C4", "E4", "F4", "G4", "B5", "E5", "B6", "D6",
               "E6", "G6", "H6", "B7", "D7", "G7", "B8"],
        id="test"
    )

    solver = MazeSolver(maze)
    longest_path = solver.get_shortest_path()
    shortest_path = solver.get_longest_path()
    assert [print_coords(c) for c in longest_path] == ["A1", "B1", "B2", "B3", "A3", "A4", "A5", "A6", "A7", "A8"]
    assert shortest_path == longest_path


def test_should_throw__when_no_path_exists():
    maze = Maze(
        entrance="A1",
        gridSize="8x8",
        walls=["C1", "G1", "A2", "C2", "E2", "G2", "C3", "E3", "B4", "C4", "E4", "F4", "G4", "B5", "E5", "B6", "D6",
               "E6", "G6", "H6", "B7", "D7", "G7", "B8", "A8"],
        id="test"
    )

    with pytest.raises(MazeException) as e:
        MazeSolver(maze)

    assert e.value.message == "No exit found."


def test_should_throw__when_multiple_exits_exist():
    maze = Maze(
        entrance="A1",
        gridSize="8x8",
        walls=["G1", "A2", "C2", "E2", "G2", "C3", "E3", "B4", "C4", "E4", "F4", "G4", "B5", "E5", "B6", "D6",
               "E6", "G6", "H6", "B7", "D7", "G7", "B8", "A8"],
        id="test"
    )

    with pytest.raises(MazeException) as e:
        MazeSolver(maze)

    assert e.value.message == "Multiple exits detected: C8, D8, E8, F8, G8, H8."
