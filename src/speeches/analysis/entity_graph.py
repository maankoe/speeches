from itertools import product
from typing import Any, Mapping

import networkx as nx
import json

from speeches.analysis.entity import Entity
from speeches.analysis.entity_disambiguator import EntityDisambiguator
from speeches.analysis.spacy_wrappers.ent import Ent
from speeches.analysis.spacy_wrappers.span import Span
from speeches.analysis.token_dependencies import TokenDependencies

OBSERVATIONS = "obs"

def entity_attributes(ent: Ent) -> Mapping[str, Any]:
    return {"text": ent.text, "ent_label": ent.label_}


def relationship_attributes(source: Ent, target: Ent, token_dependencies: TokenDependencies):
    return {
        "source_text": source.text,
        "target_text": target.text,
        "path": token_dependencies.shortest_path(source, target)
    }


class EntityGraph:
    def __init__(self, entity_disambiguator: EntityDisambiguator):
        self._graph = nx.Graph()
        self._entity_disambiguator = entity_disambiguator

    def _resolve_entities(self, span: Span) -> Mapping[Ent, Entity]:
        return {ent: self._entity_disambiguator.resolve(ent) for ent in span.ents}

    def _add_entity_nodes(self, entities: Mapping[Ent, Entity]) -> None:
        for ent, entity in entities.items():
            attributes = entity_attributes(ent)
            if self._graph.has_node(entity.id):
                self._graph.nodes[entity.id][OBSERVATIONS].append(attributes)
            else:
                self._graph.add_node(entity.id, **{OBSERVATIONS: [attributes]})

    def _add_entity_edges(self, entities: Mapping[Ent, Entity], token_dependencies: TokenDependencies) -> None:
        for (source_ent, source_entity), (target_ent, target_entity) in product(entities.items(), entities.items()):
            if source_ent.root.i < target_ent.root.i and token_dependencies.has_path(source_ent, target_ent):
                attributes = relationship_attributes(source_ent, target_ent, token_dependencies)
                if self._graph.has_edge(source_entity.id, target_entity.id):
                    self._graph[source_entity.id][target_entity.id][OBSERVATIONS].append(attributes)
                else:
                    self._graph.add_edge(source_entity.id, target_entity.id, **{OBSERVATIONS: [attributes]})

    def add(self, span: Span):
        entities = self._resolve_entities(span)
        self._add_entity_nodes(entities)
        self._add_entity_edges(entities, TokenDependencies(span))

    def to_json(self):
        return json.dumps(nx.node_link_data(self._graph), indent=4)

