# MODUL PRAKTIKUM PERTEMUAN 2
## Mata Kuliah: Pemrograman Mobile dengan Flutter
### Layout Dasar Flutter: Row, Column, Container, dan Styling

**Program Studi:** Teknik Informatika — Politeknik Negeri Lhokseumawe
**Waktu:** 3 × 50 menit
**Prasyarat:** Mahasiswa telah mengikuti Pertemuan 1 (project starter Flutter, widget, stateless & stateful widget)

---

## A. Tujuan Praktikum

Setelah menyelesaikan praktikum ini, mahasiswa mampu:

1. Menggunakan widget layout `Row` dan `Column` untuk menyusun tampilan.
2. Menggunakan `Container`, `Padding`, dan `SizedBox` untuk mengatur ukuran, jarak, dan dekorasi.
3. Mengatur alignment dan spacing dengan `mainAxisAlignment`, `crossAxisAlignment`, dan `Expanded`.
4. Menerapkan styling dasar: warna, font, ikon, dan `TextStyle`.
5. Membangun tampilan aplikasi nyata sederhana (kartu profil / halaman menu).

---

## B. Ringkasan Materi

Pada Pertemuan 1 kita sudah belajar bahwa **semua tampilan di Flutter adalah widget**. Kali ini kita fokus pada **widget layout**, yaitu widget yang tugasnya mengatur posisi widget lain.

### B.1 Column dan Row

| Widget | Arah penyusunan | Sumbu utama (main axis) | Sumbu silang (cross axis) |
|---|---|---|---|
| `Column` | Vertikal (atas → bawah) | Vertikal | Horizontal |
| `Row` | Horizontal (kiri → kanan) | Horizontal | Vertikal |

```dart
Column(
  children: [
    Text('Baris 1'),
    Text('Baris 2'),
    Text('Baris 3'),
  ],
)

Row(
  children: [
    Icon(Icons.star),
    Icon(Icons.star),
    Icon(Icons.star),
  ],
)
```

### B.2 Alignment dan Spacing

```dart
Column(
  mainAxisAlignment: MainAxisAlignment.spaceEvenly, // sepanjang sumbu utama
  crossAxisAlignment: CrossAxisAlignment.center,    // sepanjang sumbu silang
  children: [ ... ],
)
```

Nilai `MainAxisAlignment` yang sering dipakai: `start`, `center`, `end`, `spaceBetween`, `spaceAround`, `spaceEvenly`.

### B.3 Expanded dan Flexible

`Expanded` membuat child mengambil **sisa ruang** yang tersedia di dalam Row/Column:

```dart
Row(
  children: [
    Expanded(child: Container(color: Colors.red)),   // 1 bagian
    Expanded(flex: 2, child: Container(color: Colors.blue)), // 2 bagian
  ],
)
```

### B.4 Container, Padding, dan SizedBox

```dart
Container(
  width: 120,
  height: 120,
  padding: const EdgeInsets.all(16),
  margin: const EdgeInsets.only(top: 8),
  decoration: BoxDecoration(
    color: Colors.teal,
    borderRadius: BorderRadius.circular(12),
    boxShadow: const [
      BoxShadow(color: Colors.black26, blurRadius: 6, offset: Offset(0, 3)),
    ],
  ),
  child: const Text('Halo'),
)
```

- `Padding` → hanya untuk jarak di dalam.
- `SizedBox(width: w, height: h)` → jarak kosong antar widget (alternatif yang ringan).

### B.5 Styling Teks

```dart
Text(
  'Politeknik Negeri Lhokseumawe',
  style: TextStyle(
    fontSize: 18,
    fontWeight: FontWeight.bold,
    color: Colors.teal[800],
    letterSpacing: 1.2,
  ),
)
```

---

## C. Persiapan

1. Flutter SDK sudah terinstal dan `flutter doctor` tanpa error kritis (sudah dicek pada Pertemuan 1).
2. IDE (VS Code / Android Studio) terbuka.
3. Emulator atau perangkat fisik tersambung (atau gunakan Chrome untuk Flutter Web).
4. Buat project baru:

```bash
flutter create pnl_layout
cd pnl_layout
flutter run
```

---

## D. Praktikum Terpandu

### Latihan 1 — Mengenal Column (15 menit)

Ganti seluruh isi `lib/main.dart` dengan kode berikut:

```dart
import 'package:flutter/material.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        appBar: AppBar(title: const Text('Latihan 1 - Column')),
        body: Column(
          children: [
            Container(width: 100, height: 100, color: Colors.red),
            Container(width: 100, height: 100, color: Colors.green),
            Container(width: 100, height: 100, color: Colors.blue),
          ],
        ),
      ),
    );
  }
}
```

**Tugas mahasiswa:**
1. Jalankan dan amati posisi ketiga kotak.
2. Ubah `Column` menjadi `Row`. Apa yang berubah?
3. Tambahkan `mainAxisAlignment: MainAxisAlignment.spaceEvenly` pada Column. Amati perbedaannya.
4. Tambahkan `crossAxisAlignment: CrossAxisAlignment.end`. Apa efeknya?
5. Bungkus salah satu Container dengan `Expanded(...)` lalu jalankan. Jelaskan apa yang terjadi pada catatan laporan.

> **Catatan asisten:** error "RenderFlex overflowed" (garis kuning-hitam) biasanya muncul jika total tinggi child Column melebihi layar. Tunjukkan gejala ini sengaja di Latihan 3 agar mahasiswa terbiasa membacanya.

### Latihan 2 — Styling dengan Container dan Text (20 menit)

```dart
import 'package:flutter/material.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        appBar: AppBar(title: const Text('Latihan 2 - Container & Text')),
        body: Center(
          child: Container(
            padding: const EdgeInsets.all(24),
            margin: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(16),
              border: Border.all(color: Colors.teal, width: 2),
              boxShadow: const [
                BoxShadow(color: Colors.black26, blurRadius: 8, offset: Offset(0, 4)),
              ],
            ),
            child: const Text(
              'Selamat Datang di\nPoliteknik Negeri Lhokseumawe',
              textAlign: TextAlign.center,
              style: TextStyle(
                fontSize: 20,
                fontWeight: FontWeight.bold,
                color: Colors.teal,
              ),
            ),
          ),
        ),
      ),
    );
  }
}
```

**Tugas mahasiswa:**
1. Ubah warna, radius sudut, dan tebal border sesuai selera.
2. Tambahkan `gradient` pada `BoxDecoration` (petunjuk: `LinearGradient(colors: [...])`).
3. Buat teks kedua di bawah teks utama (petunjuk: ubah `child` menjadi `Column`).

### Latihan 3 — Layout Kombinasi: Baris Menu (25 menit)

Susun tiga "tombol menu" berdampingan menggunakan `Row` + `Expanded`, masing-masing berisi `Icon` di atas dan `Text` di bawah (gunakan `Column` di dalam tiap tombol).

```dart
import 'package:flutter/material.dart';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  Widget menuItem(IconData icon, String label, Color color) {
    return Expanded(
      child: Container(
        margin: const EdgeInsets.all(8),
        padding: const EdgeInsets.symmetric(vertical: 20),
        decoration: BoxDecoration(
          color: color.withOpacity(0.15),
          borderRadius: BorderRadius.circular(12),
        ),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, size: 40, color: color),
            const SizedBox(height: 8),
            Text(label, style: TextStyle(color: color, fontWeight: FontWeight.bold)),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        appBar: AppBar(title: const Text('Latihan 3 - Baris Menu')),
        body: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Row(
                children: [
                  menuItem(Icons.home, 'Beranda', Colors.teal),
                  menuItem(Icons.school, 'Akademik', Colors.orange),
                  menuItem(Icons.person, 'Profil', Colors.indigo),
                ],
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

**Pembahasan bersama dosen:**
- Perhatikan fungsi `menuItem(...)` — ini cara sederhana **mengekstrak widget yang berulang** agar kode tidak disalin-tempel. Sampaikan bahwa ini jembatan menuju materi pembuatan widget kustom.
- Coba tambahkan tombol ke-4 dan ke-5 dalam satu Row. Apa yang terjadi? Kaitkan dengan konsep `Expanded` dan lebar layar.

### Latihan 4 — Proyek Mini: Kartu Profil (30 menit)

Bangun tampilan **Kartu Profil Mahasiswa** dengan ketentuan berikut (mahasiswa mengerjakan mandiri, dosen/asisten berkeliling membimbing):

**Ketentuan wajib:**
1. `AppBar` berjudul "Profil Mahasiswa".
2. Foto profil berbentuk lingkaran di bagian atas, tengah layar. Gunakan `CircleAvatar` (boleh `backgroundImage: NetworkImage(...)` atau `child: Icon(Icons.person)` jika tanpa internet).
3. Nama lengkap dengan font besar & tebal, diikuti NIM dan program studi dengan font lebih kecil.
4. Sebuah `Container` berisi tiga info berjejer horizontal (menggunakan `Row` + `Expanded`): **Semester**, **IPK**, **SKS**. Masing-masing tampil sebagai angka besar di atas label kecil (Column di dalam tiap kolom).
5. Seluruh konten diletakkan di dalam `Card` atau `Container` dengan `borderRadius` dan `boxShadow`.
6. Beri jarak antar elemen dengan `SizedBox`.

**Struktur pohon widget yang disarankan (hint):**

```
Scaffold
└── Column
    ├── CircleAvatar
    ├── Text (Nama)
    ├── Text (NIM - Prodi)
    └── Container (kartu info)
        └── Row
            ├── Expanded → Column (angka + label)
            ├── Expanded → Column (angka + label)
            └── Expanded → Column (angka + label)
```

**Nilai tambah (opsional):**
- Tambahkan Row berisi ikon media sosial (Instagram, GitHub, email) di bagian bawah kartu.
- Terapkan warna tema kampus.

---

## E. Tugas Mandiri (Dikumpulkan)

Bangun aplikasi **"Menu Makanan"** satu halaman dengan ketentuan:

1. `AppBar` berjudul nama kafe/rumah makan pilihan mahasiswa.
2. Minimal **4 item menu**, masing-masing berbentuk `Card` berisi:
   - Ikon/gambar makanan (kiri),
   - Nama makanan + deskripsi singkat (tengah, Column),
   - Harga (kanan, teks tebal).
   - Susunan menggunakan `Row` dan `Column` (boleh memakai `ListTile` jika sudah dipelajari mandiri — jelaskan di laporan).
3. Terapkan minimal: `borderRadius`, `boxShadow`, dua warna tema yang konsisten, dan penggunaan `Expanded` atau `SizedBox` untuk kerapian.
4. **Pengumpulan:** file `main.dart` + screenshot hasil running (emulator/HP) + laporan singkat (PDF) yang menjawab pertanyaan pada setiap Latihan 1–3. Kumpulkan sebelum pertemuan berikutnya.

---

## F. Rubrik Penilaian (Total 100)

| Aspek | Bobot |
|---|---|
| Latihan 1–3 selesai dan jawaban pertanyaan benar | 25 |
| Latihan 4 (Kartu Profil) sesuai semua ketentuan wajib | 35 |
| Tugas Mandiri: kelengkapan ketentuan | 25 |
| Tugas Mandiri: kerapian kode & kreativitas tampilan | 15 |

---

## G. Troubleshooting Umum

| Gejala | Penyebab umum | Solusi |
|---|---|---|
| Garis kuning-hitam "overflowed by X pixels" | Isi Row/Column melebihi ruang | Bungkus dengan `Expanded`, kurangi ukuran, atau gunakan `SingleChildScrollView` |
| Perubahan kode tidak muncul | Lupa hot reload | Tekan `r` di terminal / ikon ⚡ di IDE |
| Kotak tidak berwarna | `color` ditaruh di `Container` bersama `decoration` | Pindahkan `color` ke dalam `BoxDecoration` |
| Error setelah edit | Kurung kurawal/kurung tidak seimbang | Manfaatkan auto-format (`Shift+Alt+F`) dan indentasi |

---

*Modul ini disusun untuk praktikum Pertemuan 2. Silakan sesuaikan waktu dan tingkat kesulitan dengan kondisi kelas.*
