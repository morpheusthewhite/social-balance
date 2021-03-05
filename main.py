import numpy as np
from social_balance.frustration import frustration_model


def main():
    model = "xor"

    edges1 = np.array([[0, 1, 1], [2, 1, 1], [2, 0, 1]])
    n_frustrated1 = frustration_model(3, edges1, False, model=model)

    print("=" * 20)
    print(f"Edges: {edges1}")
    print(f"Number of frustrated edges: {n_frustrated1}")
    print("=" * 20)
    print("-" * 10)

    edges2 = np.array([[0, 1, 1], [2, 1, 1], [2, 0, -1]])
    n_frustrated2 = frustration_model(3, edges2, False, model=model)

    print("=" * 20)
    print(f"Edges: {edges2}")
    print(f"Number of frustrated edges: {n_frustrated2}")
    print("=" * 20)


if __name__ == "__main__":
    main()
