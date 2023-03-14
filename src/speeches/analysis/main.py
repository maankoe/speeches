from speeches.analysis.entity_disambiguator import EntityDisambiguator
from speeches.analysis.entity_graph import EntityGraph
from speeches.analysis.spacy_wrappers.spacy import Spacy
from speeches.util.file_util import DATA_DIR, COVID_SPEECHES, TEXT

if __name__ == "__main__":
    text_dir = DATA_DIR / COVID_SPEECHES / TEXT

    spacy = Spacy()

    entity_disambiguator = EntityDisambiguator()

    for file in text_dir.iterdir():
        print("Processing:", file)
        with open(file) as f:
            doc = spacy.process(f.read())
            doc_entity_graph = EntityGraph(entity_disambiguator)
            for sentence in doc.sents:
                doc_entity_graph.add(sentence)
        print(doc_entity_graph.to_json())
        break
