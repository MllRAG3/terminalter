import random
import itertools

from game_objects.cell import Cell
from errors import MinesNumberError, FieldSizeError


class FieldGenerator:
    @staticmethod
    def empty_field(xsize: int, ysize: int):
        return [[Cell(
            is_mine=False, texture="[ ]", mines_around=0
        ) for _ in range(1, xsize + 1)] for __ in range(1, ysize + 1)]

    def add_mines(self, field: list[list[Cell]], mines: int) -> list[list[Cell]]:
        xsize = len(field[0])
        ysize = len(field)

        for _ in range(mines):
            while True:
                x, y = random.randint(0, xsize - 1), random.randint(0, ysize - 1)

                if field[y][x].is_mine:
                    continue
                field[y][x].is_mine = True

                for cell in self.get_around(field=field, xpos=x, ypos=y):
                    cell.mines_around += 1
                break

        return field

    @staticmethod
    def get_around(field: list[list], xpos: int, ypos: int):
        rows = field[ypos - 1 if ypos > 1 else 0:ypos + 2]
        res = list(itertools.chain(*list(map(lambda x: x[xpos - 1 if xpos > 1 else 0: xpos + 2], rows))))
        res.remove(field[ypos][xpos])

        return res

    def generate(self, xsize: int, ysize: int, mines: int) -> list[list[Cell]]:
        if xsize <= 0 or ysize <= 0:
            raise FieldSizeError("Размер поля не может быть нулевым или отрицательным!")

        if xsize >= 100 or ysize >= 100:
            raise FieldSizeError("Максимальный размер поля 99x99!")

        if mines >= xsize * ysize:
            raise MinesNumberError("Мин должно быть хотя бы на 1 меньше, чем доступных в поле клеток!")

        field = self.empty_field(xsize=xsize, ysize=ysize)
        field = self.add_mines(field=field, mines=mines)

        return field
