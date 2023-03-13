from ctypes import Union
from typing import Iterable, Any, Mapping, List

import spacy
import networkx as nx
import json

from spacy.tokens.doc import Doc
from spacy.tokens.span import Span
from spacy.tokens.token import Token

from speeches.util.file_util import *


OBSERVATIONS = "obs"


def token_dependency_graph(sentence: Iterable[Token]) -> nx.DiGraph:
    graph = nx.DiGraph()
    for token in sentence:
        graph.add_node(token.i, text=token.text, pos=token.pos_)
    for token in sentence:
        graph.add_edge(token.i, token.head.i, dep=token.dep_)
    return graph


def entity_attributes(entity: Span) -> Mapping[str, Any]:
    return {"text": entity.text, "ent_label": entity.label_}

def relationship_attributes(source: Span, target: Span, token_graph: nx.DiGraph):
    return {}

class Entity:
    def __init__(self, id: int):
        self._id = id

    @property
    def id(self):
        return self._id


class EntityDisambiguator:
    def __init__(self):
        self._entities = {}

    def resolve(self, entity_span: Span) -> Entity:
        if entity_span.text in self._entities:
            return self._entities[entity_span.text]
        else:
            entity = Entity(len(self._entities))
            self._entities[entity_span.text] = entity
            return entity


class EntityGraph:
    def __init__(self, entity_disambiguator: EntityDisambiguator):
        self._graph = nx.Graph()
        self._entity_disambiguator = entity_disambiguator

    def _resolve_entity(self, entity_span: Span):
        return self._entity_disambiguator.resolve(entity_span)

    def _add_entity_nodes(self, span: Span):
        for entity_span in span.ents:
            entity = self._resolve_entity(entity_span)
            if self._graph.has_node(entity.id):
                self._graph.nodes[entity.id][OBSERVATIONS].append(entity_attributes(entity_span))
            else:
                self._graph.add_node(entity.id, **{OBSERVATIONS: [entity_attributes(entity_span)]})

    def _add_entity_edges(self, span: Span):
        token_graph = token_dependency_graph(span)
        for source in span.ents:
            for target in span.ents:
                if source != target and nx.has_path(token_graph, source.root.i, target.root.i):
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


if __name__ == "__main__":
    text_dir = DATA_DIR / COVID_SPEECHES / TEXT

    model = spacy.load("en_core_web_md")

    entity_disambiguator = EntityDisambiguator()

    for file in text_dir.iterdir():
        print("Processing:", file)
        with open(file) as f:
            doc = model(f.read())
            doc_entity_graph = EntityGraph(entity_disambiguator)
            for sentence in doc.sents:
                doc_entity_graph.add(sentence)
        print(doc_entity_graph.to_json())
        break
