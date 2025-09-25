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
pair_dict = {
    "GO": 0,
    "GR": 2,
    "BR": 8,
    "BO": 6,
}

pair_y = {"BR": None, "GR": "y", "GO": "y2", "BO": "y'"}


def f2l_solved(cube: Cube, pair: str):
    pair_dict = {
        "BR": (
            ("B", (cube.cube[Cube.BLUE][5], cube.cube[Cube.BLUE][8])),
            ("R", (cube.cube[Cube.RED][3], cube.cube[Cube.RED][6])),
            ("W", (cube.cube[Cube.WHITE][2])),
        ),
        "GR": (
            ("G", (cube.cube[Cube.GREEN][3], cube.cube[Cube.GREEN][6])),
            ("R", (cube.cube[Cube.RED][5], cube.cube[Cube.RED][8])),
            ("W", (cube.cube[Cube.WHITE][8])),
        ),
        "GO": (
            ("O", (cube.cube[Cube.ORANGE][3], cube.cube[Cube.ORANGE][6])),
            ("G", (cube.cube[Cube.GREEN][5], cube.cube[Cube.GREEN][8])),
            ("W", (cube.cube[Cube.WHITE][6])),
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


def get_top_edges(cube: Cube):
    edge_list = []

    for index in top_edges_index:
        top_color = cube.cube[Cube.YELLOW][index]
        edge_face_index = top_edges_dict[index]
        edge_color = cube.cube[edge_face_index][1]
        edge = top_color + edge_color
        if "Y" not in edge and "W" not in edge:
            edge = "".join(sorted(edge))
            edge_list.append(edge)

    return edge_list


def get_top_corners(cube: Cube):
    corner_list = []

    for top_index, side_index_1, side_index_2 in top_corners_pairs:
        top_color = cube.cube[Cube.YELLOW][top_index]

        corner_face_index_1 = top_corners_dict[top_index][0]
        corner_color_1 = cube.cube[corner_face_index_1][side_index_1]
        corner_face_index_2 = top_corners_dict[top_index][1]
        corner_color_2 = cube.cube[corner_face_index_2][side_index_2]

        corner_colors = top_color + corner_color_1 + corner_color_2
        if "W" in corner_colors:
            corner_colors = corner_colors.replace("W", "")
            corner_colors = "".join(sorted(corner_colors))
            corner_list.append(CornerPair(top_index, corner_colors))

    return corner_list


def get_top_side_pairs(cube: Cube):
    edge_pairs = get_top_edges(cube)
    corner_pairs = get_top_corners(cube)

    return edge_pairs, corner_pairs


def get_bot_edges(cube: Cube):
    edge_dict = {}
    bottom_edge_sides = (
        (Cube.BLUE, Cube.RED, "BR"),
        (Cube.RED, Cube.GREEN, "GR"),
        (Cube.GREEN, Cube.ORANGE, "GO"),
        (Cube.ORANGE, Cube.BLUE, "BO"),
    )

    for side_1, side_2, key in bottom_edge_sides:
        color_1 = cube.cube[side_1][5]
        color_2 = cube.cube[side_2][3]
        edge = "".join(sorted(color_1 + color_2))
        if "Y" not in edge and not f2l_solved(cube, key):
            edge_dict[key] = edge

    return edge_dict


def get_bot_corners(cube: Cube):
    corner_dict = {}
    bottom_corner_sides = (
        (Cube.BLUE, Cube.RED, 2, "BR"),
        (Cube.RED, Cube.GREEN, 8, "GR"),
        (Cube.GREEN, Cube.ORANGE, 6, "GO"),
        (Cube.ORANGE, Cube.BLUE, 0, "BO"),
    )

    for side_1, side_2, white_index, key in bottom_corner_sides:
        color_1 = cube.cube[side_1][8]
        color_2 = cube.cube[side_2][6]
        color_3 = cube.cube[Cube.WHITE][white_index]
        corner_colors = color_1 + color_2 + color_3
        if "W" in corner_colors and not f2l_solved(cube, key):
            corner_colors = corner_colors.replace("W", "")
            corner_colors = "".join(sorted(corner_colors))
            corner_dict[key] = corner_colors

    return corner_dict


def solve_f2l_top(cube: Cube, pair: str):
    f2l_moves = json.loads(open("./algorithms/top_f2l.json").read())
    f2l_moves = [move.split() for move in f2l_moves]
    for move in f2l_moves:
        saved_cube = deepcopy(cube)
        moves = []
        if pair_y[pair] is not None:
            moves.append(pair_y[pair])
        moves.extend(move)
        cube_moves = saved_cube.move(moves)
        if f2l_solved(saved_cube, pair):
            return cube_moves
    return None


def set_corner(corner: CornerPair, cube: Cube):
    for move in ["U", "U'", "U2"]:
        saved_cube = deepcopy(cube)
        saved_cube.move([move])
        _, corners = get_top_side_pairs(saved_cube)
        for c in corners:
            if c.pair == corner.pair and c.index == pair_dict[corner.pair]:
                return move
    return None


def f2l_case1(cube: Cube):
    final_move_list = []

    saved_cube = deepcopy(cube)
    while True:
        edge_pairs, corner_pairs = get_top_side_pairs(saved_cube)
        pairs = [
            corner_pair
            for corner_pair in corner_pairs
            if corner_pair.pair in edge_pairs
        ]

        if pairs:
            move_list = []
            # check if a corner is already in place
            corner = None
            for corner_pair in pairs:
                if pair_dict[corner_pair.pair] == corner_pair.index:
                    corner = corner_pair
            # if not we select the first corner in pairs
            if not corner:
                corner = pairs[0]
                move = set_corner(corner, saved_cube)
                if move:
                    saved_cube.move([move])
                    move_list.append(move)
            f2l_moves = solve_f2l_top(saved_cube, corner.pair)
            if f2l_moves:
                move_list.extend(f2l_moves)
                saved_cube.move(f2l_moves)
                final_move_list.extend(move_list)
        else:
            break

    return final_move_list


def f2l_case2(cube: Cube):
    top_edges = get_top_edges(cube)
    bot_corners = get_bot_corners(cube)

    final_move_list = []
    for edge in top_edges:
        if edge in bot_corners.keys() and bot_corners[edge] == edge:
            f2l_moves_list = json.loads(open("./algorithms/f2l_case2.json").read())
            f2l_moves_list = [f2l_moves.split() for f2l_moves in f2l_moves_list]
            y = pair_y[edge]
            for f2l_moves in f2l_moves_list:
                for move in [None, "U", "U'", "U2"]:
                    saved_cube = deepcopy(cube)
                    move_list = []
                    if y:
                        move_list.append(y)
                    if move:
                        move_list.append(move)
                    move_list.extend(f2l_moves)
                    cube_moves = saved_cube.move(move_list)
                    if f2l_solved(saved_cube, edge):
                        final_move_list.extend(cube_moves)
                        break

    return final_move_list


def f2l_case3(cube: Cube):
    bot_edges = get_bot_edges(cube)
    top_corners = get_top_corners(cube)
    final_move_list = []
    for corner in top_corners:
        if corner.pair in bot_edges.keys() and bot_edges[corner.pair] == corner.pair:
            f2l_moves_list = json.loads(open("./algorithms/f2l_case3.json").read())
            f2l_moves_list = [f2l_moves.split() for f2l_moves in f2l_moves_list]
            y = pair_y[corner.pair]
            for f2l_moves in f2l_moves_list:
                for move in [None, "U", "U'", "U2"]:
                    saved_cube = deepcopy(cube)
                    move_list = []
                    if y:
                        move_list.append(y)
                    if move:
                        move_list.append(move)
                    move_list.extend(f2l_moves)
                    cube_moves = saved_cube.move(move_list)
                    if f2l_solved(saved_cube, corner.pair):
                        final_move_list.extend(cube_moves)
                        break

    return final_move_list


def test_all_f2l_cases(cube: Cube):
    f2l_cases = (f2l_case2, f2l_case3, f2l_case1)
    for f2l_case in f2l_cases:
        f2l_move_list = f2l_case(cube)
        if f2l_move_list:
            cube.move(f2l_move_list)
            return f2l_move_list


def get_f2l_pairs(
    cube: Cube,
) -> list[str]:
    pair_list = ["BR", "GR", "GO", "BO"]
    pairs = []
    for pair in pair_list:
        if f2l_solved(cube, pair):
            pairs.append(pair)

    return pairs


def move_f2l(cube: Cube):
    pair_list = ["BR", "GR", "GO", "BO"]
    solved_pairs = get_f2l_pairs(cube)

    if solved_pairs == pair_list:
        return None

    pair_list = [pair for pair in pair_list if pair not in solved_pairs]

    moves = [["R", "U", "R'"], ["R", "U'", "R'"], ["F'", "U", "F"], ["F'", "U'", "F"]]
    for pair in pair_list:
        for move in moves:
            move_list = []
            saved_cube = deepcopy(cube)
            y = pair_y[pair]
            if y:
                move_list.append(y)
            move_list.extend(move)
            set_moves = saved_cube.move(move_list)
            if test_all_f2l_cases(saved_cube):
                return set_moves


def all_f2l_solved(cube: Cube):
    pair_list = ["BR", "GR", "GO", "BO"]
    for pair in pair_list:
        if not f2l_solved(cube, pair):
            return False
    return True


# in case edges and corners are not properly placed, we mix them a bit to have a f2l solution
def mix_f2l(cube: Cube) -> list[str]:
    pair_list = ["BR", "BO", "GO", "GR"]
    solved_pairs = get_f2l_pairs(cube)
    move = ["R", "U", "R'"]
    final_move_list = []
    saved_cube = deepcopy(cube)
    for pair in pair_list:
        if pair in solved_pairs:
            continue

        move_list = []
        y = pair_y[pair]
        if y:
            move_list.append(y)
        move_list.extend(move)
        set_moves = saved_cube.move(move_list)
        final_move_list.extend(set_moves)
        if test_all_f2l_cases(saved_cube):
            return final_move_list

    return final_move_list


def solve(cube: Cube) -> list[str]:
    saved_cube = deepcopy(cube)
    final_move_list = []

    while True:
        move_list = test_all_f2l_cases(saved_cube)
        if move_list:
            final_move_list.extend(move_list)
        else:
            move_list = move_f2l(saved_cube)
            if move_list:
                saved_cube.move(move_list)
                final_move_list.extend(move_list)
            elif not all_f2l_solved(saved_cube):
                mix_moves = mix_f2l(saved_cube)
                saved_cube.move(mix_moves)
                final_move_list.extend(mix_moves)
            else:
                return final_move_list
