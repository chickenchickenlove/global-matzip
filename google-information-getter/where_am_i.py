from haversine import inverse_haversine, Direction
from dataclasses import dataclass


@dataclass
class Position:

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

        self.__is_first = True

    def __iter__(self):
        return self

    def __next__(self):
        if self.__is_south_end() and self.__is_east_end():
            raise StopIteration

        if self.__is_first:
            self.__is_first = False
            return self

        self.__move_to_east() if not self.__is_east_end() else self.__move_to_south()
        return self

    def get_position(self) -> Position:
        return self._now_position

    def get_position_with_tuple(self) -> tuple:
        return self._now_position.y, self._now_position.x

    def __is_south_end(self) -> bool:
        return self._now_position.y < self._end_position.y

    def __is_east_end(self) -> bool:
        return self._now_position.x > self._end_position.x


    def __move_to_south(self) -> None:
        next_y, _ = move_south(self._now_position.y, self._start_position.x, self._radius)
        self._now_position = Position(next_y, self._start_position.x)

    def __move_to_east(self) -> None:
        _, next_x = move_east(self._now_position.y, self._now_position.x, self._radius)
        self._now_position = Position(self._now_position.y, next_x)


def test2_class():
    y1 = 21.04378
    x1 = 105.81020
    y2 = 20.98680
    x2 = 105.86385
    RADIUS = 10000

    for o in Coordinator(y1, x1, y2, x2, RADIUS):
        print(f'{o.get_position() = }')

# test2_class()


# for minus test case.
def test3_class():
    y1, x1, y2, x2 = (-8.063314, 114.468484, -8.818296, 115.682313)
    RADIUS = 25000

    cnt = 0
    for o in Coordinator(y1, x1, y2, x2, RADIUS):
        cnt += 1
        print(f'{o.get_position() = }')
    print(cnt)
