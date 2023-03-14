from abc import ABC, abstractmethod

from spacy import tokens


class Token(ABC):
    @staticmethod
    def actual(spacy_token: tokens.Token):
        return SpacyToken(spacy_token)

    @property
    @abstractmethod
    def text(self) -> str:
        pass

    @property
    @abstractmethod
    def head(self) -> "Token":
        pass

    @property
    @abstractmethod
    def pos_(self):
        pass

    @property
    @abstractmethod
    def dep_(self) -> str:
        pass

    @property
    @abstractmethod
    def i(self):
        pass

class SpacyToken(Token):
    def __init__(self, spacy_token: tokens.Token):
        self._token = spacy_token

    @property
    def text(self) -> str:
        return self._token.text

    @property
    def head(self) -> Token:
        return Token.actual(self._token.head)

    @property
    def pos_(self) -> str:
        return self._token.pos_

    @property
    def dep_(self) -> str:
        return self._token.dep_

    @property
    def i(self):
        return self._token.i

class MockToken(Token):
    pass