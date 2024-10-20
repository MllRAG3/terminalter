import itertools
from colorama import Fore

from game_objects.cell import Cell


class Field:
    def __init__(self, field: list[list[Cell]]):
        self.field = field

    @staticmethod
    def get_around(field: list[list], xpos: int, ypos: int):
        rows = field[ypos - 1 if ypos > 1 else 0:ypos + 2]
        res = list(itertools.chain(*list(map(lambda x: x[xpos - 1 if xpos > 1 else 0: xpos + 2], rows))))
        res.remove(field[ypos][xpos])
        return res

    def __getitem__(self, item: tuple[int, int]):
        return self.field[item[1]][item[0]]

    @staticmethod
    def unlock_cell(cell: Cell) -> bool:
        if not cell.is_locked:
            return True
        return input("Данная клетка защищена! Вы уверены, что хотите ее открыть? [Y/n] >> ") == "Y"

    def open(self, cell: Cell) -> bool:
        if cell.is_opened:
            return False
        if cell.is_mine:
            return cell.open()  # True, mine
        if cell.mines_around != 0:
            return cell.open()  # False, is not mine 100%
        cell.open()

        row = tuple(filter(lambda x: cell in x, self.field))[0]
        xpos = row.index(cell)
        ypos = self.field.index(row)
        for f in filter(lambda x: not x.is_opened, self.get_around(field=self.field, xpos=xpos, ypos=ypos)):
            self.open(cell=f)

    @property
    def is_cleared(self) -> bool:
        return all(
            list(map(lambda x: all(map(lambda y: y.marked_mine if y.is_mine else y.is_opened, x)), self.field)) + [True]
        )

    def open_start_sector(self):
        zero_mines_around_cell = list(filter(
            lambda x: x.mines_around == 0 and not x.is_mine,
            itertools.chain(*self.field)
        ))
        if not zero_mines_around_cell:
            to_open = list(filter(
                lambda x: not x.is_mine,
                itertools.chain(*self.field)
            ))[0]
        else:
            to_open = zero_mines_around_cell[0]
        self.open(cell=to_open)

    def __len__(self):
        return len(self.field[0])

    @staticmethod
    def join_row(row: list[Cell]):
        return "".join(map(str, row))

    def __str__(self):
        return (
            "{}"
            "\n   / x {}"
            "\ny /"
            "\n{}"
            "\n".format(
                Fore.LIGHTMAGENTA_EX + "Же-есть какое опасное минное поле (зачем ты ваще сюда полез?):" + Fore.RESET,
                Fore.RESET + "".join(map(
                    lambda x: str(x).rjust(2, "0").ljust(3, " "),
                    range(1, len(self) + 1)
                )),
                "\n".join(map(
                    lambda x: '{}    {}'.format(Fore.RESET + str(x[0]).rjust(2, "0"), self.join_row(x[1])),
                    list(enumerate(self.field, start=1))
                ))
            )
        )
