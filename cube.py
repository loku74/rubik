from random import choices

import numpy as np


class Cube:
    WHITE = 0
    YELLOW = 1
    RED = 2
    GREEN = 3
    BLUE = 4
    ORANGE = 5

    def __init__(self):
        self.cube = {
            self.WHITE: np.array(
                ["W1", "W2", "W3", "W4", "W5", "W6", "W7", "W8", "W9"]
            ),
            self.YELLOW: np.array(
                ["Y1", "Y2", "Y3", "Y4", "Y5", "Y6", "Y7", "Y8", "Y9"]
            ),
            self.RED: np.array(["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9"]),
            self.GREEN: np.array(
                ["G1", "G2", "G3", "G4", "G5", "G6", "G7", "G8", "G9"]
            ),
            self.BLUE: np.array(["B1", "B2", "B3", "B4", "B5", "B6", "B7", "B8", "B9"]),
            self.ORANGE: np.array(
                ["O1", "O2", "O3", "O4", "O5", "O6", "O7", "O8", "O9"]
            ),
        }
        self.previous = None
        self.y = 0
        self.x = 0

    def format(self, colors=False):
        def add(str, index, piece, space=False):
            if index % 3 == 0:
                if index != 0:
                    str += "\n"
                if space:
                    str += " " * 9
                str += piece + " "
            else:
                str += piece + " "
            return str

        str = ""
        for index, piece in enumerate(self.cube[self.GREEN]):
            str = add(str, index, piece, space=True)
        str += "\n"
        for k in range(3):
            for face in [
                self.cube[self.ORANGE],
                self.cube[self.WHITE],
                self.cube[self.RED],
                self.cube[self.YELLOW],
            ]:
                str += face[k * 3] + " "
                str += face[1 + k * 3] + " "
                str += face[2 + k * 3] + " "
            str += "\n"

        for index, piece in enumerate(self.cube[self.BLUE]):
            str = add(str, index, piece, space=True)
        if colors:
            for k in range(1, 10):
                str = str.replace(f"W{k}", "⬜️")
                str = str.replace(f"Y{k}", "🟨")
                str = str.replace(f"R{k}", "🟥")
                str = str.replace(f"G{k}", "🟩")
                str = str.replace(f"B{k}", "🟦")
                str = str.replace(f"O{k}", "🟧")
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

    def U(self):
        pieces = [0, 1, 2]
        self.swap(self.RED, self.BLUE, pieces)
        self.swap(self.RED, self.ORANGE, pieces)
        self.swap(self.RED, self.GREEN, pieces)
        temp = np.reshape(self.cube[self.YELLOW], (3, 3))
        temp = np.rot90(temp, k=-1)
        self.cube[self.YELLOW] = temp.flatten()

    def Ui(self):
        pieces = [0, 1, 2]
        self.swap(self.RED, self.GREEN, pieces)
        self.swap(self.RED, self.ORANGE, pieces)
        self.swap(self.RED, self.BLUE, pieces)
        temp = np.reshape(self.cube[self.YELLOW], (3, 3))
        temp = np.rot90(temp, k=1)
        self.cube[self.YELLOW] = temp.flatten()

    def U2(self):
        self.U()
        self.U()

    def D(self):
        pieces = [6, 7, 8]
        self.swap(self.RED, self.GREEN, pieces)
        self.swap(self.RED, self.ORANGE, pieces)
        self.swap(self.RED, self.BLUE, pieces)
        temp = np.reshape(self.cube[self.WHITE], (3, 3))
        temp = np.rot90(temp, k=-1)
        self.cube[self.WHITE] = temp.flatten()

    def Di(self):
        pieces = [6, 7, 8]
        self.swap(self.RED, self.BLUE, pieces)
        self.swap(self.RED, self.ORANGE, pieces)
        self.swap(self.RED, self.GREEN, pieces)
        temp = np.reshape(self.cube[self.WHITE], (3, 3))
        temp = np.rot90(temp, k=1)
        self.cube[self.WHITE] = temp.flatten()

    def D2(self):
        self.D()
        self.D()

    def R(self):
        pieces = [2, 5, 8]
        self.swap(self.BLUE, self.YELLOW, pieces)
        self.swap(self.BLUE, self.GREEN, pieces[::-1], to=[0, 3, 6])
        self.swap(self.BLUE, self.WHITE, pieces)
        temp = np.reshape(self.cube[self.RED], (3, 3))
        temp = np.rot90(temp, k=-1)
        self.cube[self.RED] = temp.flatten()

    def Ri(self):
        pieces = [2, 5, 8]
        self.swap(self.BLUE, self.WHITE, pieces)
        self.swap(self.BLUE, self.GREEN, pieces[::-1], to=[0, 3, 6])
        self.swap(self.BLUE, self.YELLOW, pieces)
        temp = np.reshape(self.cube[self.RED], (3, 3))
        temp = np.rot90(temp, k=1)
        self.cube[self.RED] = temp.flatten()

    def R2(self):
        self.R()
        self.R()

    def L(self):
        pieces = [0, 3, 6]
        self.swap(self.BLUE, self.WHITE, pieces)
        self.swap(self.BLUE, self.GREEN, pieces[::-1], to=[2, 5, 8])
        self.swap(self.BLUE, self.YELLOW, pieces)
        temp = np.reshape(self.cube[self.ORANGE], (3, 3))
        temp = np.rot90(temp, k=-1)
        self.cube[self.ORANGE] = temp.flatten()

    def Li(self):
        pieces = [0, 3, 6]
        self.swap(self.BLUE, self.YELLOW, pieces)
        self.swap(self.BLUE, self.GREEN, pieces[::-1], to=[2, 5, 8])
        self.swap(self.BLUE, self.WHITE, pieces)
        temp = np.reshape(self.cube[self.ORANGE], (3, 3))
        temp = np.rot90(temp, k=1)
        self.cube[self.ORANGE] = temp.flatten()

    def L2(self):
        self.L()
        self.L()

    def F(self):
        self.swap(self.YELLOW, self.RED, [6, 7, 8], to=[0, 3, 6])
        self.swap(self.YELLOW, self.WHITE, [6, 7, 8], to=[2, 1, 0])
        self.swap(self.YELLOW, self.ORANGE, [6, 7, 8], to=[8, 5, 2])
        temp = np.reshape(self.cube[self.BLUE], (3, 3))
        temp = np.rot90(temp, k=-1)
        self.cube[self.BLUE] = temp.flatten()

    def Fi(self):
        self.swap(self.YELLOW, self.ORANGE, [6, 7, 8], to=[8, 5, 2])
        self.swap(self.YELLOW, self.WHITE, [6, 7, 8], to=[2, 1, 0])
        self.swap(self.YELLOW, self.RED, [6, 7, 8], to=[0, 3, 6])
        temp = np.reshape(self.cube[self.BLUE], (3, 3))
        temp = np.rot90(temp, k=1)
        self.cube[self.BLUE] = temp.flatten()

    def F2(self):
        self.F()
        self.F()

    def B(self):
        self.swap(self.YELLOW, self.ORANGE, [0, 1, 2], to=[6, 3, 0])
        self.swap(self.YELLOW, self.WHITE, [0, 1, 2], to=[8, 7, 6])
        self.swap(self.YELLOW, self.RED, [0, 1, 2], to=[2, 5, 8])
        temp = np.reshape(self.cube[self.GREEN], (3, 3))
        temp = np.rot90(temp, k=-1)
        self.cube[self.GREEN] = temp.flatten()

    def Bi(self):
        self.swap(self.YELLOW, self.RED, [0, 1, 2], to=[2, 5, 8])
        self.swap(self.YELLOW, self.WHITE, [0, 1, 2], to=[8, 7, 6])
        self.swap(self.YELLOW, self.ORANGE, [0, 1, 2], to=[6, 3, 0])
        temp = np.reshape(self.cube[self.GREEN], (3, 3))
        temp = np.rot90(temp, k=1)
        self.cube[self.GREEN] = temp.flatten()

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
