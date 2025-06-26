import spacy

def get_spacy_model():
    return spacy.load("en_core_web_sm")
