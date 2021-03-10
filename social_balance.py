import pulp
import numpy as np


def frustration_model(
    n_vertices: int,
    edges: list[list[int]],
    optimize: bool = True,
    degrees: list[int] = None,
    model_name: str = "and",
) -> int:
    """calculate frustration using either AND, XOR or ABS formulation

    Args:
        n_vertices (int): number of vertices in the graph. Vertices index in
        the edges need to be in [0, n_vertices-1]
        edges (list[list[int]]): a list (or numpy array) of the edges, each element being a 3
        element list (or tuple) whose elements are, respectively:
            - the index of one of the incident vertices
            - the index of the other incident vertex
            - the edge sign (+1 or -1)
        optimize: if true use optimizations
        degrees: the degrees of the nodes. if optimization is true and they are
        not provided they will be computed
        model: which of the models to use (either "and", "xor" or "abs")

    Returns:
        int: the number of frustrated edges
    """
    model = pulp.LpProblem("frustration_model", pulp.LpMinimize)

    vertices_variables = [
        pulp.LpVariable(name=f"x_{i}", cat=pulp.LpBinary)
        for i in range(n_vertices)
    ]

    objective = []

    for i, edge in enumerate(edges):
        vertex1 = edge[0]
        x_i = vertices_variables[vertex1]

        vertex2 = edge[1]
        x_j = vertices_variables[vertex2]

        sign = edge[2]

        if model_name == "and":
            # create edge variable, x_ij
            x_ij = pulp.LpVariable(
                name=f"x_{vertex1}{vertex2}{i}", cat=pulp.LpBinary
            )
        elif model_name == "abs":
            e_ij = pulp.LpVariable(
                name=f"e_{vertex1}{vertex2}{i}", cat=pulp.LpBinary
            )
            h_ij = pulp.LpVariable(
                name=f"h_{vertex1}{vertex2}{i}", cat=pulp.LpBinary
            )
        else:
            f_ij = pulp.LpVariable(
                name=f"f_{vertex1}{vertex2}{i}", cat=pulp.LpBinary
            )

        if sign >= 0:
            if model_name == "and":
                model += x_ij <= x_i
                model += x_ij <= x_j
            elif model_name == "abs":
                model += x_i - x_j == e_ij - h_ij
            else:
                model += f_ij >= x_i - x_j
                model += f_ij >= x_j - x_i

        else:
            if model_name == "and":
                model += x_ij >= x_i + x_j - 1
            elif model_name == "abs":
                model += x_i + x_j - 1 == e_ij - h_ij
            else:
                model += f_ij >= x_i + x_j - 1
                model += f_ij >= 1 - x_j - x_i

        if model_name == "and":
            f_ij = (1 - sign) / 2 + sign * (x_i + x_j - 2 * x_ij)
        elif model_name == "abs":
            f_ij = e_ij + h_ij
        else:
            pass

        objective.append(f_ij)

    model += pulp.lpSum(objective)
    model.solve()

    return pulp.value(model.objective)
