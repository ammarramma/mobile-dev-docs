# Pandoc & WeasyPrint Template Experiments (test-8)

Folder ini berisi hasil eksperimen variasi template CSS dan Pandoc untuk kompilasi dokumen **Laprak_Mobile_8.md** menjadi PDF dan HTML menggunakan engine **WeasyPrint** (Python venv: `/home/ramma/.venv`).

---

## 🎨 Variasi Template yang Dibuat

| Template | File CSS | File PDF | File HTML | Karakteristik Desain |
|---|---|---|---|---|
| **1. Modern Teal** *(Rekomendasi)* | `style-modern-teal.css` | `Laprak_8_ModernTeal.pdf` | `Laprak_8_ModernTeal.html` | Nuansa Flutter & Material Teal (`#0f766e`), font sans-serif modern, blok kode gelap dengan aksen mint, kartu gambar berbayang halus, header & footer halaman dinamis (`@top-left`, `@top-right`, `@bottom-right`). |
| **2. Nordic Indigo** | `style-nordic-indigo.css` | `Laprak_8_NordicIndigo.pdf` | `Laprak_8_NordicIndigo.html` | Minimalis, editorial, tipografi Cantarell/DejaVu Sans dengan warna aksen Indigo (`#4338ca`), garis pemisah tipis elegan, penomoran halaman tengah klasik. |
| **3. Academic Formal** | `style-academic-formal.css` | `Laprak_8_AcademicFormal.pdf` | `Laprak_8_AcademicFormal.html` | Standar jurnal teknik klasik (font DejaVu Serif), heading kapital rapi, blok kode monokromatik terang dengan border halus, format sitasi formal. |
| **4. Original Style** | `../style/laprak_style.css` | `Laprak_8_OriginalStyle.pdf` | `Laprak_8_OriginalStyle.html` | Gaya bawaan dari Laporan 7 sebelumnya (Muted/Clean gray). |

---

## 🚀 Cara Menghasilkan Ulang Dokumen

### Menjalankan Pandoc dengan WeasyPrint (Fish Shell):
```fish
source /home/ramma/.venv/bin/activate.fish

# Template 1: Modern Teal (PDF)
pandoc ../Laprak_Mobile_8.md -o Laprak_8_ModernTeal.pdf \
  --css=style-modern-teal.css \
  --pdf-engine=weasyprint \
  --syntax-highlighting=breezedark \
  --standalone --toc --toc-depth=2

# Template 1: Modern Teal (HTML Mandiri)
pandoc ../Laprak_Mobile_8.md -o Laprak_8_ModernTeal.html \
  --css=style-modern-teal.css \
  --syntax-highlighting=breezedark \
  --standalone --embed-resources --toc --toc-depth=2
```

### Menggunakan Skrip Otomatis `build.sh`:
Skrip `build.sh` sudah diperbarui sehingga otomatis mendeteksi WeasyPrint di `/home/ramma/.venv`:
```bash
./build.sh Laprak_Mobile_8.md pdf --toc
```
Hasil PDF resmi akan masuk ke folder `result/Laprak_Mobile_8.pdf`.
