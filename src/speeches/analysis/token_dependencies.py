import networkx as nx

from speeches.analysis.spacy_wrappers.span import Span


class TokenDependencies:
    def __init__(self, sentence: Span):
        self._graph = nx.DiGraph()
        for token in sentence:
            self._graph.add_node(token.i, text=token.text, pos=token.pos_)
        for token in sentence:
            self._graph.add_edge(token.i, token.head.i, dep=token.dep_)

    def has_path(self, source, target) -> bool:
        return nx.has_path(self._graph, source, target)
