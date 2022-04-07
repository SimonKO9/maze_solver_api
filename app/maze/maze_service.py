import typing as t

from app.maze.models import Maze, CreateMazePayload
from uuid import uuid4
from app.maze.utils import *


class MazeService:
    _mazes: dict[str, list[Maze]]

    def create_maze(self, payload: CreateMazePayload, owner: str) -> Maze:
        maze = Maze(entrance=payload.entrance, gridSize=payload.gridSize, walls=payload.walls, id=str(uuid4()))
        if owner in self._mazes:
            self._mazes[owner].append(maze)
        else:
            self._mazes[owner] = [maze]
        return maze

    def get_maze(self, owner: str, maze_id: str) -> t.Optional[Maze]:
        return next(maze for maze in self.get_mazes(owner) if maze.id == maze_id)

    def get_mazes(self, owner: str) -> t.List[Maze]:
        if owner in self._mazes:
            return self._mazes[owner]
        else:
            return []

    def print_maze(self, owner: str, maze_id: str) -> t.Optional[str]:
        maze = self.get_maze(owner, maze_id)
        if maze is not None:
            print_maze(maze)
        else:
            return None
