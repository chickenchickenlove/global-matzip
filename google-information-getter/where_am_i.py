from haversine import inverse_haversine, Direction
from dataclasses import dataclass


@dataclass
class Position:
    '''
    (-1, -1) is None.
    '''
    y: float
    x: float


def move_east(y1, x1, radius):
    return inverse_haversine((y1, x1), radius, Direction.EAST, unit='m')


def move_south(y1, x1, radius):
    return inverse_haversine((y1, x1), radius, Direction.SOUTH, unit='m')


class Coordinator:

    def __init__(self, y1: float, x1: float, y2: float, x2: float, diameter: float):
        self._start_position = Position(y1, x1)
        self._end_position = Position(y2, x2)
        self._radius = (diameter / 2)
        self._now_position = Position(y1, x1)

    def get_next_position(self) -> Position:
        if self._now_position == Position(-1, -1):
            return self._now_position

        if self.__end_of_the_south():
            move_direction = self.__move_to_east if self.__possible_move_to_east() else self.__move_to_south
            self.__move(move_direction)
            self._now_position = self._now_position if self.__end_of_the_south() else Position(-1, -1)
            return self._now_position

        else:
            self._now_position = Position(-1, -1)
            return self._now_position

    def __end_of_the_south(self) -> bool:
        return self._now_position.y > self._end_position.y

    def __possible_move_to_east(self) -> bool:
        return self._now_position.x < self._end_position.x

    def __move(self, move):
        move()

    def __move_to_south(self) -> None:
        next_y, _ = move_south(self._now_position.y, self._start_position.x, self._radius)
        self._now_position = Position(next_y, self._start_position.x)

    def __move_to_east(self) -> None:
        _, next_x = move_east(self._now_position.y, self._now_position.x, self._radius)
        self._now_position = Position(self._now_position.y, next_x)


def test1_class():
    y1 = 21.04378
    x1 = 105.81020
    y2 = 20.98680
    x2 = 105.86385
    RADIUS = 10000

    sut = Coordinator(y1, x1, y2, x2, RADIUS)

    while (result := sut.get_next_position()) != Position(-1,-1):
        print(result)

# test1_class()