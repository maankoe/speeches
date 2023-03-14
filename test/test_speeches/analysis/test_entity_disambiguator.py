import unittest

from speeches.analysis.entity_disambiguator import EntityDisambiguator
from speeches.analysis.spacy_wrappers.span import Span


class TestEntityDisambiguator(unittest.TestCase):
    def test_same_text_resolves_to_same_entity(self):
        disambiguator = EntityDisambiguator()
        entity_text = "A"
        entity_a = disambiguator.resolve(Span.mock(entity_text))
        entity_b = disambiguator.resolve(Span.mock(entity_text))
        self.assertEqual(entity_a, entity_b)

    def test_different_text_resolves_to_different_entity(self):
        disambiguator = EntityDisambiguator()
        entity_text_a = "A"
        entity_text_b = "B"
        entity_a = disambiguator.resolve(Span.mock(entity_text_a))
        entity_b = disambiguator.resolve(Span.mock(entity_text_b))
        self.assertNotEqual(entity_a, entity_b)