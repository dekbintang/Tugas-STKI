import re
from preprocessing import preprocess


# ── Vektor Boolean ───────────────────────────────────────────
def boolean_vector(term: str, doc_ids: list, inv_index: dict) -> list:
    present = {p["id"] for p in inv_index.get(term, [])}
    return [1 if d in present else 0 for d in doc_ids]

def vec_and(a, b): return [x & y for x, y in zip(a, b)]
def vec_or(a, b):  return [x | y for x, y in zip(a, b)]
def vec_not(a):    return [1 - x for x in a]


# ── Tokenizer query (mendukung kurung) ───────────────────────
def tokenize_query(raw: str) -> list:
    """
    Pecah query menjadi token: term, AND, OR, NOT, (, )
    Contoh: 'Fuzzy OR NOT (Genetik AND Learning)'
    -> ['Fuzzy', 'OR', 'NOT', '(', 'Genetik', 'AND', 'Learning', ')']
    """
    raw = raw.strip()
    raw = raw.replace('(', ' ( ').replace(')', ' ) ')
    tokens = raw.split()
    return tokens

class BooleanParser:

    def __init__(self, tokens, doc_ids, inv_index, steps):
        self.tokens   = tokens
        self.pos      = 0
        self.doc_ids  = doc_ids
        self.inv_index= inv_index
        self.steps    = steps  # list untuk menyimpan langkah-langkah

    def peek(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos].upper()
        return None

    def consume(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def parse_or(self):
        """Level terendah: OR"""
        left = self.parse_and()
        while self.peek() == "OR":
            self.consume()
            right = self.parse_and()
            result = vec_or(left, right)
            left_str  = "".join(str(v) for v in left)
            right_str = "".join(str(v) for v in right)
            res_str   = "".join(str(v) for v in result)
            self.steps.append(f"{left_str} OR {right_str} = {res_str}")
            left = result
        return left

    def parse_and(self):
        """Level: AND"""
        left = self.parse_not()
        while self.peek() == "AND":
            self.consume()
            right = self.parse_not()
            result = vec_and(left, right)
            left_str  = "".join(str(v) for v in left)
            right_str = "".join(str(v) for v in right)
            res_str   = "".join(str(v) for v in result)
            self.steps.append(f"{left_str} AND {right_str} = {res_str}")
            left = result
        return left

    def parse_not(self):
        """Level: NOT"""
        if self.peek() == "NOT":
            self.consume()
            operand = self.parse_primary()
            result  = vec_not(operand)
            op_str  = "".join(str(v) for v in operand)
            res_str = "".join(str(v) for v in result)
            self.steps.append(f"NOT {op_str} = {res_str}")
            return result
        return self.parse_primary()

    def parse_primary(self):
        """Level tertinggi: term atau ekspresi dalam kurung"""
        if self.peek() == "(":
            self.consume()  # makan '('
            result = self.parse_or()
            if self.peek() == ")":
                self.consume()  # makan ')'
            return result

        # Term biasa
        tok = self.consume()
        stemmed = preprocess(tok)
        if stemmed:
            term = stemmed[0]
        else:
            term = tok.lower()
        vec = boolean_vector(term, self.doc_ids, self.inv_index)
        vec_str = "".join(str(v) for v in vec)
        self.steps.append(f"TFbiner({term}) = {vec_str}")
        return vec


def evaluate_query(raw: str, doc_ids: list, inv_index: dict):
    """
    Evaluasi query boolean dengan operator precedence.
    Kembalikan (result_vector, steps, bool_vecs)
    """
    tokens = tokenize_query(raw)
    steps  = []
    parser = BooleanParser(tokens, doc_ids, inv_index, steps)
    result = parser.parse_or()

    # Kumpulkan vektor per term untuk ditampilkan
    bool_vecs = {}
    for tok in tokens:
        if tok.upper() not in ("AND", "OR", "NOT", "(", ")"):
            stemmed = preprocess(tok)
            term    = stemmed[0] if stemmed else tok.lower()
            if term not in bool_vecs:
                bool_vecs[term] = boolean_vector(term, doc_ids, inv_index)

    return result, steps, bool_vecs


# ── Parse operator utama (untuk label) ──────────────────────
def parse_query(raw: str):
    raw = raw.strip()
    if " AND " in raw.upper():
        parts = re.split(r'\s+AND\s+', raw, flags=re.IGNORECASE)
        return parts, "AND"
    elif " OR " in raw.upper():
        parts = re.split(r'\s+OR\s+', raw, flags=re.IGNORECASE)
        return parts, "OR"
    elif raw.upper().startswith("NOT "):
        return [raw[4:].strip()], "NOT"
    else:
        return raw.split(), "OR"


# ── Fungsi utama ─────────────────────────────────────────────
def search(raw_query: str, corpus: dict, inv_index: dict) -> dict:
    doc_ids = list(corpus.keys())

    result_vec, steps, bool_vecs = evaluate_query(raw_query, doc_ids, inv_index)

    results = []
    for doc_id, relevan in zip(doc_ids, result_vec):
        results.append({"doc_id": doc_id, "relevan": relevan})

    return {
        "results"  : results,
        "steps"    : steps,
        "bool_vecs": bool_vecs,
        "doc_ids"  : doc_ids,
        "result_vec": result_vec,
    }