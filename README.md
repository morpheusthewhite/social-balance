# Social balance

This project implements calculation of frustration index, which determines the distance of a signed graph from structural/social balance, using the programming model defined in [A modelling and computational study of the frustration index in signed networks](https://arxiv.org/abs/1611.09030), a paper by Samin Aref, Andrew J. Mason, Mark C. Wilson.

As in the paper, Gurobi is used for solving the optimization problem.

This repository contains a simple `main.py` using the functions defined to
solve the problem for sample graph. It is library agnostic, so any graph
library can be used.

## Prerequisites

To run/use this project you need to install the [Gurobi Optimizer](https://www.gurobi.com/downloads/gurobi-optimizer-eula/) and its python bindings (the easiest way being `python -m pip install -i https://pypi.gurobi.com gurobipy`), which can also be done for conda environments (see [Gurobi guide](https://www.gurobi.com/documentation/9.1/quickstart_mac/cs_python_installation_opt.html) for details). You also need at least Python 3.9 to run this code.

## Usage

To run the examples

```python
$ python main.py
```

The best way of using this code in your project is just copying `social-balance/frustration.py` into your folder and importing it (if you do it then please star this repository, it will help other people finding it).

If you appreciated my work, then follow me [on GitHub](https://github.com/morpheusthewhite).

## License

Distributed under the MIT License. See `LICENSE` for more information.
