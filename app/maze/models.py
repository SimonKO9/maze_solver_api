import typing as t
from enum import Enum

from pydantic import BaseModel, root_validator, constr, conlist  # pylint: disable=no-name-in-module

Coords = t.Tuple[int, int]
GridSize = t.Tuple[int, int]
Path = t.List[Coords]


class Steps(Enum):
    MIN = "min"
    MAX = "max"


def parse_coords(coords: str) -> t.Tuple[int, int]:
    x_coord = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.index(coords[0])
    y_coord = int(coords[1]) - 1
    return x_coord, y_coord


def parse_grid_size(grid_size: str) -> t.Tuple[int, int]:
    dimensions = grid_size.split("x")
    return int(dimensions[0]), int(dimensions[1])


class CreateMazePayload(BaseModel):
    entrance: constr(regex=r'^[A-Z][0-9]+$')
    gridSize: constr(regex=r'[1-9][0-9]*x[1-9][0-9]*')
    walls: conlist(constr(regex=r'^[A-Z][0-9]+$'))

    @root_validator(skip_on_failure=True)
    @classmethod
    def check_entrance_within_bounds(cls, values):
        entrance_coords = parse_coords(values['entrance'])
        grid = parse_grid_size(values['gridSize'])
        if entrance_coords[0] >= grid[0] or entrance_coords[1] >= grid[1]:
            raise ValueError("Entrance is not within bounds.")
        return values

    @root_validator(skip_on_failure=True)
    @classmethod
    def check_walls_within_bounds(cls, values):
        grid = parse_grid_size(values['gridSize'])
        for wall in values['walls']:
            coords = parse_coords(wall)
            if coords[0] >= grid[0] or coords[1] >= grid[1]:
                raise ValueError(f"Wall {wall} is not within bounds.")
        return values

    @root_validator()
    @classmethod
    def check_entrance_not_at_all(cls, values):
        entrance = values['entrance']
        walls = values['walls']
        if entrance in walls:
            raise ValueError("Entrance can't be where wall is.")
        return values


class Maze(CreateMazePayload):
    id: str
