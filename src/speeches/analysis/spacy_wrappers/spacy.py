import spacy

from speeches.analysis.spacy_wrappers.doc import Doc


class Spacy:
    def __init__(self):
        self._model = spacy.load("en_core_web_md")

    def process(self, text: str) -> Doc:
        return Doc.actual(self._model(text))
