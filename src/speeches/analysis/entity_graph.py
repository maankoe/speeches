from typing import Any, Mapping

import networkx as nx
import json

from speeches.analysis.entity_disambiguator import EntityDisambiguator
from speeches.analysis.spacy_wrappers.ent import Ent
from speeches.analysis.spacy_wrappers.span import Span
from speeches.analysis.token_dependencies import TokenDependencies

OBSERVATIONS = "obs"

def entity_attributes(ent: Ent) -> Mapping[str, Any]:
    return {"text": ent.text, "ent_label": ent.label_}

def relationship_attributes(source: Ent, target: Ent, token_dependencies: TokenDependencies):
    return {}


class EntityGraph:
    def __init__(self, entity_disambiguator: EntityDisambiguator):
        self._graph = nx.Graph()
        self._entity_disambiguator = entity_disambiguator

    def _resolve_entity(self, text_entity: Ent):
        return self._entity_disambiguator.resolve(text_entity)

    def _add_entity_nodes(self, span: Span):
        for entity_span in span.ents:
            entity = self._resolve_entity(entity_span)
            if self._graph.has_node(entity.id):
                self._graph.nodes[entity.id][OBSERVATIONS].append(entity_attributes(entity_span))
            else:
                self._graph.add_node(entity.id, **{OBSERVATIONS: [entity_attributes(entity_span)]})

    def _add_entity_edges(self, span: Span):
        token_graph = TokenDependencies(span)
        for source in span.ents:
            for target in span.ents:
                if source != target and token_graph.has_path(source.root.i, target.root.i):
                    self._graph.add_edge(
                        self._resolve_entity(source).id,
                        self._resolve_entity(target).id,
                        **{OBSERVATIONS: [relationship_attributes(source, target, token_graph)]}
                    )

    def add(self, span: Span):
        self._add_entity_nodes(span)
        self._add_entity_edges(span)

    def to_json(self):
        return json.dumps(nx.node_link_data(self._graph), indent=4)

