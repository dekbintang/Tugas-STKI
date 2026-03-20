# 📚 Tugas STKI — Boolean Retrieval Model

> **Mata Kuliah:** Sistem Temu Kembali Informasi (STKI)  
> **Nama:** I Kadek Bintang Adi Bimantara  
> **NIM:** 2405551049  

---

## 📄 Deskripsi

Implementasi **Boolean Retrieval Model** dengan teknik **Incidence Matrix** dan **Inverted Index** menggunakan Python dan Streamlit. Program mendukung query boolean dengan operator AND, OR, NOT, serta kurung `()` dengan operator precedence sesuai materi kuliah.

---

## 📸 Tampilan Aplikasi

**1. Tampilan Corpus Dokumen**

![Tampilan Corpus Dokumen](images/corpus.png)

**2. Tampilan Incidence Matrix**

![Tampilan Incidence Matrix](images/matrix.png)

**3. Tampilan Inverted Index**

![Tampilan Inverted Index](images/inverted_index.png)

**4. Tampilan Input Query**

![Tampilan Input Query](images/query.png)

**5. Tampilan Hasil Pencarian Query**

![Tampilan Hasil Pencarian Query](images/hasil_query.png)

---

## 🗂️ Struktur Project

```
Tugas-STKI/
├── app.py
├── preprocessing.py
├── indexing.py
├── ir_model.py
├── requirements.txt
├── .gitignore
├── images/
└── corpus/
    ├── doc1.txt
    ├── doc2.txt
    ├── doc3.txt
    ├── doc4.txt
    ├── doc5.txt
    ├── doc6.txt
    └── doc7.txt
```

---

## ⚙️ Pre-Processing

| Tahap | Keterangan |
|---|---|
| Tokenisasi | Memecah teks menjadi token/kata |
| Stemming | Mengubah kata ke bentuk dasar menggunakan PySastrawi |
| Stopwords | Tidak digunakan |

---

## 🔍 Fitur

- **Incidence Matrix** — Representasi biner (TFbiner) term x dokumen
- **Inverted Index** — Notasi `<idj, fij, [posisi]>`
- **Boolean Query** — Operator AND, OR, NOT
- **Operator Precedence** — `()` → `NOT` → `AND` → `OR`
- **Langkah Operasi** — Ditampilkan step-by-step seperti materi kuliah

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
Fuzzy OR NOT (Genetik AND Learning)
(Fuzzy OR Optimasi) AND NOT Genetik
```

---

## 🛠️ Teknologi

![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=flat&logo=pandas&logoColor=white)