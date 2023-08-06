# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pygarn']

package_data = \
{'': ['*']}

install_requires = \
['networkx>=2.7.1,<3.0.0']

setup_kwargs = {
    'name': 'pygarn',
    'version': '0.1.0',
    'description': '',
    'long_description': '# pygarn [![PyPI version](https://badge.fury.io/py/pygarn.svg)](https://badge.fury.io/py/pygarn) ![Tests](https://github.com/innvariant/pygarn/workflows/Tests/badge.svg) [![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370/) [![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380/)\n\n```python\nimport networkx as nx\nfrom pygarn.base import VertexDegreeSelector\nfrom pygarn.growth import AddVertex\n\nn_vertices_initial = 20\ng_initial = nx.erdos_renyi_graph(n_vertices_initial, 0.3)\nn_edges_initial = len(g_initial.edges)\ndegrees_initial = [(v, d) for v, d in g_initial.degree()]\n\nselector = VertexDegreeSelector()\nop_add = AddVertex()\nn_rounds = 5\n\ng_current = g_initial.copy()\nfor _ in range(n_rounds):\n    g_current = op_add.forward(g_current)\n\n```\n',
    'author': 'Julian Stier',
    'author_email': 'julian.stier@uni-passau.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/innvariant/pygarn',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
