from cube import Cube

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


def is_f2l_valid(cube: Cube):
    def check_top_edge():
        edge_list = []

        for index in top_edges_index:
            top_color = cube.cube[Cube.YELLOW][index]
            edge_face_index = top_edges_dict[index]
            edge_color = cube.cube[edge_face_index][1]
            edge = str(top_color + edge_color)
            if "Y" not in edge:
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
                corner_list.append(corner_colors)

        return corner_list

    corner_pairs = check_top_corners()

    return edge_pairs, corner_pairs
