from speeches.analysis.entity import Entity
from speeches.analysis.spacy_wrappers.ent import Ent
from speeches.analysis.spacy_wrappers.span import Span


class EntityDisambiguator:
    def __init__(self):
        self._entities = {}

    def resolve(self, text_entity: Ent) -> Entity:
        if text_entity.text in self._entities:
            return self._entities[text_entity.text]
        else:
            entity = Entity(len(self._entities))
            self._entities[text_entity.text] = entity
            return entity
