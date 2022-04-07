from app.maze.models import *
from app.maze.utils import *
import typing as t


class MazeException(Exception):
    def __init__(self, message):
        self.message = message


class MazeSolver:
    _width: int
    _height: int
    _entrance: t.Tuple[int, int]
    _width: int

    def __init__(self, maze: Maze) -> None:
        self._width, self._height = parse_grid_size(maze.gridSize)
        self._matrix = maze_to_matrix(maze)
        self._entrance = parse_coords(maze.entrance)
        self._solve()

    def _solve(self):
        paths = []

        def dfs(v, visited):
            visited.append(v)
            for neighbour in self._get_neighbours(v):
                if neighbour not in visited:
                    dfs(neighbour, visited.copy())

            if v[1] == self._height - 1:  # append path if leads to exit (exit located at bottom row)
                paths.append(visited)

        dfs(self._entrance, [])

        exits = set([c[-1] for c in paths])
        if len(exits) > 1:
            exits_pretty = [print_coords(e) for e in exits]
            exits_pretty.sort()
            print_exits = ", ".join(exits_pretty)
            raise MazeException(f"Multiple exits detected: {print_exits}.")
        if len(exits) == 0:
            raise MazeException("No exit found.")

        paths.sort(key=lambda x: len(x))
        self._paths = paths

    def get_paths(self):
        return self._paths

    def get_shortest_path(self) -> t.Optional[Path]:
        if len(self._paths) > 0:
            return self._paths[0]
        else:
            return None

    def get_longest_path(self) -> t.Optional[Path]:
        if len(self._paths) > 0:
            return self._paths[-1]
        else:
            return None

    def _get_exits(self) -> t.List[Coords]:
        return

    def _get_neighbours(self, node: Coords) -> t.List[Coords]:
        candidates = [
            (node[0] - 1, node[1]),
            (node[0] + 1, node[1]),
            (node[0], node[1] - 1),
            (node[0], node[1] + 1)
        ]
        return [
            c for c in candidates
            if 0 <= c[0] < self._width and 0 <= c[1] < self._height  # within bounds
               and self._matrix[c[1]][c[0]] == "0"  # and is not wall
        ]
