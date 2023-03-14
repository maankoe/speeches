from abc import ABC, abstractmethod
from typing import Iterable, Optional

from spacy import tokens

from speeches.analysis.spacy_wrappers.ent import Ent


class Span(ABC):
    @staticmethod
    def actual(spacy_span: tokens.Span) -> "Span":
        return SpacySpan(spacy_span)

    @staticmethod
    def mock(text: Optional[str]=None, ents: Optional[Iterable[Ent]]=None) -> "Span":
        return MockSpan(text, ents)

    @abstractmethod
    def __iter__(self):
        pass

    @property
    @abstractmethod
    def text(self) -> str:
        pass

    @property
    @abstractmethod
    def ents(self) -> Iterable[Ent]:
        pass


class SpacySpan(Span):
    def __init__(self, spacy_span: tokens.Span):
        self._span = spacy_span

    def __iter__(self):
        return self._span.__iter__()

    @property
    def text(self) -> str:
        return self._span.text

    @property
    def ents(self) -> Iterable[Ent]:
        return (Ent.actual(x) for x in self._span.ents)


class MockSpan(Span):
    def __init__(self, text: str = None, ents: Iterable[Ent] = None):
        self._text = text
        self._ents = ents

    def __iter__(self):
        return self.text.split(" ")

    @property
    def text(self) -> str:
        return self._text or "text"

    @property
    def ents(self) -> Iterable[Ent]:
        return self._ents or []
