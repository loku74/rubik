import json
from copy import deepcopy
from dataclasses import dataclass

from cube import Cube


@dataclass
class CornerPair:
    index: int
    pair: str


top_edges_index = (1, 3, 5, 7)
top_edges_dict = {1: Cube.GREEN, 3: Cube.ORANGE, 5: Cube.RED, 7: Cube.BLUE}

top_corners_pairs = (
    (0, 0, 2),
    (2, 0, 2),
    (8, 0, 2),
    (6, 0, 2),
)

top_corners_dict = {
    0: [Cube.ORANGE, Cube.GREEN],
    2: [Cube.GREEN, Cube.RED],
    8: [Cube.RED, Cube.BLUE],
    6: [Cube.BLUE, Cube.ORANGE],
}


def get_top_side_pairs(cube: Cube):
    def check_top_edge():
        edge_list = []

        for index in top_edges_index:
            top_color = cube.cube[Cube.YELLOW][index]
            edge_face_index = top_edges_dict[index]
            edge_color = cube.cube[edge_face_index][1]
            edge = str(top_color + edge_color)
            if "Y" not in edge and "W" not in edge:
                edge = "".join(sorted(edge))
                edge_list.append(edge)

        return edge_list

    edge_pairs = check_top_edge()

    def check_top_corners():
        corner_list = []

        for top_index, side_index_1, side_index_2 in top_corners_pairs:
            top_color = cube.cube[Cube.YELLOW][top_index]

            corner_face_index_1 = top_corners_dict[top_index][0]
            corner_color_1 = cube.cube[corner_face_index_1][side_index_1]
            corner_face_index_2 = top_corners_dict[top_index][1]
            corner_color_2 = cube.cube[corner_face_index_2][side_index_2]

            corner_colors = str(top_color + corner_color_1 + corner_color_2)
            if "W" in corner_colors:
                corner_colors = corner_colors.replace("W", "")
                corner_colors = "".join(sorted(corner_colors))
                corner_list.append(CornerPair(top_index, corner_colors))

        return corner_list

    corner_pairs = check_top_corners()

    return edge_pairs, corner_pairs


def get_corner(edge_pairs, corner_pairs: [CornerPair]):
    for corner_pair in corner_pairs:
        if corner_pair.pair in edge_pairs:
            return corner_pair
    return None


def is_f2l_solved(cube: Cube, pair: str):
    pair_dict = {
        "GO": (
            ("O", (cube.cube[Cube.ORANGE][3], cube.cube[Cube.ORANGE][6])),
            ("G", (cube.cube[Cube.GREEN][5], cube.cube[Cube.GREEN][8])),
            ("W", (cube.cube[Cube.WHITE][6])),
        ),
        "GR": (
            ("G", (cube.cube[Cube.GREEN][3], cube.cube[Cube.GREEN][6])),
            ("R", (cube.cube[Cube.RED][5], cube.cube[Cube.RED][8])),
            ("W", (cube.cube[Cube.WHITE][8])),
        ),
        "BR": (
            ("B", (cube.cube[Cube.BLUE][5], cube.cube[Cube.BLUE][8])),
            ("R", (cube.cube[Cube.RED][3], cube.cube[Cube.RED][6])),
            ("W", (cube.cube[Cube.WHITE][2])),
        ),
        "BO": (
            ("B", (cube.cube[Cube.BLUE][3], cube.cube[Cube.BLUE][6])),
            ("O", (cube.cube[Cube.ORANGE][5], cube.cube[Cube.ORANGE][8])),
            ("W", (cube.cube[Cube.WHITE][0])),
        ),
    }

    pair_solve = pair_dict[pair]
    for correct_color, colors in pair_solve:
        for color in colors:
            if color != correct_color:
                return False
    return True


def solve_f2l_top(cube: Cube, pair: str):
    print("solving corner", pair)
    pair_y = {"GO": "y2", "GR": "y", "BR": None, "BO": "y'"}
    f2l_moves = json.loads(open("./algorithms/top_f2l.json").read())
    for move in f2l_moves:
        saved_cube = deepcopy(cube)
        moves = []
        if pair_y[pair] is not None:
            moves.append(pair_y[pair])
        split = move.split()
        moves.extend(split)
        cube_moves = saved_cube.move(moves)
        if is_f2l_solved(saved_cube, pair):
            return cube_moves
    return None


def solve(cube: Cube):
    pair_dict = {
        "GO": 0,
        "GR": 2,
        "BR": 8,
        "BO": 6,
    }

    def set_corner(corner, cube):
        print("setting corner", corner.pair)
        for move in ["U", "U'", "U2"]:
            saved_cube = deepcopy(cube)
            saved_cube.move([move])
            _, corners = get_top_side_pairs(saved_cube)
            for c in corners:
                if c.pair == corner.pair and c.index == pair_dict[corner.pair]:
                    return move
        return None

    move_list = []

    edge_pairs, corner_pairs = get_top_side_pairs(cube)
    pairs = [
        corner_pair for corner_pair in corner_pairs if corner_pair.pair in edge_pairs
    ]

    print([pair.pair for pair in pairs])

    while True:
        edge_pairs, corner_pairs = get_top_side_pairs(cube)
        pairs = [
            corner_pair
            for corner_pair in corner_pairs
            if corner_pair.pair in edge_pairs
        ]

        if pairs:
            # check if a corner is already in place
            corner = None
            for corner_pair in pairs:
                if pair_dict[corner_pair.pair] == corner_pair.index:
                    corner = corner_pair
            # if not we place one
            if not corner:
                corner = get_corner(edge_pairs, corner_pairs)
                move = set_corner(corner, cube)
                if move:
                    cube.move([move])
                    move_list.append(move)
                f2l_moves = solve_f2l_top(cube, corner.pair)
                if f2l_moves:
                    move_list.extend(f2l_moves)
                    cube.move(f2l_moves)
            else:
                f2l_moves = solve_f2l_top(cube, corner.pair)
                if f2l_moves:
                    move_list.extend(f2l_moves)
                    cube.move(f2l_moves)
        else:
            break

    return move_list
