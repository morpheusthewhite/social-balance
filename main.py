from social_balance import frustration_model
import argparse

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
    "-on",
    "--optimize-no",
    action="store_true",
    default=False,
    dest="no_optimize",
    help="If passed does not use optimization techniques (like branching priority and lazy constraints)",
)


def main():
    args = parser.parse_args()

    edges1 = [[0, 1, 1], [2, 1, 1], [2, 0, 1]]
    n_frustrated1 = frustration_model(
        3, edges1, args.no_optimize, args.model_name
    )

    print("=" * 20)
    print(f"Edges: {edges1}")
    print(f"Number of frustrated edges: {n_frustrated1}")
    print("=" * 20)

    edges2 = [[0, 1, 1], [2, 1, 1], [2, 0, -1]]
    n_frustrated2 = frustration_model(
        3, edges2, args.no_optimize, args.model_name
    )

    print("=" * 20)
    print(f"Edges: {edges2}")
    print(f"Number of frustrated edges: {n_frustrated2}")
    print("=" * 20)


if __name__ == "__main__":
    main()
