from random import choices

import numpy as np

from utils import y_dict


class Cube:
    WHITE = 0
    YELLOW = 1
    RED = 2
    GREEN = 3
    BLUE = 4
    ORANGE = 5

    def __init__(self):
        self.cube = {
            self.WHITE: np.array(["W", "W", "W", "W", "W", "W", "W", "W", "W"]),
            self.YELLOW: np.array(["Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y", "Y"]),
            self.RED: np.array(["R", "R", "R", "R", "R", "R", "R", "R", "R"]),
            self.GREEN: np.array(["G", "G", "G", "G", "G", "G", "G", "G", "G"]),
            self.BLUE: np.array(["B", "B", "B", "B", "B", "B", "B", "B", "B"]),
            self.ORANGE: np.array(["O", "O", "O", "O", "O", "O", "O", "O", "O"]),
        }
        self.previous = None

    def format(self, colors=False):
        def add(str, index, piece, space=False):
            if index % 3 == 0:
                if index != 0:
                    str += "\n"
                if space:
                    str += " " * 11
                str += piece + " "
            else:
                str += piece + " "
            return str

        str = ""
        for index, piece in enumerate(self.cube[self.GREEN]):
            str = add(str, index, piece, space=True)
        str += "\n" + " " * 11 + "-" * 8 + "\n"

        for k in range(3):
            for index, face in enumerate(
                [
                    self.cube[self.ORANGE],
                    self.cube[self.YELLOW],
                    self.cube[self.RED],
                ]
            ):
                str += face[k * 3] + " "
                str += face[1 + k * 3] + " "
                str += face[2 + k * 3]
                if index != 2:
                    str += " | "
            str += "\n"

        str += " " * 11 + "-" * 8 + "\n"

        for index, piece in enumerate(self.cube[self.BLUE]):
            str = add(str, index, piece, space=True)

        str += "\n"
        str += " " * 11 + "-" * 8 + "\n"

        for index, piece in enumerate(self.cube[self.WHITE]):
            str = add(str, index, piece, space=True)

        if colors:
            for _ in range(10):
                str = str.replace("W", "⬜️")
                str = str.replace("Y", "🟨")
                str = str.replace("R", "🟥")
                str = str.replace("G", "🟩")
                str = str.replace("B", "🟦")
                str = str.replace("O", "🟧")
        return str

    def swap(
        self,
        color_a: int,
        color_b: int,
        pieces: list[int],
        to: list[int] or None = None,
    ):
        x1 = pieces[0]
        x2 = pieces[1]
        x3 = pieces[2]

        if to:
            y1 = to[0]
            y2 = to[1]
            y3 = to[2]
        else:
            y1 = pieces[0]
            y2 = pieces[1]
            y3 = pieces[2]

        (
            self.cube[color_a][x1],
            self.cube[color_a][x2],
            self.cube[color_a][x3],
            self.cube[color_b][y1],
            self.cube[color_b][y2],
            self.cube[color_b][y3],
        ) = (
            self.cube[color_b][y1],
            self.cube[color_b][y2],
            self.cube[color_b][y3],
            self.cube[color_a][x1],
            self.cube[color_a][x2],
            self.cube[color_a][x3],
        )

    def __str__(self):
        return self.format(colors=True)

    def display(self):
        print(self.format())

    def rotate(self, color: int, k: int):
        temp = np.reshape(self.cube[color], (3, 3))
        temp = np.rot90(temp, k=k)
        self.cube[color] = temp.flatten()

    def U(self):
        pieces = [0, 1, 2]
        self.swap(self.RED, self.BLUE, pieces)
        self.swap(self.RED, self.ORANGE, pieces)
        self.swap(self.RED, self.GREEN, pieces)
        self.rotate(self.YELLOW, k=-1)

    def Ui(self):
        pieces = [0, 1, 2]
        self.swap(self.RED, self.GREEN, pieces)
        self.swap(self.RED, self.ORANGE, pieces)
        self.swap(self.RED, self.BLUE, pieces)
        self.rotate(self.YELLOW, k=1)

    def U2(self):
        self.U()
        self.U()

    def D(self):
        pieces = [6, 7, 8]
        self.swap(self.RED, self.GREEN, pieces)
        self.swap(self.RED, self.ORANGE, pieces)
        self.swap(self.RED, self.BLUE, pieces)
        self.rotate(self.WHITE, k=-1)

    def Di(self):
        pieces = [6, 7, 8]
        self.swap(self.RED, self.BLUE, pieces)
        self.swap(self.RED, self.ORANGE, pieces)
        self.swap(self.RED, self.GREEN, pieces)
        self.rotate(self.WHITE, k=1)

    def D2(self):
        self.D()
        self.D()

    def R(self):
        pieces = [2, 5, 8]
        self.swap(self.BLUE, self.YELLOW, pieces)
        self.swap(self.BLUE, self.GREEN, pieces[::-1], to=[0, 3, 6])
        self.swap(self.BLUE, self.WHITE, pieces)
        self.rotate(self.RED, k=-1)

    def Ri(self):
        pieces = [2, 5, 8]
        self.swap(self.BLUE, self.WHITE, pieces)
        self.swap(self.BLUE, self.GREEN, pieces[::-1], to=[0, 3, 6])
        self.swap(self.BLUE, self.YELLOW, pieces)
        self.rotate(self.RED, k=1)

    def R2(self):
        self.R()
        self.R()

    def L(self):
        pieces = [0, 3, 6]
        self.swap(self.BLUE, self.WHITE, pieces)
        self.swap(self.BLUE, self.GREEN, pieces[::-1], to=[2, 5, 8])
        self.swap(self.BLUE, self.YELLOW, pieces)
        self.rotate(self.ORANGE, k=-1)

    def Li(self):
        pieces = [0, 3, 6]
        self.swap(self.BLUE, self.YELLOW, pieces)
        self.swap(self.BLUE, self.GREEN, pieces[::-1], to=[2, 5, 8])
        self.swap(self.BLUE, self.WHITE, pieces)
        self.rotate(self.ORANGE, k=1)

    def L2(self):
        self.L()
        self.L()

    def F(self):
        self.swap(self.YELLOW, self.RED, [6, 7, 8], to=[0, 3, 6])
        self.swap(self.YELLOW, self.WHITE, [6, 7, 8], to=[2, 1, 0])
        self.swap(self.YELLOW, self.ORANGE, [6, 7, 8], to=[8, 5, 2])
        self.rotate(self.BLUE, k=-1)

    def Fi(self):
        self.swap(self.YELLOW, self.ORANGE, [6, 7, 8], to=[8, 5, 2])
        self.swap(self.YELLOW, self.WHITE, [6, 7, 8], to=[2, 1, 0])
        self.swap(self.YELLOW, self.RED, [6, 7, 8], to=[0, 3, 6])
        self.rotate(self.BLUE, k=1)

    def F2(self):
        self.F()
        self.F()

    def B(self):
        self.swap(self.YELLOW, self.ORANGE, [0, 1, 2], to=[6, 3, 0])
        self.swap(self.YELLOW, self.WHITE, [0, 1, 2], to=[8, 7, 6])
        self.swap(self.YELLOW, self.RED, [0, 1, 2], to=[2, 5, 8])
        self.rotate(self.GREEN, k=-1)

    def Bi(self):
        self.swap(self.YELLOW, self.RED, [0, 1, 2], to=[2, 5, 8])
        self.swap(self.YELLOW, self.WHITE, [0, 1, 2], to=[8, 7, 6])
        self.swap(self.YELLOW, self.ORANGE, [0, 1, 2], to=[6, 3, 0])
        self.rotate(self.GREEN, k=1)

    def B2(self):
        self.B()
        self.B()

    # def move(self, str: string):
    #     moves = str.split()

    def randomMove(self, cross=False):
        func_set_list = [
            [self.B, self.Bi, self.B2],
            [self.F, self.Fi, self.F2],
            [self.L, self.Li, self.L2],
            [self.R, self.Ri, self.R2],
            [self.U, self.Ui, self.U2],
            [self.D, self.Di, self.D2],
        ]

        cross_set_list = [
            [self.B2],
            [self.F2],
            [self.L2],
            [self.R2],
            [self.U, self.Ui, self.U2],
            [self.D, self.Di, self.D2],
        ]

        if cross:
            func_set_list = cross_set_list

        set = choices(func_set_list)[0]
        while self.previous == set:
            set = choices(func_set_list)[0]
        self.previous = set
        func = choices(set)[0]
        func()
        return func.__name__

    def move(self, moves=[]):
        move_dict = {
            "R": self.R(),
            "R'": self.Ri(),
            "R2": self.R2(),
            "L": self.L(),
            "L'": self.Li(),
            "L2": self.L2(),
            "F": self.F(),
            "F'": self.Fi(),
            "F2": self.F2(),
            "B": self.B(),
            "B'": self.Bi(),
            "B2": self.B2(),
            "U": self.U(),
            "U'": self.Ui(),
            "U2": self.U2(),
            "D": self.D(),
            "D'": self.Di(),
            "D2": self.D2(),
        }
        for move in moves:
            func = move_dict[move]
            func()

    def translateY(self, moves=[]):
        y = 0
        final_moves = []
        for move in moves:
            if move.contains("y"):
                match move:
                    case "y":
                        y += 1
                    case "y'":
                        y += 3
                    case "y2":
                        y += 2

            elif y % 4:
                final_moves.append(y_dict[y % 4][move])
            else:
                final_moves.append(move)

        return final_moves
