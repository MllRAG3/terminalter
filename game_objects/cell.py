from colorama import Fore


class TextureColorConverter:
    textures = {
        0: Fore.WHITE,
        1: Fore.BLUE,
        2: Fore.GREEN,
        3: Fore.YELLOW,
        4: Fore.RED,
        5: Fore.MAGENTA,
        6: Fore.MAGENTA,
        7: Fore.MAGENTA,
        8: Fore.MAGENTA,
    }

    def convert(self, texture: str):
        match texture:
            case "[#]":
                return Fore.LIGHTRED_EX + texture

            case "[ ]":
                return Fore.LIGHTGREEN_EX + texture

            case "[?]":
                return Fore.LIGHTMAGENTA_EX + texture

            case "[F]":
                return Fore.LIGHTYELLOW_EX + texture

            case _ as num_texture:
                return self.textures[int(num_texture.strip())] + num_texture


class Cell:
    def __init__(self, is_mine: bool, texture: str, mines_around: int, xpos: int, ypos: int, is_opened: bool = False) -> None:
        self.ypos = ypos
        self.xpos = xpos
        self.is_opened = is_opened
        self.mines_around = mines_around
        self.texture = texture
        self.is_mine = is_mine

    def open(self) -> bool:
        self.settexture("[#]" if self.is_mine else f" {self.mines_around} ")
        self.is_opened = True

        return self.is_mine

    def settexture(self, new: str) -> None:
        if self.is_opened:
            return

        self.texture = new

    @property
    def is_locked(self) -> bool:
        return self.texture in ["[F]", "[?]"]

    @property
    def marked_mine(self) -> bool:
        return self.is_mine and self.texture == "[F]"

    def __str__(self) -> str:
        return TextureColorConverter().convert(texture=self.texture)

    def __repr__(self) -> str:
        return TextureColorConverter().convert(texture=self.texture)
