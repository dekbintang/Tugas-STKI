# Boolean IR Engine

Mesin pencari teks berbasis Boolean Retrieval Model untuk korpus Bahasa Indonesia. Mengimplementasikan Inverted Index, Term-Document Incidence Matrix, dan parser ekspresi boolean rekursif dengan antarmuka web Streamlit.

## Tech Stack

- **Bahasa:** Python 3.10+
- **UI:** Streamlit
- **NLP:** PySastrawi (stemming Bahasa Indonesia)
- **Data:** Pandas

## Fitur

- Query boolean dengan operator `AND`, `OR`, `NOT`, dan tanda kurung bertingkat
- Inverted Index dan Incidence Matrix yang dibangun dari nol
- Pipeline preprocessing: tokenisasi, normalisasi, stemming Sastrawi
- Visualisasi langkah evaluasi vektor bitwise per sub-ekspresi

## Contoh Query

| Query | Logika |
| :--- | :--- |
| `fuzzy AND clustering` | Dokumen memuat kedua kata |
| `genetik OR neural` | Dokumen memuat salah satu |
| `NOT optimasi` | Dokumen tidak memuat kata tersebut |
| `fuzzy OR NOT (genetik AND learning)` | Kombinasi bersarang |

## Struktur

```
├── app.py              # Aplikasi Streamlit
├── indexing.py          # Inverted Index & Incidence Matrix
├── ir_model.py          # Parser AST Boolean Query & logika bitwise
├── preprocessing.py     # Tokenisasi & stemming Sastrawi
├── corpus/              # Dokumen sumber
├── docs/                # Spesifikasi teknis
└── requirements.txt
```

## Setup

```bash
git clone https://github.com/dekbintang/Tugas-STKI.git
cd Tugas-STKI
python -m venv venv
.\venv\Scripts\activate     # Windows
pip install -r requirements.txt
streamlit run app.py
```

## Lisensi

[MIT](LICENSE)
