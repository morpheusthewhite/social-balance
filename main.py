import numpy as np
from social_balance.frustration import (
    and_model,
    xor_model,
    abs_model,
)


def main():
    solving_function = abs_model

    edges1 = np.array([[0, 1, 1], [2, 1, 1], [2, 0, 1]])
    n_frustrated1 = solving_function(3, edges1)

    print("=" * 20)
    print(f"Edges: {edges1}")
    print(f"Number of frustrated edges: {n_frustrated1}")
    print("=" * 20)
    print("-" * 10)

    edges2 = np.array([[0, 1, 1], [2, 1, 1], [2, 0, -1]])
    n_frustrated2 = solving_function(3, edges2)

    print("=" * 20)
    print(f"Edges: {edges2}")
    print(f"Number of frustrated edges: {n_frustrated2}")
    print("=" * 20)


if __name__ == "__main__":
    main()
