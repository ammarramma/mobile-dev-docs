# AGENTS.md — Workflow Laporan Praktikum (Markdown → PDF)

Dokumen ini adalah panduan untuk agent CLI (dan manusia) yang bekerja di folder ini.
Kalau memakai Claude Code, salin/ganti nama file ini menjadi `CLAUDE.md`.

## 1. Tujuan

Pemilik: **Ammar**, kelas TI3B, mata kuliah Praktikum Pemrograman Mobile (Flutter).
Laporan ditulis dalam **Bahasa Indonesia**, dibuat sebagai Markdown, lalu dikonversi ke PDF.

```
Laprak_Mobile_N.md  --pandoc-->  HTML  --weasyprint + style/laprak_style.css-->  result/Laprak_Mobile_N.pdf
```

Markdown **tidak punya konsep halaman**. Halaman baru muncul dari CSS saat weasyprint
menata HTML. Karena itu:

> **Isi diubah di `.md`. Tampilan/halaman diubah di `style/laprak_style.css`.**
> Sebelum mengedit, tanya: "ini urusan isi atau tampilan?"

## 2. Struktur folder

```
mobile/
├── AGENTS.md                  ← file ini
├── build.sh                   ← satu-satunya cara membuat PDF/HTML
├── style/laprak_style.css     ← semua aturan tampilan & halaman
├── template/Laprak_TEMPLATE.md← kerangka laporan baru
├── Laprak_Mobile_N.md         ← SUMBER laporan (yang diedit)
├── images/
│   ├── latihan1/…             ← screenshot per latihan (huruf kecil semua)
│   └── latihan2/…
├── modul/                     ← modul dosen (hanya dibaca, jangan diubah)
└── result/                    ← hasil build (PDF/HTML), boleh dihapus kapan saja
```

File `*_OPTIMIZED.md`, `00_START_HERE.txt`, `ANALYSIS_REPORT.md`, `QUICK_REFERENCE.md`,
`README_ANALYSIS.md`, `PANDOC_CONVERSION_GUIDE.md` adalah sisa lama. **Abaikan.**
Satu laporan = satu file sumber `.md`. Jangan membuat varian salinan.

## 3. Aturan emas

**Wajib**

1. Bangun hanya lewat `./build.sh` (jangan menjalankan pandoc manual dengan opsi acak).
2. Jalankan `./build.sh <file>.md check` setelah mengedit `.md`, sebelum build PDF.
3. Gambar memakai Markdown murni: `![Caption](images/latihanX/nama.png)`.
4. Pindah halaman dan jarak kosong memakai fenced div (bagian 4), bukan trik enter.
5. Jaga isi laporan: jangan mengubah hasil percobaan, angka, nama file gambar, atau
   identitas tanpa diminta. Placeholder seperti `[Isi dengan jumlah yang didapat]`
   hanya boleh diisi bila datanya diberikan pemilik.

**Dilarang**

| Jangan | Alasan | Gunakan |
|---|---|---|
| Baris `---` | Pemilik tidak suka garis; di PDF disembunyikan CSS | Heading / `::: pagebreak` |
| `\pagebreak`, `\newpage` | Perintah LaTeX, tidak jalan di weasyprint | `::: pagebreak` |
| `<img …>`, `<br>` | Tidak konsisten antar mesin | `![caption](path)`, `::: spacer` |
| `## Daftar Isi` manual | Anchor pandoc ≠ GitHub, memicu ERROR | `./build.sh f.md pdf --toc` |
| Enter kosong berulang untuk jarak | Diabaikan Markdown | `::: spacer` |
| Menaruh `---` di baris pertama file | Dibaca sebagai blok YAML | (tidak perlu) |
| Mengubah CSS demi memperbaiki isi | Mencampur isi & tampilan | Edit `.md` |

## 4. Cheatsheet sintaks

### Enter = baris baru
Build memakai `markdown+hard_line_breaks`: **1× enter = 1 baris baru**, persis seperti
yang diketik. Tidak perlu dua spasi di akhir baris. Paragraf baru tetap pakai baris kosong.
Baris kosong ekstra tidak menambah jarak (pakai `::: spacer`).

### Pindah halaman
Default: setiap `##` (h2) **mulai di halaman baru**. Hasilnya, bab-bab terpisah rapi.

```markdown
## Pendahuluan {.lanjut}      ← h2 yang TIDAK pindah halaman (lanjut dari atas)

::: pagebreak                 ← paksa pindah halaman di titik ini
:::
```

### Jarak kosong

```markdown
::: spacer                    ← ± 1,5 baris
:::

::: spacer-lg                 ← ± 3 baris
:::
```

### Gambar
Teks di dalam `[...]` otomatis menjadi **caption** di bawah gambar.

```markdown
![Gambar 1.1 — Status code 200 dan JSON mentah](images/latihan1/masalah1.png)
```

Dua gambar berdampingan (**wajib dipisah baris kosong**):

```markdown
::: side-by-side
![Tanpa await](images/latihan1/masalah4.png)

![Dengan await](images/latihan1/masalah4.5.png)
:::
```

### Blok lain

```markdown
::: identitas      ← kotak Nama/NIM/Kelas (lihat template)
:::

::: keep           ← jaga isinya tetap satu halaman (kode pendek, tabel kecil)
:::

::: center         ← rata tengah
:::
```

### Kode
Selalu sebutkan bahasa agar berwarna:

````markdown
```dart
final response = await http.get(Uri.parse(url));
```
````

## 5. Hierarki heading (baku)

| Level | Fungsi | Contoh |
|---|---|---|
| `#` | Judul laporan (hanya **satu**) | `# Laporan Praktikum Pemrograman Mobile` |
| `##` | Bab / latihan (pindah halaman otomatis) | `## Latihan 1: …`, `## Kesimpulan` |
| `###` | Sub-percobaan | `### 1.1 Verifikasi Koneksi API` |
| `####` | Bagian tetap tiap percobaan | `#### Masalah` |

Pola isi tiap percobaan (`###`), urutan tetap:

`#### Masalah` → `#### Tugas` → `#### Kode Implementasi` → `#### Hasil Eksekusi` → `#### Pembahasan`

## 6. Perintah

```bash
./build.sh Laprak_Mobile_7.md check        # cek gambar hilang + gaya penulisan
./build.sh Laprak_Mobile_7.md html         # preview cepat → result/*.html (buka di browser)
./build.sh Laprak_Mobile_7.md              # PDF → result/Laprak_Mobile_7.pdf
./build.sh Laprak_Mobile_7.md pdf --toc    # PDF + daftar isi otomatis
```

Catatan `--toc`: daftar isi dibuat pandoc dan diletakkan **sebelum** judul `#`.
Laporan 10–25 halaman biasanya tidak membutuhkannya.

Prasyarat: `pandoc`, `weasyprint` (≥ 53). Cek: `pandoc -v && weasyprint --version`.

## 7. Alur kerja agent

1. Baca permintaan, tentukan: **isi** (edit `.md`) atau **tampilan** (edit `.css`).
2. Edit sesuai aturan bagian 3–5. Perubahan sekecil mungkin.
3. `./build.sh <file>.md check` — perbaiki semua `x hilang` dan `!` sebelum lanjut.
4. `./build.sh <file>.md html` untuk melihat hasil cepat; bila bagus, build PDF.
5. Laporkan: file apa yang diubah, apa yang diubah, dan hasil `check`.
   Jangan membuat file ringkasan/analisis baru di folder utama.

Untuk laporan baru: `cp template/Laprak_TEMPLATE.md Laprak_Mobile_N.md`, lalu isi dari modul
di `modul/` (hanya baca). Tugas dan pertanyaan di laporan mengikuti urutan modul.

## 8. Migrasi file lama (`Laprak_Mobile_7.md` dsb.)

Terapkan sekali bila menemukan pola lama:

- [ ] Hapus semua baris `---`.
- [ ] Hapus `## Daftar Isi` manual.
- [ ] Naikkan hierarki: `# Latihan N` → `## Latihan N`; `## 1.1` → `### 1.1`; `### Masalah` → `#### Masalah`.
- [ ] Ganti `<img … width="48%"> <img …>` → blok `::: side-by-side` (dua gambar, dipisah baris kosong).
- [ ] Caption gambar: pindahkan teks `*Gambar 1.1: …*` ke dalam `![…]`.
- [ ] Beri `{.lanjut}` pada `## Pendahuluan` agar ikut halaman judul.
- [ ] Hapus dua spasi di akhir baris (tidak perlu lagi).

## 9. Troubleshooting

| Gejala | Penyebab | Solusi |
|---|---|---|
| `Could not fetch resource images/…` | File tidak ada / beda huruf besar-kecil / folder salah | `./build.sh f.md check`; Linux membedakan `Masalah1.png` ≠ `masalah1.png` |
| PDF kecil (~100 KB) padahal banyak gambar | Gambar tidak ikut masuk | Sama seperti di atas |
| `--resource-path=".:images"` membuat gagal | Path di `.md` sudah diawali `images/` | `build.sh` sudah memakai `--resource-path=.` |
| `No anchor #… for internal URI` | Daftar isi manual | Hapus; pakai `--toc` |
| Enter tidak jadi baris baru | Build tidak lewat `build.sh` | Pakai `build.sh` (membawa `+hard_line_breaks`) |
| Halaman kosong di tengah | `::: pagebreak` tepat sebelum `##` | Hapus salah satunya (`##` sudah pindah halaman) |
| Heading menggantung di dasar halaman | — | Sudah dicegah CSS (`break-after: avoid`); bila tetap terjadi, tambah `::: pagebreak` sebelumnya |
| Kode terpotong ke kanan | CSS lama | Sudah `pre-wrap` di CSS baru |
| `WARNING: Ignored user-select: none` | CSS bawaan highlight pandoc | Aman, abaikan |
| Dua gambar tidak berdampingan | Tidak dipisah baris kosong / div salah tulis | Lihat contoh `side-by-side` bagian 4 |
| Perubahan CSS tidak terlihat | Cache pratinjau | Build ulang; buka HTML dengan refresh keras |

## 10. Identitas default (untuk template)

```
Nama: Ammar
NIM: 2024573010129
Kelas: TI3B
Mata Kuliah: Praktikum Pemrograman Mobile (With Flutter)
Dosen: Muhammad Rizka
```
