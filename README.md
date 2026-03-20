# 📚 Sistem Temu Kembali Informasi
### STKI — Information Retrieval Model

---

## 📋 Deskripsi

Program ini mengimplementasikan **Boolean Retrieval Model** dengan teknik **Incidence Matrix** dan **Inverted Index** menggunakan bahasa pemrograman Python dan antarmuka berbasis Streamlit.

---

## 🗂️ Struktur Project

```
stki_project/
├── app.py               # Antarmuka utama (Streamlit)
├── preprocessing.py     # Tokenisasi & Stemming
├── indexing.py          # Incidence Matrix & Inverted Index
├── ir_model.py          # Extended Boolean Model
├── requirements.txt     # Daftar library
└── corpus/
    ├── doc1.txt         # Kecerdasan Buatan
    ├── doc2.txt         # Algoritma Genetika
    ├── doc3.txt         # Jaringan Saraf Tiruan
    ├── doc4.txt         # Sistem Temu Kembali Informasi
    ├── doc5.txt         # Logika Fuzzy
    ├── doc6.txt         # Pemrosesan Bahasa Alami
    └── doc7.txt         # Robotika Cerdas
```

---

## ⚙️ Pre-Processing

| Tahap | Keterangan |
|---|---|
| Tokenisasi | Memecah teks menjadi token/kata |
| Stemming | Mengubah kata ke bentuk dasar menggunakan **PySastrawi** |
| Stopwords | Tidak digunakan |

---

## 🔍 Fitur

- **Incidence Matrix** — Representasi biner (TFbiner) term × dokumen
- **Inverted Index** — Pemetaan term ke daftar dokumen beserta posisi
- **Boolean Query** — Mendukung operator AND, OR, NOT
- **Extended Boolean** — Skor kontinu [0,1] menggunakan P-norm & TF-IDF
- **Ranking Dokumen** — Dokumen diurutkan berdasarkan tingkat relevansi

---

## 🚀 Cara Menjalankan

**1. Install library**
```bash
pip install streamlit pandas PySastrawi
```

**2. Jalankan aplikasi**
```bash
streamlit run app.py
```

**3. Buka browser**
```
http://localhost:8501
```

---

## 🔎 Contoh Query

```
Fuzzy AND Learning
Genetik AND Learning
Fuzzy OR Optimasi
NOT Genetik
```

---

## 🛠️ Teknologi

- Python 3.x
- Streamlit
- PySastrawi
- Pandas