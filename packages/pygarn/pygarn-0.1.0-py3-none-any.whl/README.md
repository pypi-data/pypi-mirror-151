# pygarn [![PyPI version](https://badge.fury.io/py/pygarn.svg)](https://badge.fury.io/py/pygarn) ![Tests](https://github.com/innvariant/pygarn/workflows/Tests/badge.svg) [![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/) [![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)

```python
import networkx as nx
from pygarn.base import VertexDegreeSelector
from pygarn.growth import AddVertex

n_vertices_initial = 20
g_initial = nx.erdos_renyi_graph(n_vertices_initial, 0.3)
n_edges_initial = len(g_initial.edges)
degrees_initial = [(v, d) for v, d in g_initial.degree()]

selector = VertexDegreeSelector()
op_add = AddVertex()
n_rounds = 5

g_current = g_initial.copy()
for _ in range(n_rounds):
    g_current = op_add.forward(g_current)

```
