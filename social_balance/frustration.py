import gurobipy as gp
import numpy as np


def and_model(
    n_vertices: int,
    edges: np.array,
    optimize: bool = True,
    degrees: np.array = None,
) -> int:
    """calculate frustration using XOR formulation (no optimization)

    Args:
        n_vertices (int): number of vertices in the graph. Vertices index in
        the edges need to be in [0, n_vertices-1]
        edges (np.array): a (n_edges, 3) numpy array, each row representing an
        edge:
            - the first and second elements are the vertices index
            - the third element is the edge sign (+1 or -1)
        optimize: if true use optimizations
        degrees: the degrees of the nodes. if optimization is true and they are
        not provided they will be computed

    Returns:
        int: the number of frustrated edges
    """
    model = gp.Model("and_unoptimized")
    vertices_variables = [
        model.addVar(vtype=gp.GRB.BINARY, name=f"x_{i}")
        for i in range(n_vertices)
    ]
    model.update()

    objective = 0
    # if optimization is requested and degrees are not provided they are
    # computed in the cycle
    if degrees is None and optimize:
        degrees_ = np.zeros((n_vertices), dtype=np.int32)

    for edge in edges:
        vertex1 = edge[0]
        x_i = vertices_variables[vertex1]

        vertex2 = edge[1]
        x_j = vertices_variables[vertex2]

        # if not provided compute the degrees
        if degrees is None and optimize:
            degrees_[vertex1] += 1
            degrees_[vertex2] += 1

        sign = edge[2]

        # create edge variable, x_ij
        x_ij = model.addVar(vtype=gp.GRB.BINARY, name=f"x_{vertex1}{vertex2}")
        model.update()

        if sign >= 0:
            model.addConstr(x_ij <= x_i)
            model.addConstr(x_ij <= x_j)

        else:
            model.addConstr(x_ij >= x_i + x_j - 1)

        f_ij = (1 - sign) / 2 + sign * (x_i + x_j - 2 * x_ij)
        objective += f_ij

    if degrees is None:
        degrees = degrees_

    for i, degree in enumerate(degrees):
        x_i = vertices_variables[i]
        x_i.branchPriority = int(degree)

    model.setObjective(objective, gp.GRB.MINIMIZE)
    model.optimize()

    return model.objVal


def xor_model(
    n_vertices: int,
    edges: np.array,
    optimize: bool = True,
    degrees: np.array = None,
) -> int:
    """calculate frustration using AND formulation (no optimization)

    Args:
        n_vertices (int): number of vertices in the graph. Vertices index in
        the edges need to be in [0, n_vertices-1]
        edges (np.array): a (n_edges, 3) numpy array, each row representing an
        edge:
            - the first and second elements are the vertices index
            - the third element is the edge sign (+1 or -1)
        optimize: if true use optimizations
        degrees: the degrees of the nodes. if optimization is true and they are
        not provided they will be computed

    Returns:
        int: the number of frustrated edges
    """
    model = gp.Model("and_unoptimized")
    vertices_variables = [
        model.addVar(vtype=gp.GRB.BINARY, name=f"x_{i}")
        for i in range(n_vertices)
    ]
    model.update()

    objective = 0
    # if optimization is requested and degrees are not provided they are
    # computed in the cycle
    if degrees is None and optimize:
        degrees_ = np.zeros((n_vertices), dtype=np.int32)

    for edge in edges:
        vertex1 = edge[0]
        x_i = vertices_variables[vertex1]

        vertex2 = edge[1]
        x_j = vertices_variables[vertex2]

        # if not provided compute the degrees
        if degrees is None and optimize:
            degrees_[vertex1] += 1
            degrees_[vertex2] += 1

        sign = edge[2]

        # create edge variable, x_ij
        f_ij = model.addVar(vtype=gp.GRB.BINARY, name=f"f_{vertex1}{vertex2}")
        model.update()

        if sign >= 0:
            model.addConstr(f_ij >= x_i - x_j)
            model.addConstr(f_ij >= x_j - x_i)

        else:
            model.addConstr(f_ij >= x_i + x_j - 1)
            model.addConstr(f_ij >= 1 - x_j - x_i)

        objective += f_ij

    if degrees is None:
        degrees = degrees_

    for i, degree in enumerate(degrees):
        x_i = vertices_variables[i]
        x_i.branchPriority = int(degree)

    model.setObjective(objective, gp.GRB.MINIMIZE)
    model.optimize()

    return model.objVal


def abs_model(
    n_vertices: int,
    edges: np.array,
    optimize: bool = True,
    degrees: np.array = None,
) -> int:
    """calculate frustration using ABS formulation (no optimization)

    Args:
        n_vertices (int): number of vertices in the graph. Vertices index in
        the edges need to be in [0, n_vertices-1]
        edges (np.array): a (n_edges, 3) numpy array, each row representing an
        edge:
            - the first and second elements are the vertices index
            - the third element is the edge sign (+1 or -1)
        optimize: if true use optimizations
        degrees: the degrees of the nodes. if optimization is true and they are

    Returns:
        int: the number of frustrated edges
    """
    model = gp.Model("and_unoptimized")
    vertices_variables = [
        model.addVar(vtype=gp.GRB.BINARY, name=f"x_{i}")
        for i in range(n_vertices)
    ]
    model.update()

    objective = 0
    # if optimization is requested and degrees are not provided they are
    # computed in the cycle
    if degrees is None and optimize:
        degrees_ = np.zeros((n_vertices), dtype=np.int32)

    for edge in edges:
        vertex1 = edge[0]
        x_i = vertices_variables[vertex1]

        vertex2 = edge[1]
        x_j = vertices_variables[vertex2]

        # if not provided compute the degrees
        if degrees is None and optimize:
            degrees_[vertex1] += 1
            degrees_[vertex2] += 1

        sign = edge[2]

        # create edge variable, x_ij
        e_ij = model.addVar(vtype=gp.GRB.BINARY, name=f"e_{vertex1}{vertex2}")
        h_ij = model.addVar(vtype=gp.GRB.BINARY, name=f"h_{vertex1}{vertex2}")
        model.update()

        if sign >= 0:
            model.addConstr(x_i - x_j == e_ij - h_ij)
        else:
            model.addConstr(x_i + x_j - 1 == e_ij - h_ij)

        f_ij = e_ij + h_ij
        objective += f_ij

    if degrees is None:
        degrees = degrees_

    for i, degree in enumerate(degrees):
        x_i = vertices_variables[i]
        x_i.branchPriority = int(degree)

    model.setObjective(objective, gp.GRB.MINIMIZE)
    model.optimize()

    return model.objVal
