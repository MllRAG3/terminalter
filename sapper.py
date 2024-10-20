from argparse import ArgumentParser, Namespace
from colorama import init, Fore
import os
import time

from game_objects import FieldGenerator, Field


class Main:
    def __init__(self):
        self.field: Field | None = None

    def start(self, args: Namespace):
        os.system('cls' if os.name == 'nt' else 'clear')
        generator = FieldGenerator()
        self.field = Field(field=generator.generate(xsize=args.xsize, ysize=args.ysize, mines=args.mines))
        self.field.open_start_sector()
        self.game_polling()

    def render(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print(self.field)

    def turn(self, x: int, y: int) -> bool:
        try:
            instruction = ("Введите 'O' чтобы открыть клетку;"
            "\nВведите '?' чтобы пометить клетку вопросительным знаком;"
            "\nВведите 'F' чтобы пометить клетку флагом"
            "\nВаше действие? [O/F/?]: >> ")
            d = input(instruction)

            match d:
                case "?":
                    self.field[x, y].settexture("[?]")
                case _ as c if c.upper() == "O":
                    if not self.field.unlock_cell(self.field[x, y]):
                        raise Exception("Клетка не была разблокирована!")
                    return self.field.open(self.field[x, y])
                case _ as c if c.upper() == "F":
                    self.field[x, y].settexture("[F]")
                case _:
                    raise Exception("Введено неправильное действие! (Список доступных: ['O', 'F', '?'])")
        except IndexError:
            self.render()
            print("Введены неправильные координаты!")
            time.sleep(3)
            return False
        except Exception as e:
            self.render()
            print(e)
            time.sleep(3)
            return False

    def game_polling(self):
        while True:
            self.render()
            try:
                x = int(input("Введите X координату: ")) - 1
                self.render()
                y = int(input("Введите Y координату: ")) - 1
                self.render()
            except ValueError:
                print("координаты - это числа :)")
                continue
            if x < 0 or y < 0:
                print("координаты не могут быть нулевыми или отрицательными!")
                continue
            if self.turn(x=x, y=y):
                self.render()
                print(Fore.LIGHTRED_EX + "Вы наткнулись на мину! Для повторной игры перезапустите программу.")
                return
            if self.field.is_cleared:
                self.render()
                print(Fore.LIGHTWHITE_EX + "FINE, U WON. IT WAS A GREAT JOB, BYE!")
                return

    @staticmethod
    def setup_args(parser_: ArgumentParser):
        parser_.add_argument('-xsize', help="Размер поля, ширина (макс. 99)", default=18, type=int)
        parser_.add_argument('-ysize', help="Размер поля, высота (макс. 99)", default=10, type=int)
        parser_.add_argument('-m', '--mines', help="Количество мин на поле", default=69, type=int)


if __name__ == "__main__":
    init(autoreset=True)

    main = Main()
    parser = ArgumentParser()
    main.setup_args(parser_=parser)
    main.start(args=parser.parse_args())
