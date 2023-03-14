from abc import ABC, abstractmethod
from typing import Iterable

from spacy import tokens

from speeches.analysis.spacy_wrappers.span import Span


class Doc(ABC):
    @staticmethod
    def actual(spacy_doc: tokens.Doc) -> "Doc":
        return SpacyDoc(spacy_doc)

    @property
    @abstractmethod
    def sents(self) -> Iterable[Span]:
        pass


class SpacyDoc(Doc):
    def __init__(self, spacy_doc: tokens.Doc):
        self._doc = spacy_doc

    @property
    def sents(self) -> Iterable[Span]:
        return (Span.actual(x) for x in self._doc.sents)


