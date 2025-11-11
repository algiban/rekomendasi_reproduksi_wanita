# Demo Web: Hybrid Recommender (Medis + Non-Medis)

Aplikasi web sederhana berbasis **Flask** untuk uji coba sistem rekomendasi keluhan kesehatan reproduksi.
- Input: teks keluhan (+ opsional profil).
- Output: Top-N rekomendasi *non-medis* dari dataset profil, serta **rekomendasi medis yang diambil dari dataset penanganan**.
- Menampilkan skor kemiripan (cosine similarity) berbasis TF-IDF.

## Cara Menjalankan

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

export FLASK_APP=app.py  # Windows: set FLASK_APP=app.py
python app.py
# buka http://127.0.0.1:5000
```

## Format Dataset

- **Profil** (xlsx/csv): kolom wajib `keluhan_inti`; opsional `profil_pengguna`, `rekomendasi_non-medis`.
- **Penanganan** (xlsx/csv): kolom wajib `keluhan_inti`, `penanganan`.

> Semua teks akan dinormalisasi ke huruf kecil.

## Catatan
- Model TF-IDF di-*fit* pada korpus `keluhan_inti` dari dataset profil.
- Skor kemiripan dihitung dari keluhan input vs korpus.
- Rekomendasi medis **selalu** diambil dari dataset `penanganan` dengan *merge* berdasarkan `keluhan_inti`.# rekomendasi_reproduksi_wanita
