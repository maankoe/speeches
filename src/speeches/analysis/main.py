from speeches.analysis.entity_disambiguator import EntityDisambiguator
from speeches.analysis.entity_graph import EntityGraph
from speeches.analysis.spacy_wrappers.spacy import Spacy
from speeches.util.file_util import DATA_DIR, COVID_SPEECHES, TEXT

if __name__ == "__main__":
    text_dir = DATA_DIR / COVID_SPEECHES / TEXT

    spacy = Spacy()

    entity_disambiguator = EntityDisambiguator()
    entity_graph = EntityGraph(entity_disambiguator)


    for file in text_dir.iterdir():
        print("Processing:", file)
        with open(file) as f:
            doc = spacy.process(f.read())
            for sentence in doc.sents:
                entity_graph.add(sentence)
    print(entity_graph.to_json())
