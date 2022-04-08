import typing as t
from uuid import uuid4

from app.maze.maze_solver import MazeSolver
from app.maze.models import CreateMazePayload, Steps, Maze, Path
from app.maze.utils import print_coords
from app.persistence import schemas
from app.persistence.persistence import Persistence


class MazeNotFoundException(Exception):
    pass


class MazeWithoutSolutionException(Exception):
    pass


class MazeService:
    def __init__(self, persistence: Persistence) -> None:
        self._persistence = persistence

    def create_maze(self, payload: CreateMazePayload, owner: str) -> Maze:
        maze = Maze(entrance=payload.entrance, gridSize=payload.gridSize,
                    walls=payload.walls, id=str(uuid4()))
        self._persistence.create_maze(
            schemas.Maze(id=maze.id, entrance=maze.entrance, gridSize=maze.gridSize, walls=maze.walls), owner)
        return maze

    def get_maze(self, owner: str, maze_id: str) -> t.Optional[Maze]:
        return next((maze for maze in self.get_mazes(
            owner) if maze.id == maze_id), None)

    def get_mazes(self, owner: str) -> t.List[Maze]:
        return self._persistence.get_mazes_by_username(owner)

    def get_maze_solution(self, owner: str, maze_id: str,
                          steps: Steps) -> t.Optional[t.List[str]]:
        maze = self.get_maze(owner, maze_id)
        if maze is None:
            raise MazeNotFoundException()
        solver = MazeSolver(maze)

        if steps == Steps.MIN:
            path = solver.get_shortest_path()
        elif steps == Steps.MAX:
            path = solver.get_longest_path()
        else:
            raise NotImplementedError("Steps must be either min or max")

        if path is not None:
            return [print_coords(x) for x in path]
        raise MazeWithoutSolutionException()
