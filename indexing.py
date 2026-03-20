import os
import pandas as pd
from collections import defaultdict
from preprocessing import preprocess


def load_corpus(folder: str) -> dict:
    """Baca semua file .txt dari folder corpus."""
    corpus = {}
    for fname in sorted(os.listdir(folder)):
        if fname.endswith('.txt'):
            doc_id = fname.replace('.txt', '')
            with open(os.path.join(folder, fname), encoding='utf-8') as f:
                corpus[doc_id] = f.read().strip()
    return corpus


def build_inverted_index(corpus: dict) -> dict:
    
    # Struktur sementara: term -> {doc_id -> [posisi]}
    raw = defaultdict(lambda: defaultdict(list))

    for doc_id, text in corpus.items():
        tokens = preprocess(text)
        for pos, token in enumerate(tokens, start=1):
            raw[token][doc_id].append(pos)

    # Bentuk final
    index = {}
    for term, doc_dict in sorted(raw.items()):
        postings = []
        for doc_id, positions in sorted(doc_dict.items()):
            postings.append({
                "id"       : doc_id,
                "fij"      : len(positions),
                "positions": positions,
            })
        index[term] = postings
    return index


def build_incidence_matrix(corpus: dict, inv_index: dict) -> pd.DataFrame:
    """
    Bangun Incidence Matrix (TFbiner):
    baris = term, kolom = dokumen
    nilai = 1 jika term ada di dokumen, 0 jika tidak.
    """
    doc_ids = list(corpus.keys())
    vocab   = sorted(inv_index.keys())

    matrix = pd.DataFrame(0, index=vocab, columns=doc_ids)
    for term, postings in inv_index.items():
        for p in postings:
            matrix.loc[term, p["id"]] = 1
    return matrix
