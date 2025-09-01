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
    def check_edge(cube: Cube):
        edge_list = []
        for index in top_edges_index:
            top_color = cube.cube[Cube.YELLOW][index]
            edge_face = top_edges_dict[index]
            edge_color = cube.cube[edge_face][1]
            if top_color != "Y" and edge_color != "Y":
                edge_list.append((str(top_color), str(edge_color)))
        return edge_list

    edges = check_edge(cube)
    return edges
