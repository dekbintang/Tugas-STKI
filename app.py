import streamlit as st
import pandas as pd
from indexing import load_corpus, build_inverted_index, build_incidence_matrix
from ir_model import search, parse_query
from preprocessing import preprocess

st.set_page_config(
    page_title="IR Engine – STKI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@300;400;500;600;700&family=Fira+Code:wght@400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif;
    background-color: #0D1117;
    color: #E6EDF3;
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #161B22 0%, #0D1117 100%);
    border-right: 1px solid #21262D;
}
[data-testid="stSidebar"] * { color: #E6EDF3 !important; }
.main .block-container { background: #0D1117; padding-top: 1.5rem; }
h1 { color: #58A6FF !important; font-weight: 700 !important; font-size: 1.6rem !important; }
h2 { color: #79C0FF !important; font-weight: 600 !important; font-size: 1.1rem !important; }

[data-baseweb="tab-list"] {
    background: #161B22 !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid #21262D !important;
}
[data-baseweb="tab"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: .8rem !important;
    font-weight: 500 !important;
    color: #8B949E !important;
    border-radius: 8px !important;
    padding: .5rem 1.2rem !important;
}
[aria-selected="true"][data-baseweb="tab"] {
    background: #1F6FEB !important;
    color: #FFFFFF !important;
}
[data-testid="stTextInput"] input {
    background: #161B22 !important;
    border: 1px solid #30363D !important;
    border-radius: 8px !important;
    color: #E6EDF3 !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: .9rem !important;
}
[data-testid="stTextInput"] input:focus {
    border-color: #1F6FEB !important;
    box-shadow: 0 0 0 3px rgba(31,111,235,.15) !important;
}
[data-testid="stExpander"] {
    background: #161B22 !important;
    border: 1px solid #21262D !important;
    border-radius: 10px !important;
}
[data-testid="stExpander"]:hover { border-color: #30363D !important; }
details summary { color: #79C0FF !important; font-weight: 500 !important; }
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; border: 1px solid #21262D; }
[data-testid="metric-container"] {
    background: #161B22;
    border: 1px solid #21262D;
    border-radius: 12px;
    padding: 1rem 1.2rem;
}
[data-testid="stMetricValue"] { color: #58A6FF !important; font-size: 1.8rem !important; font-weight: 700 !important; }
[data-testid="stMetricLabel"] { color: #8B949E !important; font-size: .72rem !important; text-transform: uppercase; letter-spacing: 1px; }
[data-testid="stAlert"] {
    background: #161B22 !important;
    border-radius: 10px !important;
    border: 1px solid #21262D !important;
    color: #E6EDF3 !important;
}
hr { border-color: #21262D !important; }
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0D1117; }
::-webkit-scrollbar-thumb { background: #30363D; border-radius: 3px; }
[data-testid="collapsedControl"] { display: none !important; }
[data-testid="stSidebar"] { display: none !important; }

.card {
    background: #161B22;
    border: 1px solid #21262D;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: .6rem;
}
.card:hover { border-color: #30363D; }
.token {
    display: inline-block;
    background: #21262D;
    color: #79C0FF;
    border-radius: 5px;
    padding: 1px 8px;
    font-size: .75rem;
    font-family: 'Fira Code', monospace;
    margin: 2px;
}
.badge {
    display: inline-block;
    background: #1F6FEB18;
    color: #58A6FF;
    border: 1px solid #1F6FEB40;
    border-radius: 20px;
    padding: 2px 10px;
    font-size: .75rem;
    font-weight: 600;
    margin: 2px;
}
.vec-0 {
    display:inline-block;width:26px;height:26px;line-height:26px;
    text-align:center;border-radius:5px;
    background:#1C2128;color:#484F58;
    font-family:'Fira Code',monospace;font-size:.82rem;margin:2px;
}
.vec-1 {
    display:inline-block;width:26px;height:26px;line-height:26px;
    text-align:center;border-radius:5px;
    background:#1F6FEB25;color:#58A6FF;
    border:1px solid #1F6FEB50;
    font-family:'Fira Code',monospace;font-size:.82rem;font-weight:700;margin:2px;
}
.score-row {
    display:flex;align-items:center;gap:10px;
    padding:9px 12px;border-radius:8px;margin-bottom:5px;
    background:#161B22;border:1px solid #21262D;
}
.score-bar { height:5px;border-radius:3px;flex-shrink:0; }
.score-num { color:#58A6FF;font-weight:700;font-size:.82rem;font-family:'Fira Code',monospace;min-width:50px; }
</style>
""", unsafe_allow_html=True)

# ── Load data ─────────────────────────────────────────────────
@st.cache_data
def load_data():
    corpus  = load_corpus("corpus")
    inv_idx = build_inverted_index(corpus)
    matrix  = build_incidence_matrix(corpus, inv_idx)
    return corpus, inv_idx, matrix

corpus, inv_idx, matrix = load_data()
doc_ids = list(corpus.keys())
N = len(corpus)


# ── Header ────────────────────────────────────────────────────
st.markdown("""
<div style='margin-bottom:1.2rem'>
    <h1 style='margin:0'>🔍 Information Retrieval Engine</h1>
    <p style='color:#8B949E;margin:.2rem 0 0;font-size:.85rem'>
        Extended Boolean Model &nbsp;·&nbsp; Incidence Matrix &nbsp;·&nbsp; Inverted Index
    </p>
</div>
""", unsafe_allow_html=True)

# ── Tabs ──────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📄  Corpus",
    "📊  Incidence Matrix",
    "🔍  Inverted Index",
    "🔎  Query",
])

# ══ TAB 1 — CORPUS ═══════════════════════════════════════════
with tab1:
    st.markdown("## Corpus")
    for doc_id, text in corpus.items():
        tokens = preprocess(text)
        with st.expander(f"**{doc_id.upper()}**  —  {len(tokens)} token"):
            st.markdown(f"<div style='color:#CDD9E5;font-size:.9rem;line-height:1.7;margin-bottom:.8rem'>{text}</div>", unsafe_allow_html=True)
            pills = "".join(f"<span class='token'>{t}</span>" for t in tokens)
            st.markdown(pills, unsafe_allow_html=True)

# ══ TAB 2 — INCIDENCE MATRIX ═════════════════════════════════
with tab2:
    st.markdown("## Incidence Matrix")

    filt = st.text_input("Filter term:", key="mat", placeholder="ketik nama term...")
    disp = matrix
    if filt:
        disp = matrix.loc[[t for t in matrix.index if filt.lower() in t]]
        st.caption(f"{len(disp)} term ditampilkan")

    st.dataframe(
        disp.style.applymap(
            lambda v: "background:#1a3a2a; color:#3FB950; font-weight:700" if v == 1
                      else "background:#0D1117; color:#30363D"
        ),
        use_container_width=True,
        height=460,
    )
    st.caption(f"{len(matrix)} term × {N} dokumen")

# ══ TAB 3 — INVERTED INDEX ═══════════════════════════════════
with tab3:
    st.markdown("## Inverted Index")

    filt2 = st.text_input("Cari term:", key="inv", placeholder="ketik term...")
    rows  = []
    for term, postings in sorted(inv_idx.items()):
        if filt2 and filt2.lower() not in term:
            continue
        notasi = "  |  ".join(
            f"<{p['id']}, {p['fij']}, {p['positions']}>" for p in postings
        )
        rows.append({
            "Term"        : term,
            "DF"          : len(postings),
            "Postings"    : notasi,
        })

    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, height=460)
        st.caption(f"{len(rows)} dari {len(inv_idx)} term")
    else:
        st.info("Term tidak ditemukan.")

# ══ TAB 4 — QUERY ════════════════════════════════════════════
with tab4:
    st.markdown("## Query")

    st.markdown("""
    <div class='card' style='margin-bottom:1rem'>
        <div style='color:#8B949E;font-size:.8rem;margin-bottom:.5rem'>Contoh query</div>
        <div>
            <span class='badge'>Fuzzy AND Learning</span>
            <span class='badge'>Genetik AND Learning</span>
            <span class='badge'>Fuzzy OR NOT (Genetik AND Learning)</span>
            <span class='badge'>(Fuzzy OR Optimasi) AND NOT Genetik</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    query_raw = st.text_input("", placeholder="Masukkan query...", label_visibility="collapsed")

    if query_raw:
        hasil      = search(query_raw, corpus, inv_idx)
        results    = hasil["results"]
        steps      = hasil["steps"]
        bool_vecs  = hasil["bool_vecs"]
        result_vec = hasil["result_vec"]
        d_ids      = hasil["doc_ids"]

        st.divider()

        # ── Vektor TFbiner per term ───────────────────────────
        st.markdown("### Vektor TFbiner")
        for term, vec in bool_vecs.items():
            vec_str = "".join(str(v) for v in vec)
            pills   = "".join(f"<span class='vec-{v}'>{v}</span>" for v in vec)
            st.markdown(f"""
            <div class='card' style='padding:.6rem 1rem;display:flex;align-items:center;gap:10px;flex-wrap:wrap'>
                <code style='color:#79C0FF;font-family:Fira Code,monospace;font-size:.82rem;min-width:160px'>TFbiner({term})</code>
                <span style='color:#8B949E'>=</span>
                <code style='color:#58A6FF;font-family:Fira Code,monospace;font-size:.88rem;font-weight:700'>{vec_str}</code>
                <span style='color:#30363D'>|</span>
                {pills}
            </div>
            """, unsafe_allow_html=True)

        # ── Langkah-langkah operasi (seperti slide dosen) ─────
        st.markdown("### Langkah Operasi")
        op_steps = [s for s in steps if " AND " in s or " OR " in s or s.startswith("NOT ")]
        for i, step in enumerate(op_steps):
            parts = step.split(" = ")
            left  = parts[0].strip()
            right = parts[1].strip() if len(parts) > 1 else ""
            is_last = (i == len(op_steps) - 1)
            bg     = "#1a1600" if is_last else "#161B22"
            border = "#F0C04055" if is_last else "#21262D"
            lcolor = "#E3B341"
            rcolor = "#F0C040" if is_last else "#3FB950"
            st.markdown(f"""
            <div style='background:{bg};border:1px solid {border};border-radius:8px;
                        padding:.6rem 1rem;margin-bottom:5px;
                        display:inline-flex;align-items:center;gap:8px'>
                <code style='color:{lcolor};font-family:Fira Code,monospace;font-size:.85rem'>{left}</code>
                <span style='color:#484F58;font-size:.85rem'>=</span>
                <code style='color:{rcolor};font-family:Fira Code,monospace;font-size:.85rem;font-weight:700'>{right}</code>
            </div>
            """, unsafe_allow_html=True)

        # ── Hasil akhir vektor ────────────────────────────────
        res_str   = "".join(str(v) for v in result_vec)
        res_pills = "".join(f"<span class='vec-{v}'>{v}</span>" for v in result_vec)
        st.markdown(f"""
        <div class='card' style='padding:.7rem 1rem;display:flex;align-items:center;gap:10px;flex-wrap:wrap;
             border-color:#F0C04055;background:#1a1600;margin-top:.2rem'>
            <code style='color:#F0C040;font-family:Fira Code,monospace;font-size:.82rem;min-width:120px'>Hasil Akhir</code>
            <span style='color:#8B949E'>=</span>
            <code style='color:#F0C040;font-family:Fira Code,monospace;font-size:.9rem;font-weight:700'>{res_str}</code>
            <span style='color:#30363D'>|</span>
            {res_pills}
        </div>
        """, unsafe_allow_html=True)

        st.divider()

        # ── Tabel hasil dokumen ───────────────────────────────
        st.markdown("### Hasil Pencarian")
        found = [r for r in results if r["relevan"] == 1]

        cols = st.columns(len(d_ids))
        for col, r in zip(cols, sorted(results, key=lambda x: x["doc_id"])):
            hit = r["relevan"] == 1
            col.markdown(f"""
            <div style='text-align:center;padding:.8rem .4rem;border-radius:10px;
                 background:{"#0f2d1f" if hit else "#161B22"};
                 border:1px solid {"#238636" if hit else "#21262D"}'>
                <div style='font-size:.75rem;font-weight:600;color:#8B949E;margin-bottom:.3rem'>{r["doc_id"].upper()}</div>
                <div style='font-size:1.3rem'>{"✅" if hit else "❌"}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("<div style='margin-top:.8rem'></div>", unsafe_allow_html=True)

        if not found:
            st.markdown("<div style='color:#8B949E;font-size:.85rem;padding:.5rem 0'>Tidak ada dokumen yang relevan.</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div style='color:#3FB950;font-size:.85rem;margin-bottom:.8rem'>{len(found)} dokumen relevan ditemukan</div>", unsafe_allow_html=True)
            for r in found:
                with st.expander(f"✅  {r['doc_id'].upper()}"):
                    st.markdown(f"<div style='color:#CDD9E5;font-size:.9rem;line-height:1.7'>{corpus[r['doc_id']]}</div>", unsafe_allow_html=True)