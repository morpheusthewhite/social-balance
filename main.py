from social_balance import frustration_model
import argparse
import graph_tool.all as gt
import numpy as np

parser = argparse.ArgumentParser()
parser.add_argument(
    "-m",
    "--model",
    default="xor",
    metavar="MODEL_NAME",
    dest="model_name",
    help="Which model to use (either 'and', 'xor' or 'abs')",
)
parser.add_argument(
    "-g",
    "--graph",
    metavar="GRAPH_FILE",
    dest="graph_file",
    default=None,
    help="Load a graph-tool graph from the given file. It needs to have an edge_property_map `weights` which contains the sign of the edges",
)


def main():
    args = parser.parse_args()

    if args.graph_file is None:
        edges1 = [[0, 1, 1], [2, 1, 1], [2, 0, 1]]
        n_frustrated1 = frustration_model(3, edges1, args.model_name)

        print("=" * 20)
        print(f"Edges: {edges1}")
        print(f"Number of frustrated edges: {n_frustrated1}")
        print("=" * 20)

        edges2 = [[0, 1, 1], [2, 1, 1], [2, 0, -1]]
        n_frustrated2 = frustration_model(3, edges2, args.model_name)

        print("=" * 20)
        print(f"Edges: {edges2}")
        print(f"Number of frustrated edges: {n_frustrated2}")
        print("=" * 20)
    else:
        graph = gt.load_graph(args.graph_file)
        num_vertices = graph.num_vertices()
        num_edges = graph.num_edges()
        weights = graph.edge_properties["weights"]

        edges = graph.get_edges([weights])
        # get the sign of the weights (in case they are float if casted they
        # may produce uncorrect values)
        edges[:, 2] = np.sign(edges[:, 2])
        # now cast to int
        edges = edges.astype(np.int32)

        n_frustrated = frustration_model(num_vertices, edges, args.model_name)

        print("=" * 20)
        print(f"Edges: {edges}")
        print(f"Number of frustrated edges: {n_frustrated}")
        print(f"Fraction of frustrated edges: {n_frustrated/num_edges}")
        print("=" * 20)


if __name__ == "__main__":
    main()
