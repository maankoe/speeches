from typing import List

import networkx as nx

from speeches.analysis.spacy_wrappers.ent import Ent
from speeches.analysis.spacy_wrappers.span import Span


class TokenDependencies:
    def __init__(self, sentence: Span):
        self._graph = nx.Graph()
        for token in sentence:
            self._graph.add_node(token.i, text=token.text, pos=token.pos_)
        for token in sentence:
            self._graph.add_edge(token.i, token.head.i, dep=token.dep_)

    def has_path(self, source: Ent, target: Ent) -> bool:
        return nx.has_path(self._graph, source.root.i, target.root.i)

    def shortest_path(self, source: Ent, target: Ent) -> List[str]:
        return [self._graph.nodes[x]["text"]
                for x in sorted(nx.shortest_path(self._graph, source.root.i, target.root.i))]
