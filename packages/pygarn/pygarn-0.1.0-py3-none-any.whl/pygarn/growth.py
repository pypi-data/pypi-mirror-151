import itertools

from typing import TypeVar
from typing import Union

import networkx as nx
import numpy as np

from pygarn.base import GraphOperation
from pygarn.base import RandomVertexSelector
from pygarn.base import VertexDegreeSelector
from pygarn.base import VertexSelector
from pygarn.base import get_unused_vertices_and_relabel
from pygarn.base import pass_param_or_call


T_Graph = TypeVar("T_Graph", bound=nx.Graph)  # T_Graph = Type[nx.Graph]


class AddVertex(GraphOperation):
    def __init__(self, connect_to: VertexSelector = RandomVertexSelector(min=1, max=3)):
        self._selector_connect_to = connect_to

    def applicable(self, graph: T_Graph) -> bool:
        return True

    def forward_inplace(self, graph: T_Graph) -> T_Graph:
        vertices_new = get_unused_vertices_and_relabel(graph)
        vertex_new = vertices_new[0]
        targets = None
        if len(graph.nodes) > 0:
            targets = self._selector_connect_to.forward_sample(graph)
        graph.add_node(vertex_new)
        if targets is not None:
            graph.add_edges_from([(vertex_new, t) for t in targets])

    def backward_inplace(self, graph: T_Graph) -> T_Graph:
        assert len(graph.nodes) > 0

        selector_degree = VertexDegreeSelector(
            limit=None,
            min=1,
            max=1,
            min_degree=self._selector_connect_to._sample_min,
            max_degree=self._selector_connect_to._sample_max,
        )
        vertices = selector_degree.forward_sample(graph)
        if len(vertices) < 1:
            raise ValueError("Operation could not be applied to graph")
        graph.remove_nodes_from(vertices)


class DuplicateGraph(GraphOperation):
    def __init__(
        self,
        bridge_selector: VertexSelector = RandomVertexSelector(min=1, max=3),
        backward_trials: Union[int, callable] = 1000,
    ):
        self._selector = bridge_selector
        self._backward_trials = backward_trials
        self._backward_acc_threshold = lambda g: int(np.log(len(g.nodes) - 1))

    def applicable(self, graph: T_Graph) -> bool:
        return True

    def forward_inplace(self, graph: T_Graph) -> T_Graph:
        if len(graph.nodes) < 1:
            return graph

        other = graph.copy()
        graph_new = nx.union(graph, other, rename=("G", "H"))

        sources = self._selector.forward_sample(graph)
        targets = self._selector.forward_sample(other)

        graph_new.add_edges_from(
            [(f"G{s}", f"H{t}") for s, t in itertools.product(sources, targets)]
        )
        nx.relabel_nodes(
            graph_new, {name: ix for ix, name in enumerate(graph_new.nodes)}, copy=False
        )

        return graph_new

    def backward_inplace(self, graph: T_Graph) -> T_Graph:
        if len(graph.nodes) % 2 != 0:
            raise ValueError(
                "Graph must have an even number of vertices to be put backward in half."
            )

        cur_trial = 0
        trials = []

        v2d = {v: d for v, d in graph.degree()}
        graph_edges = [(s, t) for s, t in graph.edges]

        while cur_trial < 10 * pass_param_or_call(self._backward_trials, graph):
            cur_graph = graph.copy()
            cur_trial += 1

            """selector_bridges = VertexDegreeSelector(
                limit=None,
                min=1,
                max=2 * self._selector._sample_max,
                min_degree=2,
                max_degree=None
            )
            vertices = selector_bridges.forward_sample(cur_graph)"""
            # TODO using strange heuristic to find some kind of a bridge
            candidate_Gs = []
            candidate_Hs = []
            np.random.shuffle(graph_edges)
            for (s, t) in graph_edges:
                if s == t or v2d[s] < 2 or v2d[t] < 2:
                    continue
                if len(candidate_Gs) == 0 and len(candidate_Hs) == 0:
                    candidate_Gs.append(s)
                    candidate_Hs.append(t)
                else:
                    s_pot_h = False
                    t_pot_h = False
                    for h in candidate_Hs:
                        if cur_graph.has_edge(s, h):
                            s_pot_h = True
                        if cur_graph.has_edge(t, h):
                            t_pot_h = True
                    s_pot_g = False
                    t_pot_g = False
                    for g in candidate_Gs:
                        if cur_graph.has_edge(s, g):
                            s_pot_g = True
                        if cur_graph.has_edge(t, g):
                            t_pot_g = True
                    if s_pot_h and t_pot_g and not (t_pot_h or s_pot_g):
                        candidate_Hs.append(s)
                        candidate_Gs.append(t)
            edges = [
                (s, t)
                for s, t in itertools.product(candidate_Gs, candidate_Hs)
                if s != t
            ]

            if edges in trials:
                continue
            # print(f"Trial with {edges}")
            trials.append(edges)
            cur_graph.remove_edges_from(edges)

            comps = [
                comp for comp, _ in zip(nx.connected_components(cur_graph), range(3))
            ]
            if len(comps) != 2:
                continue

            if np.abs(len(comps[0]) - len(comps[1])) < pass_param_or_call(
                self._backward_acc_threshold, cur_graph
            ):
                print(f"Took {cur_trial} trials.")
                return cur_graph.subgraph(comps[0])

        print(f"Took {cur_trial} trials.")
        raise ValueError(
            "Could not find an appropriate half for the given graph in time."
        )
