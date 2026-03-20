import re
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory

factory = StemmerFactory()
stemmer = factory.create_stemmer()


def tokenize(text: str) -> list:
    """Case folding + tokenisasi."""
    text = text.lower()
    text = re.sub(r'[^a-z\s]', ' ', text)
    return [t for t in text.split() if t]


def stem_tokens(tokens: list) -> list:
    """Stemming dengan PySastrawi."""
    return [stemmer.stem(t) for t in tokens]


def preprocess(text: str) -> list:
    """
    Pipeline pre-processing (TANPA stopwords):
    1. Tokenisasi
    2. Stemming (PySastrawi)
    """
    tokens = tokenize(text)
    tokens = stem_tokens(tokens)
    return tokens
