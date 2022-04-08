from app.maze.maze_solver import MazeSolver
from app.maze.models import CreateMazePayload, Steps
from uuid import uuid4
from app.maze.utils import *
import typing as t


class MazeNotFoundException(Exception):
    pass


class MazeWithoutSolutionException(Exception):
    pass


class MazeService:
    _mazes: t.Dict[str, list[Maze]]

    def __init__(self) -> None:
        self._mazes = {}

    def create_maze(self, payload: CreateMazePayload, owner: str) -> Maze:
        maze = Maze(entrance=payload.entrance, gridSize=payload.gridSize, walls=payload.walls, id=str(uuid4()))
        if owner in self._mazes:
            self._mazes[owner].append(maze)
        else:
            self._mazes[owner] = [maze]
        return maze

    def get_maze(self, owner: str, maze_id: str) -> t.Optional[Maze]:
        return next((maze for maze in self.get_mazes(owner) if maze.id == maze_id), None)

    def get_mazes(self, owner: str) -> t.List[Maze]:
        if owner in self._mazes:
            return self._mazes[owner]
        else:
            return []

    def get_maze_solution(self, owner: str, maze_id: str, steps: Steps) -> t.Optional[Path]:
        maze = self.get_maze(owner, maze_id)
        if maze is None:
            raise MazeNotFoundException()
        solver = MazeSolver(maze)

        if steps == Steps.min:
            path = solver.get_shortest_path()
        elif steps == Steps.max:
            path = solver.get_longest_path()
        else:
            raise NotImplementedError("Steps must be either min or max")

        if path is not None:
            return [print_coords(x) for x in path]
        else:
            raise MazeWithoutSolutionException()
