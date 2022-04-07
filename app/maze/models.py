import typing
import typing as t

from pydantic import BaseModel, root_validator, constr, conlist

Coords = typing.Tuple[int, int]
GridSize = typing.Tuple[int, int]
Path = typing.List[Coords]


def parse_coords(coords: str) -> t.Tuple[int, int]:
    x = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'.index(coords[0])
    y = int(coords[1]) - 1
    return x, y


def parse_grid_size(grid_size: str) -> t.Tuple[int, int]:
    dimensions = grid_size.split("x")
    return int(dimensions[0]), int(dimensions[1])


class CreateMazePayload(BaseModel):
    entrance: constr(regex=r'^[A-Z][0-9]+$')
    gridSize: constr(regex=r'[1-9][0-9]*x[1-9][0-9]*')
    walls: conlist(constr(regex=r'^[A-Z][0-9]+$'))

    @root_validator()
    @classmethod
    def check_entrance_within_bounds(cls, values):
        entrance_coords = parse_coords(values['entrance'])
        grid = parse_grid_size(values['gridSize'])
        if entrance_coords[0] >= grid[0] or entrance_coords[1] >= grid[1]:
            raise ValueError(f"Entrance is not within bounds.")
        return values

    @root_validator()
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
            raise ValueError(f"Entrance can't be where wall is.")
        return values


class Maze(CreateMazePayload):
    id: str

