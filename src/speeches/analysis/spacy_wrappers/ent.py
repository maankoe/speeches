from abc import ABC, abstractmethod

from spacy import tokens
from speeches.analysis.spacy_wrappers.token import Token


class Ent(ABC):
    @staticmethod
    def actual(entity_span: tokens.Span):
        return SpacyEnt(entity_span)

    @property
    @abstractmethod
    def text(self) -> str:
        pass

    @property
    @abstractmethod
    def label_(self) -> str:
        pass

    @property
    @abstractmethod
    def root(self) -> Token:
        pass


class SpacyEnt(Ent):
    def __init__(self, entity_span: tokens.Span):
        self._span = entity_span

    @property
    def text(self) -> str:
        return self._span.text

    @property
    def label_(self) -> str:
        return self._span.label_

    @property
    def root(self) -> Token:
        return Token.actual(self._span.root)

    def __eq__(self, other):
        return self._span.__eq__(other._span)

    def __hash__(self):
        return self._span.__hash__()