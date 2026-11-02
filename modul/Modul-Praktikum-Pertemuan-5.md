# MODUL PRAKTIKUM PERTEMUAN 5
## Mata Kuliah: Pemrograman Mobile dengan Flutter
### Database Online dengan Supabase: Membuat, Membaca, Mengubah, dan Menghapus Data (CRUD)

**Program Studi:** Teknik Informatika — Politeknik Negeri Lhokseumawe
**Waktu:** 3 × 50 menit
**Prasyarat:** Mahasiswa telah mengikuti Pertemuan 4 (package `http`, JSON, model class + `fromJson`, `FutureBuilder`, penanganan keadaan loading/error)

---

## Catatan Pembuka — Baca Sebelum Praktikum

### 1. Modul ini dikerjakan sebagai satu project yang dikembangkan bertahap

Buat project `pnl_supabase` **sekali saja**, lalu kembangkan `lib/main.dart` dari Latihan 1 sampai Latihan 4. Setiap latihan menambah atau mengubah sebagian kode latihan sebelumnya — bukan membuat project baru.

```
pnl_supabase/
├── lib/
│   ├── config.dart     ← URL + publishable key (diisi sekali, bagian C.3)
│   └── main.dart       ← seluruh kode latihan
└── pubspec.yaml
```

| Latihan | Perlakuan terhadap kode |
|---|---|
| 1 | Membuat kerangka: inisialisasi, model, `ambilDaftarMenu()`, daftar menu |
| 2 | **Menambah** halaman formulir, satu method `insert`, dan tombol `+` |
| 3 | **Menambah** tiga method (`update`, `delete`, `ubahKetersediaan`), mengubah formulir menjadi dua mode, mengganti `itemBuilder` |
| 4 | **Mengganti** seluruh isi `_HalamanKatalogState` (dari `FutureBuilder` ke `StreamBuilder`) |

> **Bila kelas Anda lebih nyaman memakai project terpisah per latihan**, hal itu tetap dapat dilakukan dengan satu penyesuaian penting: setiap project baru harus memuat ulang inisialisasi `Supabase.initialize()`, model `MenuItem`, dan `lib/config.dart`. Untuk Latihan 3 dan 4, salin dulu hasil latihan sebelumnya agar tidak menulis ulang dari awal.

### 2. Pembagian waktu (3 × 50 menit)

| Sesi | Isi |
|---|---|
| 1 | Bagian B (ringkasan materi) + Latihan 1 |
| 2 | Latihan 2 + Latihan 3 |
| 3 | Latihan 4 + pembahasan Tugas Mandiri |

Bila sesi 1 habis untuk pembuatan akun dan project, pindahkan Latihan 3 ke sesi 3 dan jadikan Latihan 4 sebagai tugas rumah. **Jangan memangkas Latihan 1**, karena tabel dan koneksi yang disiapkan di sana dipakai oleh seluruh latihan berikutnya.

### 3. Persiapan yang wajib selesai sebelum praktikum dimulai

1. Akun Supabase sudah dibuat dan project sudah aktif.
2. Skrip SQL pada bagian C.2 sudah dijalankan, dan 5 baris data contoh terlihat di **Table Editor**.
3. URL project dan publishable key sudah dicatat.
4. Project Flutter sudah dibuat dan package `supabase_flutter` sudah terpasang.

Waktu praktikum yang dialokasikan untuk keempat langkah tersebut adalah **nol menit**. Bila kelas belum siap, seluruh sesi 1 akan habis untuk administrasi. Untuk kelas dengan koneksi terbatas, sediakan satu project contoh yang kuncinya dibagikan agar semua mahasiswa dapat langsung fokus ke bagian kode.

> Praktikum ini juga membutuhkan **koneksi internet yang stabil sepanjang sesi**, karena hampir setiap langkah berinteraksi dengan server. Bila koneksi terputus di tengah latihan, aplikasi akan menampilkan pesan error — ini justru momen yang baik untuk memperlihatkan bahwa penanganan error yang dibuat di Latihan 2 benar-benar bekerja.

### 4. Peringatan keselamatan — sampaikan secara lisan sebelum praktikum

- **Latihan 3 tugas nomor 4 sengaja berbahaya.** Mahasiswa diminta menghapus filter `.eq('id', id)` sehingga **seluruh isi tabel terhapus**. Hanya boleh dilakukan pada tabel latihan `menu`, dan pastikan data contoh dapat dibuat ulang (skrip bagian C.2 dapat dijalankan ulang).
- **Policy `using (true)`** yang dipakai hari ini berarti tabel terbuka bagi siapa pun yang memiliki publishable key. Ini **khusus untuk latihan** dan akan dipersempit pada pertemuan berikutnya setelah fitur login tersedia.
- **Kunci *secret* / *service_role* tidak boleh** dimasukkan ke kode aplikasi, laporan, maupun repositori. Bila sudah terjadi, ganti kuncinya dari dashboard.

### 5. Tingkat kesulitan

Ini modul terberat di antara Pertemuan 1–5, karena mahasiswa sekaligus berhadapan dengan tiga hal baru: konsep database relasional, aturan keamanan (RLS), dan pola `Stream` untuk data realtime. Bila waktu sesi terbatas, prioritas yang harus tetap tersampaikan adalah **Latihan 1 dan Latihan 2** — keduanya sudah cukup untuk menunjukkan bahwa aplikasi dapat membaca dan menulis ke database sungguhan. Latihan 3, Latihan 4, dan fitur realtime dapat diberikan sebagai tugas rumah tanpa kehilangan inti materi.

---

## A. Tujuan Praktikum

Setelah menyelesaikan praktikum ini, mahasiswa mampu:

1. Menjelaskan perbedaan antara **mengonsumsi API publik** (Pertemuan 4) dengan **mengelola database milik sendiri**.
2. Menjelaskan peran database, Data API, dan kunci akses (publishable key vs secret key) pada arsitektur Backend as a Service (BaaS).
3. Membuat tabel di database Supabase melalui SQL Editor dan mengaktifkan Row Level Security beserta policy-nya.
4. Menginisialisasi `supabase_flutter` dan menghubungkan aplikasi ke project Supabase.
5. Melakukan operasi **Create, Read, Update, Delete (CRUD)** pada tabel Supabase dari aplikasi Flutter.
6. Menggunakan filter dan pengurutan (`.eq()`, `.order()`, `.ilike()`, `.limit()`) pada query database.
7. Menampilkan data yang berubah secara **realtime** menggunakan `.stream()` dan `StreamBuilder`.
8. Menjelaskan mengapa kunci *publishable* boleh disertakan di aplikasi, sedangkan kunci *secret* tidak boleh.

---

## B. Ringkasan Materi

### B.1 Keterbatasan Modul Pertemuan 4

Pada Pertemuan 4, aplikasi kita **hanya bisa membaca** data dari server orang lain. Kita tidak bisa:

- menambah menu baru dari dalam aplikasi,
- mengubah harga,
- menghapus data yang salah,
- membuat struktur data sendiri dengan kolom sesuai kebutuhan.

Semua itu memerlukan **database milik sendiri**. Di situlah Supabase masuk.

| Aspek | Pertemuan 4 (API publik) | Pertemuan 5 (database sendiri) |
|---|---|---|
| Arah data | Hanya baca (GET) | Baca **dan** tulis (SELECT/INSERT/UPDATE/DELETE) |
| Struktur data | Ditentukan pemilik API | Ditentukan kita sendiri |
| Penyimpanan | Data milik orang lain | Data milik kita |
| Keamanan | Tidak relevan (data publik) | Wajib diatur (RLS + policy) |

### B.2 Apa Itu Supabase

Supabase adalah layanan **Backend as a Service (BaaS)**: kita tidak perlu membangun dan mengelola server sendiri, cukup menyewa bagian backend yang kita perlukan. Yang paling penting dipahami mahasiswa:

- Di bawah Supabase ada **PostgreSQL**, yaitu database relasional sungguhan (bukan database khusus/NoSQL).
- Supabase menyediakan **Data API** di atas Postgres. Artinya, kita bisa mengakses tabel lewat HTTP tanpa menulis kode backend.
- SDK resmi tersedia untuk Flutter, sehingga dari Dart kita langsung menulis `select()`, `insert()`, `update()`, `delete()` — mirip SQL, tetapi dalam bentuk method Dart.

**Ringkasan SQL ↔ method Dart:**

| Perintah SQL | Method Dart (`supabase_flutter`) |
|---|---|
| `SELECT * FROM menu` | `supabase.from('menu').select()` |
| `SELECT * FROM menu WHERE kategori = 'Minuman'` | `supabase.from('menu').select().eq('kategori', 'Minuman')` |
| `SELECT * FROM menu ORDER BY nama` | `supabase.from('menu').select().order('nama')` |
| `INSERT INTO menu (...) VALUES (...)` | `supabase.from('menu').insert({...})` |
| `UPDATE menu SET harga=... WHERE id=1` | `supabase.from('menu').update({...}).eq('id', 1)` |
| `DELETE FROM menu WHERE id=1` | `supabase.from('menu').delete().eq('id', 1)` |

**Alternatif lain yang perlu diketahui mahasiswa (tanpa perlu dicoba hari ini):** Firebase (Google, database NoSQL dan ekosistem paling luas), Appwrite (open source, dapat dihosting sendiri), atau backend buatan sendiri (mis. Laravel/Express + MySQL). Supabase dipilih untuk praktikum ini karena memakai SQL standar yang sudah dikenal dari mata kuliah basis data, gratis untuk skala praktikum, dan memiliki SDK Flutter resmi. Prinsip yang dipelajari hari ini — memodelkan data, CRUD, dan mengatur hak akses — berlaku di semua pilihan tersebut.

### B.3 Anatomi Sebuah Project Supabase

```
            Dashboard Supabase (pengajar/mahasiswa)
            ├── Table Editor   → melihat/menyunting data
            ├── SQL Editor     → menjalankan perintah SQL
            └── Connect        → URL + kunci akses
                       │
                       │ (URL + publishable key dimasukkan ke aplikasi)
                       ▼
   Aplikasi Flutter ──HTTP──► Data API (PostgREST) ──► PostgreSQL
                                    ▲
                        Row Level Security (RLS)
                        menentukan baris mana yang boleh
                        dibaca/ditulis oleh siapa
```

Tiga hal yang wajib diingat dari gambar di atas:

1. Aplikasi berbicara ke **Data API**, bukan ke database secara langsung.
2. **RLS** adalah pengaman yang berada **di dalam database**, bukan di dalam aplikasi. Jadi walaupun kunci disalin orang lain, isi database tetap terlindungi.
3. Kunci aplikasi (*publishable key*) aman disertakan dalam aplikasi client, karena hanya berfungsi sebagai identitas, bukan pemberi izin penuh.

### B.4 Tiga Jenis Kunci dan Perannya

| Kunci | Ditulis di mana | Kemampuan | Boleh disertakan di aplikasi? |
|---|---|---|---|
| **Publishable key** (dulu disebut *anon key*) | Dalam aplikasi Flutter | Hanya sejauh yang diizinkan RLS | **Ya** — memang untuk aplikasi client |
| **Secret key** (dulu disebut *service_role key*) | Hanya di server/backend | Menembus RLS, akses penuh | **TIDAK PERNAH** |
| **Kunci database langsung** (password Postgres) | Hanya di server | Akses penuh ke database | **TIDAK PERNAH** |

> **Bila kunci *secret* pernah tertulis di kode aplikasi atau di-*upload* ke GitHub, kunci tersebut harus segera diganti (di-*rotate*) dari dashboard.** Sampaikan aturan ini sejak awal, karena banyak mahasiswa menyimpan kunci di repositori publik.

### B.5 Inisialisasi supabase_flutter

Package `supabase_flutter` ditambahkan seperti package biasa:

```bash
flutter pub add supabase_flutter
```

```yaml
dependencies:
  flutter:
    sdk: flutter
  supabase_flutter: ^2.18.3     # versi stabil saat modul ini disusun
```

Inisialisasi **harus** dilakukan sebelum aplikasi berjalan, dan karena ada proses `await`, perlu `WidgetsFlutterBinding.ensureInitialized()`:

```dart
import 'package:supabase_flutter/supabase_flutter.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();   // wajib sebelum ada await

  await Supabase.initialize(
    url: supabaseUrl,
    publishableKey: supabaseKey,
  );

  runApp(const MyApp());
}

final supabase = Supabase.instance.client;     // klien yang dipakai di seluruh aplikasi
```

> **Perubahan nama parameter:** dokumentasi Supabase sekarang memakai `publishableKey`. Parameter lama `anonKey` masih diterima, tetapi `publishableKey` yang diprioritaskan bila keduanya diisi. Bila mahasiswa menemukan tutorial lama yang memakai `anonKey`, sampaikan bahwa keduanya merujuk hal yang sama.

### B.6 CRUD di supabase_flutter

**Read — mengambil data**

```dart
final data = await supabase.from('menu').select();
// hasilnya berupa List berisi Map, mis. [{'id': 1, 'nama': 'Mie Aceh', ...}, ...]
```

**Create — menambah data**

```dart
await supabase.from('menu').insert({
  'nama': 'Mie Aceh',
  'kategori': 'Makanan',
  'harga': 25000,
});
// Kolom 'id' tidak perlu diisi — database membuatnya otomatis.
```

**Update — mengubah data**

```dart
await supabase.from('menu').update({'harga': 27000}).eq('id', 1);
```

**Delete — menghapus data**

```dart
await supabase.from('menu').delete().eq('id', 1);
```

Dua aturan keselamatan yang harus selalu disebut:

- `update()` dan `delete()` **wajib** diikuti filter (`.eq(...)`). Tanpa itu, **seluruh isi tabel** akan terubah/terhapus.
- Pada tabel dengan RLS aktif, `delete()` hanya dapat menghapus baris yang **terlihat** oleh policy `SELECT`. Jadi bila policy `SELECT` belum ada, `delete()` akan tampak "berhasil" tetapi tidak menghapus apa pun — dan ini bukan pesan error.

### B.7 Filter, Pengurutan, dan Pembatasan

```dart
final data = await supabase
    .from('menu')
    .select()
    .eq('kategori', 'Minuman')      // WHERE kategori = 'Minuman'
    .gte('harga', 10000)            // AND harga >= 10000
    .order('nama', ascending: true) // ORDER BY nama ASC
    .limit(20);                     // LIMIT 20
```

| Method | Padanan SQL | Kegunaan |
|---|---|---|
| `.eq(kolom, nilai)` | `= ` | Sama dengan |
| `.neq(kolom, nilai)` | `<>` | Tidak sama dengan |
| `.gt()` / `.gte()` | `>` / `>=` | Lebih besar (atau sama dengan) |
| `.lt()` / `.lte()` | `<` / `<=` | Lebih kecil (atau sama dengan) |
| `.ilike(kolom, pola)` | `ILIKE` | Pencarian teks, **tidak** peka huruf besar/kecil |
| `.order(kolom)` | `ORDER BY` | Pengurutan |
| `.limit(n)` / `.range(a, b)` | `LIMIT` / halaman | Membatasi jumlah baris |

> Supabase secara bawaan mengembalikan maksimal **1.000 baris** per permintaan. Untuk data yang lebih banyak, gunakan `.range()` untuk mengambil per halaman.

### B.8 Realtime dengan `.stream()`

Bila aplikasi dijalankan di dua perangkat, perubahan data di perangkat pertama dapat langsung muncul di perangkat kedua. Caranya, ganti `Future` menjadi `Stream`:

```dart
final stream = supabase.from('menu').stream(primaryKey: ['id']).order('nama');
```

`primaryKey` wajib diisi agar SDK tahu kolom mana yang menjadi identitas baris.

> **Peringatan penting:** sama seperti `Future` pada Pertemuan 4, `stream` **jangan** dibuat di dalam `build()`. Simpan sebagai variabel di `StatefulWidget`. Jika dibuat di dalam `build()`, koneksi realtime akan terus dibuka-tutup dan sambungan realtime akhirnya hilang.

Realtime juga harus **diaktifkan untuk tabel tersebut** di dashboard Supabase. Bila belum diaktifkan, `.stream()` umumnya hanya mengirim data awal lalu berhenti memberi pembaruan — tanpa pesan error.

### B.9 Keamanan: RLS dan Policy

Tanpa RLS, **siapa pun** yang memiliki publishable key (dan kunci ini ada di dalam aplikasi) dapat membaca bahkan menghapus seluruh isi tabel. Karena itu Supabase mengaktifkan RLS: setelah aktif, **tidak ada baris yang boleh diakses** kecuali ada *policy* yang mengizinkannya.

```sql
alter table public.menu enable row level security;

create policy "menu_baca_publik"
on public.menu for select
to anon, authenticated
using (true);            -- semua baris boleh dibaca
```

| Peran (role) | Siapa | Dipakai untuk |
|---|---|---|
| `anon` | Pengunjung yang belum login | Praktikum hari ini |
| `authenticated` | Pengguna yang sudah login | Pertemuan berikutnya |
| `service_role` | Server, melewati RLS | Hanya tugas administratif |

> **Penjelasan jujur yang perlu disampaikan ke mahasiswa:** policy `using (true)` berarti **seluruh dunia boleh membaca dan mengubah tabel ini** — itu memang diperlukan karena aplikasi kita belum memiliki sistem login. Pola ini **hanya untuk latihan dan prototipe**, bukan untuk aplikasi yang sudah dipakai orang banyak. Pada pertemuan berikutnya, setelah login tersedia, policy akan dipersempit menjadi seperti `using (auth.uid() = user_id)` sehingga setiap pengguna hanya dapat mengubah datanya sendiri.

### B.10 Alur Aplikasi yang Akan Dibangun

```
HalamanKatalog (daftar menu)
   │   SELECT * FROM menu            → List<MenuItem>
   │   tombol "+"  → FormMenu (mode tambah)   INSERT
   │   tap item    → FormMenu (mode edit)     UPDATE
   │   geser item  → konfirmasi       DELETE
   ▼
Supabase (tabel menu + RLS + policy)
   ▲
   │   data berubah → seluruh perangkat yang terhubung ikut terbarui
   │
HalamanKatalog perangkat lain (realtime, Latihan 4)
```

---

## C. Persiapan

### C.1 Menyiapkan Project Supabase (lakukan sekali)

1. Buka `supabase.com`, buat akun (tersedia paket gratis), lalu **New project**.
   - Simpan **database password** di tempat aman — password ini bukan kunci aplikasi.
   - Pilih region terdekat (mis. Singapore) agar respons lebih cepat.
2. Tunggu hingga project selesai dibuat (biasanya 1–2 menit).
3. Buka **SQL Editor**, tempel dan jalankan seluruh skrip di bagian C.2.
4. Buka **Connect** (atau *Project Settings → API*), catat dua nilai berikut:
   - **Project URL** — bentuknya `https://xxxxxxxxxxxx.supabase.co`
   - **Publishable key** (dahulu *anon key*)

> Jangan copas *secret key* / *service_role key* ke dalam aplikasi.

### C.2 Skrip SQL yang Harus Dijalankan

Salin **seluruhnya** ke SQL Editor, lalu klik **Run**. Skrip ini membuat tabel, mengisi data contoh, mengaktifkan RLS, membuat policy, dan memberikan hak akses Data API.

```sql
-- =====================================================================
-- MODUL PRAKTIKUM PERTEMUAN 5 — TABEL MENU
-- Jalankan seluruh skrip ini sekali di SQL Editor Supabase.
-- =====================================================================

-- 1. Tabel utama
create table if not exists public.menu (
  id          bigint primary key generated always as identity,
  nama        text not null,
  kategori    text not null default 'Makanan',
  harga       integer not null default 0,
  deskripsi   text,
  tersedia    boolean not null default true,
  dibuat_pada timestamptz not null default now()
);

-- 2. Data contoh (agar Latihan 1 langsung ada isinya)
insert into public.menu (nama, kategori, harga, deskripsi) values
  ('Mie Aceh',           'Makanan', 25000, 'Mie tebal dengan kuah bumbu rempah khas Aceh'),
  ('Kopi Sanger',        'Minuman', 15000, 'Kopi robusta diseduh dengan susu kental manis'),
  ('Ayam Tangkap',       'Makanan', 35000, 'Ayam goreng dengan daun kari dan daun pandan'),
  ('Pisang Goreng Keju', 'Camilan', 12000, 'Pisang goreng renyah dengan topping keju parut'),
  ('Es Timun Serut',     'Minuman', 10000, 'Minuman segar dari timun serut dan jeruk nipis');

-- 3. Aktifkan Row Level Security (WAJIB)
alter table public.menu enable row level security;

-- 4. Policy untuk praktikum (aplikasi belum memiliki sistem login)
drop policy if exists "menu_baca_publik"  on public.menu;
drop policy if exists "menu_tambah_publik" on public.menu;
drop policy if exists "menu_ubah_publik"  on public.menu;
drop policy if exists "menu_hapus_publik" on public.menu;

create policy "menu_baca_publik"
  on public.menu for select to anon, authenticated using (true);

create policy "menu_tambah_publik"
  on public.menu for insert to anon, authenticated with check (true);

create policy "menu_ubah_publik"
  on public.menu for update to anon, authenticated using (true) with check (true);

create policy "menu_hapus_publik"
  on public.menu for delete to anon, authenticated using (true);

-- 5. Hak akses Data API (diperlukan pada Supabase versi terbaru)
grant select, insert, update, delete on public.menu to anon;
grant select, insert, update, delete on public.menu to authenticated;

-- 6. Izin sequence (diperlukan bila kolom id memakai tipe serial/identity)
grant usage, select on all sequences in schema public to anon;
grant usage, select on all sequences in schema public to authenticated;
```

**Cara memastikan skrip berhasil:** buka **Table Editor**, pilih tabel `menu`. Kelima baris data contoh harus terlihat. Bila tabel tidak muncul, periksa panel pesan di SQL Editor — biasanya ada satu perintah yang gagal dan harus dijalankan ulang.

> **Catatan untuk pengajar:** pada Supabase versi terbaru, sebuah tabel **tidak otomatis** dapat diakses lewat Data API. Selain policy RLS, diperlukan `grant` (langkah 5). Bila mahasiswa melaporkan hasil `select()` selalu kosong atau muncul error `permission denied`, penyebab paling sering adalah langkah 5 yang belum dijalankan. Alternatifnya, tabel juga dapat diekspos melalui **Data API → Settings → Exposed tables** di dashboard.

### C.3 Menyiapkan Project Flutter

```bash
flutter create pnl_supabase
cd pnl_supabase
flutter pub add supabase_flutter
```

Buat file `lib/config.dart` berisi kunci (jangan di-*commit* ke repositori publik bila nanti menggunakan Git):

```dart
// lib/config.dart
const String supabaseUrl = 'https://xxxxxxxxxxxx.supabase.co';
const String supabaseKey = 'salin-publishable-key-anda-di-sini';
```

> **Nilai tambah (opsional):** pada proyek nyata, kunci disimpan di file `.env` dan tidak di-*commit*. Untuk praktikum ini, `config.dart` sudah memadai, tetapi kebiasaan baik sebaiknya diperkenalkan sejak sekarang.

---

## D. Praktikum Terpandu

> **Catatan waktu:** Latihan 1 paling lama karena memuat proses pendaftaran akun dan pembuatan tabel. Bila koneksi kelas lambat, minta mahasiswa membuat akun dan project **sebelum** praktikum dimulai, atau sediakan satu project contoh yang kuncinya dibagikan agar semua mahasiswa dapat langsung fokus ke bagian kode.

### Latihan 1 — Dari Dashboard ke Aplikasi: SELECT Pertama (30 menit)

Tujuannya membuktikan bahwa data yang tampil di aplikasi benar-benar berasal dari database di cloud, bukan dari kode program.

**Tahap A — buktikan data ada di cloud.** Buka **Table Editor** di dashboard Supabase dan pilih tabel `menu`. Anda akan melihat 5 baris data contoh yang dibuat oleh skrip SQL pada bagian C.2. Ubah satu baris di sana (mis. ubah harga `Mie Aceh` menjadi `27000`).

**Tahap B — tampilkan data di aplikasi.** Tulis kode berikut pada `lib/main.dart` (`lib/config.dart` dari bagian C.3 tetap dipakai):

```dart
import 'package:flutter/material.dart';
import 'package:supabase_flutter/supabase_flutter.dart';

import 'config.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();   // wajib: ada await sebelum runApp

  await Supabase.initialize(
    url: supabaseUrl,
    publishableKey: supabaseKey,
  );

  runApp(const MyApp());
}

/// Klien Supabase — dipakai di seluruh aplikasi.
final supabase = Supabase.instance.client;

// ---------------- MODEL ----------------
class MenuItem {
  final int id;
  final String nama;
  final String kategori;
  final int harga;
  final String deskripsi;
  final bool tersedia;

  const MenuItem({
    required this.id,
    required this.nama,
    required this.kategori,
    required this.harga,
    required this.deskripsi,
    required this.tersedia,
  });

  factory MenuItem.fromJson(Map<String, dynamic> json) {
    return MenuItem(
      // bigint dari Postgres tiba sebagai angka, jadi dikonversi dengan aman.
      id: (json['id'] as num).toInt(),
      nama: json['nama'] as String? ?? '-',
      kategori: json['kategori'] as String? ?? 'Lainnya',
      harga: (json['harga'] as num?)?.toInt() ?? 0,
      deskripsi: json['deskripsi'] as String? ?? '',
      tersedia: json['tersedia'] as bool? ?? true,
    );
  }
}

String formatRupiah(int nilai) {
  final pola = RegExp(r'\B(?=(\d{3})+(?!\d))');
  final hasil = nilai.toString().replaceAllMapped(pola, (match) => '.');
  return 'Rp $hasil';
}

// ---------------- AKSES DATABASE ----------------
Future<List<MenuItem>> ambilDaftarMenu() async {
  final data = await supabase
      .from('menu')
      .select()                        // SELECT * FROM menu
      .order('nama', ascending: true); // ORDER BY nama ASC

  return data.map((baris) => MenuItem.fromJson(baris)).toList();
}

// ---------------- TAMPILAN ----------------
class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: HalamanKatalog(),
    );
  }
}

class HalamanKatalog extends StatefulWidget {
  const HalamanKatalog({super.key});

  @override
  State<HalamanKatalog> createState() => _HalamanKatalogState();
}

class _HalamanKatalogState extends State<HalamanKatalog> {
  late Future<List<MenuItem>> futureMenu;

  @override
  void initState() {
    super.initState();
    futureMenu = ambilDaftarMenu();
  }

  void muatUlang() {
    setState(() {
      futureMenu = ambilDaftarMenu();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Menu Kafe (Supabase)'),
        backgroundColor: Colors.teal,
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            onPressed: muatUlang,
            icon: const Icon(Icons.refresh),
            tooltip: 'Muat ulang',
          ),
        ],
      ),
      body: FutureBuilder<List<MenuItem>>(
        future: futureMenu,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError) {
            return _tampilanError('${snapshot.error}', muatUlang);
          }

          final daftar = snapshot.data ?? [];
          if (daftar.isEmpty) {
            return const Center(
              child: Text('Tabel masih kosong. Tambahkan data dulu.'),
            );
          }

          return RefreshIndicator(
            onRefresh: () async => muatUlang(),
            child: ListView.builder(
              padding: const EdgeInsets.all(12),
              itemCount: daftar.length,
              itemBuilder: (context, index) {
                final menu = daftar[index];

                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  elevation: 3,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: ListTile(
                    leading: CircleAvatar(
                      backgroundColor: Colors.teal.shade50,
                      child: Text(
                        '${menu.id}',
                        style: const TextStyle(
                          color: Colors.teal,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                    ),
                    title: Text(
                      menu.nama,
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                    subtitle: Text(
                      '${menu.kategori} • ${menu.deskripsi}',
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                    ),
                    trailing: Text(
                      formatRupiah(menu.harga),
                      style: const TextStyle(
                        fontWeight: FontWeight.bold,
                        color: Colors.teal,
                      ),
                    ),
                  ),
                );
              },
            ),
          );
        },
      ),
    );
  }
}

Widget _tampilanError(String pesan, VoidCallback onCobaLagi) {
  return Center(
    child: Padding(
      padding: const EdgeInsets.all(24),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Icon(Icons.cloud_off, size: 56, color: Colors.grey),
          const SizedBox(height: 16),
          const Text(
            'Gagal memuat data',
            style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
          ),
          const SizedBox(height: 8),
          Text(pesan, textAlign: TextAlign.center, style: const TextStyle(fontSize: 12)),
          const SizedBox(height: 20),
          ElevatedButton.icon(
            onPressed: onCobaLagi,
            icon: const Icon(Icons.refresh),
            label: const Text('Coba Lagi'),
          ),
        ],
      ),
    ),
  );
}
```

**Tugas mahasiswa:**
1. Jalankan aplikasi. Apakah data yang tampil sama dengan isi **Table Editor**? Berapa harga `Mie Aceh` yang tampil, dan mengapa?
2. Buka kembali **Table Editor**, ubah satu nama menu, lalu tekan tombol *refresh* di aplikasi. Apakah perubahannya muncul? Jelaskan alur data dari Table Editor sampai ke layar aplikasi.
3. Tambahkan satu baris baru langsung dari **Table Editor** (tanpa mengubah kode apa pun). Apakah baris tersebut muncul di aplikasi setelah *refresh*? Apa kesimpulan Anda?
4. Pada model, kolom `dibuat_pada` tidak diikutsertakan. Tambahkan sebagai field baru, lalu tentukan tipe Dart yang tepat untuk kolom `timestamptz`.
5. Ubah `.order('nama', ascending: true)` menjadi `ascending: false`. Apa yang berubah?
6. Jalankan aplikasi di **dua perangkat** (mis. emulator dan HP) sekaligus. Apakah keduanya menampilkan data yang sama?

> **Catatan asisten:** jawaban tugas nomor 1 dan 3 adalah inti latihan ini. Mahasiswa harus menyimpulkan sendiri bahwa **aplikasi tidak menyimpan data apa pun secara lokal** — ia hanya menampilkan apa yang ada di database cloud saat itu. Jangan beri tahu lebih dulu; biarkan mereka membuktikannya lewat Table Editor.

> **Catatan asisten:** untuk tugas nomor 6, tutup dulu pertanyaan "mengapa data sama?" sampai Latihan 4. Data menjadi sama karena keduanya membaca tabel yang sama; pada Latihan 4 ditambahkan pembaruan otomatis tanpa tombol refresh.

### Latihan 2 — Menambah Data dengan INSERT (25 menit)

Sekarang aplikasi mulai **menulis** ke database. Tambahkan halaman formulir dan satu method insert pada `lib/main.dart` (biarkan class yang sudah ada tetap utuh).

**Tambahan 1 — method insert.**

```dart
Future<void> tambahMenu({
  required String nama,
  required String kategori,
  required int harga,
  required String deskripsi,
}) async {
  await supabase.from('menu').insert({
    'nama': nama,
    'kategori': kategori,
    'harga': harga,
    'deskripsi': deskripsi,
    // 'id' tidak diisi — database membuatnya otomatis.
    // 'tersedia' dan 'dibuat_pada' memakai nilai default dari tabel.
  });
}
```

**Tambahan 2 — halaman formulir.**

```dart
class FormTambahMenu extends StatefulWidget {
  const FormTambahMenu({super.key});

  @override
  State<FormTambahMenu> createState() => _FormTambahMenuState();
}

class _FormTambahMenuState extends State<FormTambahMenu> {
  final _formKey = GlobalKey<FormState>();
  final _nama = TextEditingController();
  final _harga = TextEditingController();
  final _deskripsi = TextEditingController();

  String _kategori = 'Makanan';
  bool _sedangMenyimpan = false;

  @override
  void dispose() {
    _nama.dispose();
    _harga.dispose();
    _deskripsi.dispose();
    super.dispose();   // WAJIB: controller harus dibuang agar tidak bocor memori
  }

  Future<void> _simpan() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _sedangMenyimpan = true);

    try {
      await tambahMenu(
        nama: _nama.text.trim(),
        kategori: _kategori,
        harga: int.parse(_harga.text.trim()),
        deskripsi: _deskripsi.text.trim(),
      );

      if (!mounted) return;
      Navigator.pop(context, true);   // true = berhasil, dipakai halaman katalog
    } on PostgrestException catch (e) {
      if (!mounted) return;
      setState(() => _sedangMenyimpan = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Gagal menyimpan: ${e.message}')),
      );
    } catch (e) {
      if (!mounted) return;
      setState(() => _sedangMenyimpan = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Terjadi kesalahan: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Tambah Menu'),
        backgroundColor: Colors.teal,
        foregroundColor: Colors.white,
      ),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            TextFormField(
              controller: _nama,
              textInputAction: TextInputAction.next,
              decoration: const InputDecoration(
                labelText: 'Nama menu',
                border: OutlineInputBorder(),
              ),
              validator: (nilai) {
                if (nilai == null || nilai.trim().isEmpty) {
                  return 'Nama menu wajib diisi';
                }
                if (nilai.trim().length < 3) {
                  return 'Nama menu minimal 3 karakter';
                }
                return null;
              },
            ),
            const SizedBox(height: 16),
            DropdownButtonFormField<String>(
              initialValue: _kategori,
              decoration: const InputDecoration(
                labelText: 'Kategori',
                border: OutlineInputBorder(),
              ),
              items: const [
                DropdownMenuItem(value: 'Makanan', child: Text('Makanan')),
                DropdownMenuItem(value: 'Minuman', child: Text('Minuman')),
                DropdownMenuItem(value: 'Camilan', child: Text('Camilan')),
              ],
              onChanged: (nilai) {
                if (nilai == null) return;
                setState(() => _kategori = nilai);
              },
            ),
            const SizedBox(height: 16),
            TextFormField(
              controller: _harga,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(
                labelText: 'Harga (angka saja)',
                prefixText: 'Rp ',
                border: OutlineInputBorder(),
              ),
              validator: (nilai) {
                if (nilai == null || nilai.trim().isEmpty) {
                  return 'Harga wajib diisi';
                }
                final angka = int.tryParse(nilai.trim());
                if (angka == null) return 'Harga harus berupa angka';
                if (angka <= 0) return 'Harga harus lebih dari 0';
                return null;
              },
            ),
            const SizedBox(height: 16),
            TextFormField(
              controller: _deskripsi,
              maxLines: 3,
              decoration: const InputDecoration(
                labelText: 'Deskripsi (opsional)',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 24),
            FilledButton.icon(
              onPressed: _sedangMenyimpan ? null : _simpan,
              icon: _sedangMenyimpan
                  ? const SizedBox(
                      width: 18,
                      height: 18,
                      child: CircularProgressIndicator(
                        strokeWidth: 2,
                        color: Colors.white,
                      ),
                    )
                  : const Icon(Icons.save),
              label: Text(_sedangMenyimpan ? 'Menyimpan...' : 'Simpan'),
            ),
          ],
        ),
      ),
    );
  }
}
```

**Tambahan 3 — tombol `+` pada halaman katalog** (di dalam `Scaffold`, sejajar dengan `AppBar`):

```dart
floatingActionButton: FloatingActionButton.extended(
  onPressed: () async {
    // Menunggu hasil dari halaman formulir: true = data berhasil disimpan.
    final berhasil = await Navigator.push<bool>(
      context,
      MaterialPageRoute(builder: (context) => const FormTambahMenu()),
    );

    if (berhasil == true) {
      muatUlang();
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Menu berhasil ditambahkan')),
      );
    }
  },
  icon: const Icon(Icons.add),
  label: const Text('Tambah Menu'),
),
```

> Pada versi Flutter sebelum 3.33, ganti `initialValue:` pada `DropdownButtonFormField` menjadi `value:`. Keduanya berfungsi, hanya namanya yang berbeda.

**Tugas mahasiswa:**
1. Tambahkan satu menu baru dari aplikasi, lalu periksa **Table Editor**. Apakah baris tersebut benar-benar tersimpan di database?
2. Berapa nilai kolom `id`, `tersedia`, dan `dibuat_pada` untuk baris baru itu? Dari mana nilai tersebut berasal?
3. Tekan tombol Simpan dengan harga berisi teks (mis. `dua ribu`). Pesan validasi apa yang muncul? Apakah permintaan ke database terkirim? Jelaskan mengapa.
4. Hapus blok `try`/`catch` sehingga error tidak ditangani. Matikan internet, lalu coba simpan. Apa yang terjadi pada aplikasi? **Kembalikan** kode `try`/`catch` setelah selesai.
5. Tambahkan validasi pada kolom deskripsi: maksimal 100 karakter.
6. **Pertanyaan analisis:** apa perbedaan mendasar antara `Navigator.push` pada Pertemuan 3 (mengirim data) dengan `Navigator.push<bool>` di sini (menerima data kembali)? Kapan masing-masing dipakai?

> **Catatan asisten:** tugas nomor 4 sengaja menuntun mahasiswa melihat akibat tidak menangani error pada operasi tulis. Berbeda dengan operasi baca, kegagalan `insert` yang tidak tertangani dapat membuat aplikasi berhenti total (unhandled exception) — bukan sekadar menampilkan layar kosong.

### Latihan 3 — Mengubah dan Menghapus (UPDATE & DELETE) (25 menit)

Sekarang lengkapi siklus CRUD. Perhatikan bahwa `update()` dan `delete()` **selalu** disertai filter.

**Tambahan 1 — tiga method baru.**

```dart
Future<void> ubahMenu({
  required int id,
  required String nama,
  required String kategori,
  required int harga,
  required String deskripsi,
  required bool tersedia,
}) async {
  await supabase.from('menu').update({
    'nama': nama,
    'kategori': kategori,
    'harga': harga,
    'deskripsi': deskripsi,
    'tersedia': tersedia,
  }).eq('id', id);          // TANPA .eq() → SELURUH tabel akan terubah!
}

Future<void> ubahKetersediaan({required int id, required bool tersedia}) async {
  await supabase.from('menu').update({'tersedia': tersedia}).eq('id', id);
}

Future<void> hapusMenu(int id) async {
  await supabase.from('menu').delete().eq('id', id);   // TANPA .eq() → SELURUH tabel terhapus!
}
```

**Tambahan 2 — formulir dipakai untuk dua mode.** Ubah `FormTambahMenu` menjadi `FormMenu` yang menerima data opsional. Karena nama class berubah, **jangan lupa memperbarui pemanggilannya pada `floatingActionButton`** di halaman katalog agar menjadi `const FormMenu()` — bila terlewat, muncul error "The method 'FormTambahMenu' isn't defined".

```dart
class FormMenu extends StatefulWidget {
  const FormMenu({super.key, this.menu});

  /// null  → mode TAMBAH
  /// terisi → mode EDIT
  final MenuItem? menu;

  @override
  State<FormMenu> createState() => _FormMenuState();
}

class _FormMenuState extends State<FormMenu> {
  final _formKey = GlobalKey<FormState>();

  late final TextEditingController _nama;
  late final TextEditingController _harga;
  late final TextEditingController _deskripsi;

  late String _kategori;
  late bool _tersedia;
  bool _sedangMenyimpan = false;

  bool get _modeEdit => widget.menu != null;

  @override
  void initState() {
    super.initState();

    // Isi awal: dari data yang ada (mode edit) atau kosong (mode tambah).
    final menu = widget.menu;
    _nama = TextEditingController(text: menu?.nama ?? '');
    _harga = TextEditingController(text: menu == null ? '' : '${menu.harga}');
    _deskripsi = TextEditingController(text: menu?.deskripsi ?? '');
    _kategori = menu?.kategori ?? 'Makanan';
    _tersedia = menu?.tersedia ?? true;
  }

  @override
  void dispose() {
    _nama.dispose();
    _harga.dispose();
    _deskripsi.dispose();
    super.dispose();
  }

  /// Daftar pilihan kategori. Nilai dari database selalu dimasukkan,
  /// agar dropdown tidak error bila data memakai kategori di luar daftar bawaan.
  List<String> get _pilihanKategori {
    const bawaan = ['Makanan', 'Minuman', 'Camilan'];
    if (bawaan.contains(_kategori)) return bawaan;
    return [_kategori, ...bawaan];
  }

  Future<void> _simpan() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _sedangMenyimpan = true);

    try {
      if (_modeEdit) {
        await ubahMenu(
          id: widget.menu!.id,
          nama: _nama.text.trim(),
          kategori: _kategori,
          harga: int.parse(_harga.text.trim()),
          deskripsi: _deskripsi.text.trim(),
          tersedia: _tersedia,
        );
      } else {
        await tambahMenu(
          nama: _nama.text.trim(),
          kategori: _kategori,
          harga: int.parse(_harga.text.trim()),
          deskripsi: _deskripsi.text.trim(),
        );
      }

      if (!mounted) return;
      Navigator.pop(context, true);
    } on PostgrestException catch (e) {
      if (!mounted) return;
      setState(() => _sedangMenyimpan = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Gagal menyimpan: ${e.message}')),
      );
    } catch (e) {
      if (!mounted) return;
      setState(() => _sedangMenyimpan = false);
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('Terjadi kesalahan: $e')),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(_modeEdit ? 'Ubah Menu' : 'Tambah Menu'),
        backgroundColor: Colors.teal,
        foregroundColor: Colors.white,
      ),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(16),
          children: [
            TextFormField(
              controller: _nama,
              textInputAction: TextInputAction.next,
              decoration: const InputDecoration(
                labelText: 'Nama menu',
                border: OutlineInputBorder(),
              ),
              validator: (nilai) {
                if (nilai == null || nilai.trim().isEmpty) {
                  return 'Nama menu wajib diisi';
                }
                if (nilai.trim().length < 3) {
                  return 'Nama menu minimal 3 karakter';
                }
                return null;
              },
            ),
            const SizedBox(height: 16),
            DropdownButtonFormField<String>(
              initialValue: _kategori,
              decoration: const InputDecoration(
                labelText: 'Kategori',
                border: OutlineInputBorder(),
              ),
              items: _pilihanKategori
                  .map((k) => DropdownMenuItem(value: k, child: Text(k)))
                  .toList(),
              onChanged: (nilai) {
                if (nilai == null) return;
                setState(() => _kategori = nilai);
              },
            ),
            const SizedBox(height: 16),
            TextFormField(
              controller: _harga,
              keyboardType: TextInputType.number,
              decoration: const InputDecoration(
                labelText: 'Harga (angka saja)',
                prefixText: 'Rp ',
                border: OutlineInputBorder(),
              ),
              validator: (nilai) {
                if (nilai == null || nilai.trim().isEmpty) {
                  return 'Harga wajib diisi';
                }
                final angka = int.tryParse(nilai.trim());
                if (angka == null) return 'Harga harus berupa angka';
                if (angka <= 0) return 'Harga harus lebih dari 0';
                return null;
              },
            ),
            const SizedBox(height: 16),
            TextFormField(
              controller: _deskripsi,
              maxLines: 3,
              maxLength: 100,
              decoration: const InputDecoration(
                labelText: 'Deskripsi (opsional)',
                border: OutlineInputBorder(),
              ),
            ),
            SwitchListTile(
              value: _tersedia,
              onChanged: (nilai) => setState(() => _tersedia = nilai),
              title: const Text('Tersedia'),
              subtitle: const Text('Menu yang tidak tersedia ditandai pada daftar'),
              contentPadding: EdgeInsets.zero,
            ),
            const SizedBox(height: 16),
            FilledButton.icon(
              onPressed: _sedangMenyimpan ? null : _simpan,
              icon: _sedangMenyimpan
                  ? const SizedBox(
                      width: 18,
                      height: 18,
                      child: CircularProgressIndicator(
                        strokeWidth: 2,
                        color: Colors.white,
                      ),
                    )
                  : const Icon(Icons.save),
              label: Text(_sedangMenyimpan ? 'Menyimpan...' : 'Simpan'),
            ),
          ],
        ),
      ),
    );
  }
}
```

> Pada mode edit, `SwitchListTile` untuk kolom `tersedia` hanya muncul di formulir. Ini sengaja: menaruh `Switch` di dalam `trailing` `ListTile` bersama teks harga mudah membuat tampilan meluber (overflow) pada layar sempit.

**Tambahan 3 — daftar dengan geser-untuk-hapus dan tap-untuk-ubah.** Ganti `itemBuilder` pada halaman katalog:

```dart
itemBuilder: (context, index) {
  final menu = daftar[index];

  return Dismissible(
    key: ValueKey(menu.id),              // wajib unik untuk setiap baris
    direction: DismissDirection.endToStart,
    background: Container(
      alignment: Alignment.centerRight,
      padding: const EdgeInsets.only(right: 24),
      margin: const EdgeInsets.only(bottom: 12),
      decoration: BoxDecoration(
        color: Colors.red.shade400,
        borderRadius: BorderRadius.circular(16),
      ),
      child: const Icon(Icons.delete, color: Colors.white),
    ),
    confirmDismiss: (arah) async {
      return await showDialog<bool>(
            context: context,
            builder: (context) => AlertDialog(
              title: const Text('Hapus menu?'),
              content: Text('"${menu.nama}" akan dihapus permanen dari database.'),
              actions: [
                TextButton(
                  onPressed: () => Navigator.pop(context, false),
                  child: const Text('Batal'),
                ),
                FilledButton(
                  onPressed: () => Navigator.pop(context, true),
                  child: const Text('Hapus'),
                ),
              ],
            ),
          ) ??
          false;
    },
    onDismissed: (arah) {
      // Hapus di database DULU, baru muat ulang daftar.
      // Urutan ini penting: bila daftar dimuat ulang sebelum penghapusan
      // selesai, baris yang sudah digeser akan muncul kembali dan
      // Flutter melempar error "A dismissed Dismissible widget is still part of the tree".
      setState(() {
        futureMenu = _hapusLaluMuatUlang(menu.id);
      });
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text('"${menu.nama}" dihapus')),
      );
    },
    child: Card(
      margin: const EdgeInsets.only(bottom: 12),
      elevation: 3,
      shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
      child: ListTile(
        contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        leading: CircleAvatar(
          backgroundColor: menu.tersedia ? Colors.teal.shade50 : Colors.grey.shade200,
          child: Text(
            '${menu.id}',
            style: TextStyle(
              color: menu.tersedia ? Colors.teal : Colors.grey,
              fontWeight: FontWeight.bold,
            ),
          ),
        ),
        title: Text(
          menu.nama,
          style: TextStyle(
            fontWeight: FontWeight.bold,
            // Menu yang tidak tersedia ditampilkan lebih redup.
            color: menu.tersedia ? null : Colors.grey,
          ),
        ),
        subtitle: Text(
          '${menu.kategori}${menu.tersedia ? '' : ' • TIDAK TERSEDIA'}\n${menu.deskripsi}',
          maxLines: 2,
          overflow: TextOverflow.ellipsis,
        ),
        isThreeLine: true,
        trailing: Text(
          formatRupiah(menu.harga),
          style: const TextStyle(fontWeight: FontWeight.bold, color: Colors.teal),
        ),
        onTap: () async {
          final berhasil = await Navigator.push<bool>(
            context,
            MaterialPageRoute(builder: (context) => FormMenu(menu: menu)),
          );
          if (berhasil == true && mounted) {
            muatUlang();
            ScaffoldMessenger.of(context).showSnackBar(
              const SnackBar(content: Text('Perubahan disimpan')),
            );
          }
        },
      ),
    ),
  );
},
```

Dan tambahkan method pembantu di dalam `_HalamanKatalogState`:

```dart
Future<List<MenuItem>> _hapusLaluMuatUlang(int id) async {
  await hapusMenu(id);
  return ambilDaftarMenu();
}
```

**Tugas mahasiswa:**
1. Ubah harga sebuah menu dari aplikasi, lalu periksa Table Editor. Apakah nilai barunya tersimpan?
2. Geser satu baris ke kiri, tekan "Batal" pada dialog, lalu geser lagi dan tekan "Hapus". Jelaskan mengapa dialog konfirmasi penting pada operasi hapus.
3. Tandai satu menu sebagai tidak tersedia. Bagaimana tampilannya berubah di daftar?
4. **Percobaan berbahaya (di database latihan, bukan database produksi):** pada method `hapusMenu`, hapus bagian `.eq('id', id)` lalu jalankan tombol hapus sekali saja. Periksa Table Editor. Apa yang terjadi, dan mengapa? Pelajari gejalanya, lalu **kembalikan** `.eq('id', id)`.
5. Tambahkan kolom `stok` (integer) pada tabel melalui SQL Editor, lengkapi model dan formulirnya, lalu tampilkan pada daftar. Catat perintah SQL yang Anda pakai di laporan.
6. **Pertanyaan analisis:** pada `_hapusLaluMuatUlang`, mengapa penghapusan dilakukan **sebelum** `ambilDaftarMenu()`? Apa akibatnya bila urutannya dibalik?

> **Catatan asisten:** tugas nomor 4 adalah latihan keselamatan yang paling berkesan bagi mahasiswa, tetapi **wajib** dilakukan pada database latihan dan datanya sudah tidak diperlukan. Sebelum mereka mencoba, pastikan data contoh dapat dibuat ulang (skrip SQL di bagian C.2 dapat dijalankan ulang, atau cukup tambahkan kembali data lewat aplikasi).

> **Catatan asisten:** jawaban tugas nomor 6 adalah penghapusan harus selesai lebih dulu agar daftar yang dimuat ulang tidak lagi memuat baris tersebut. Bila urutannya dibalik, baris yang sudah digeser akan kembali muncul dan Flutter melempar error "A dismissed Dismissible widget is still part of the tree".

### Latihan 4 — Proyek Mini: CRUD Realtime dengan Pencarian dan Filter (35 menit)

Latihan inti hari ini: daftar berubah otomatis di **semua perangkat** yang terhubung, tanpa tombol refresh. Mahasiswa mengerjakan mandiri, dosen/asisten berkeliling membimbing.

**Ketentuan wajib:**
1. Daftar menu memakai `.stream(primaryKey: ['id'])` + `StreamBuilder` sehingga pembaruan datang otomatis.
2. `stream` disimpan sebagai variabel di `StatefulWidget` — **bukan** dibuat di dalam `build()`.
3. Terdapat kolom pencarian yang memfilter nama menu tanpa memanggil ulang server.
4. Terdapat filter kategori (`Semua`, `Makanan`, `Minuman`, `Camilan`).
5. Keadaan **menunggu**, **gagal** (dengan tombol "Coba Lagi"), dan **berhasil** ditangani.
6. Tambah, ubah, dan hapus tetap berfungsi; daftar ikut berubah tanpa tombol refresh.
7. Bila hasil pencarian kosong, tampilkan pesan yang jelas (bukan layar putih).

**Struktur pohon widget yang disarankan (hint):**

```
HalamanKatalog (StatefulWidget)
├── Scaffold + AppBar
├── floatingActionButton → FormMenu (tambah)
└── body: Column
    ├── Padding → TextField         (pencarian)
    ├── Padding → Wrap → ChoiceChip (filter kategori)
    └── Expanded
        └── StreamBuilder<List<Map<String, dynamic>>>
            ├── hasError   → pesan + tombol "Coba Lagi"
            ├── !hasData   → CircularProgressIndicator
            └── data       → saring (pencarian + kategori)
                             → ListView.builder → Dismissible → Card → ListTile
                                                    (onTap → FormMenu(mode edit))
```

**Kode acuan — hanya class `_HalamanKatalogState` yang berubah:**

```dart
class _HalamanKatalogState extends State<HalamanKatalog> {
  // Stream disimpan sebagai variabel. JANGAN dibuat di dalam build(),
  // karena build() dapat dipanggil berkali-kali dan koneksi realtime akan terputus.
  late Stream<List<Map<String, dynamic>>> _streamMenu;

  String _kataKunci = '';
  String _kategoriTerpilih = 'Semua';

  @override
  void initState() {
    super.initState();
    _buatStream();
  }

  void _buatStream() {
    _streamMenu = supabase
        .from('menu')
        .stream(primaryKey: ['id'])   // kolom identitas baris — wajib diisi
        .order('nama', ascending: true);
  }

  Future<void> _bukaForm({MenuItem? menu}) async {
    final berhasil = await Navigator.push<bool>(
      context,
      MaterialPageRoute(builder: (context) => FormMenu(menu: menu)),
    );

    if (berhasil == true && mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text(menu == null ? 'Menu ditambahkan' : 'Perubahan disimpan'),
          duration: const Duration(seconds: 1),
        ),
      );
      // Tidak perlu memuat ulang: perubahan akan datang sendiri lewat stream.
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Menu Kafe (Realtime)'),
        backgroundColor: Colors.teal,
        foregroundColor: Colors.white,
      ),
      floatingActionButton: FloatingActionButton.extended(
        onPressed: () => _bukaForm(),
        icon: const Icon(Icons.add),
        label: const Text('Tambah'),
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(12, 12, 12, 0),
            child: TextField(
              decoration: const InputDecoration(
                hintText: 'Cari nama menu...',
                prefixIcon: Icon(Icons.search),
                border: OutlineInputBorder(),
                isDense: true,
              ),
              onChanged: (nilai) => setState(() => _kataKunci = nilai),
            ),
          ),
          Padding(
            padding: const EdgeInsets.all(12),
            child: Wrap(
              spacing: 8,
              runSpacing: 8,
              children: [
                for (final kategori in const [
                  'Semua',
                  'Makanan',
                  'Minuman',
                  'Camilan',
                ])
                  ChoiceChip(
                    label: Text(kategori),
                    selected: _kategoriTerpilih == kategori,
                    onSelected: (dipilih) {
                      setState(() => _kategoriTerpilih = kategori);
                    },
                  ),
              ],
            ),
          ),
          Expanded(
            child: StreamBuilder<List<Map<String, dynamic>>>(
              stream: _streamMenu,
              builder: (context, snapshot) {
                if (snapshot.hasError) {
                  return _tampilanError(
                    '${snapshot.error}',
                    () => setState(_buatStream),
                  );
                }

                if (!snapshot.hasData) {
                  return const Center(child: CircularProgressIndicator());
                }

                // Semua baris dari database diubah menjadi objek.
                final semua = snapshot.data!
                    .map((baris) => MenuItem.fromJson(baris))
                    .toList();

                // Penyaringan dilakukan di sisi aplikasi agar daftar tetap
                // realtime. Cara lain: memfilter di sisi database dengan .eq().
                final hasil = semua.where((menu) {
                  final cocokKata = menu.nama
                      .toLowerCase()
                      .contains(_kataKunci.toLowerCase());
                  final cocokKategori = _kategoriTerpilih == 'Semua' ||
                      menu.kategori == _kategoriTerpilih;
                  return cocokKata && cocokKategori;
                }).toList();

                if (hasil.isEmpty) {
                  return Center(
                    child: Padding(
                      padding: const EdgeInsets.all(24),
                      child: Text(
                        semua.isEmpty
                            ? 'Tabel masih kosong. Tekan "Tambah" untuk mengisi.'
                            : 'Tidak ada menu yang cocok dengan pencarian.',
                        textAlign: TextAlign.center,
                      ),
                    ),
                  );
                }

                return ListView.builder(
                  padding: const EdgeInsets.fromLTRB(12, 0, 12, 88),
                  itemCount: hasil.length,
                  itemBuilder: (context, index) {
                    final menu = hasil[index];
                    return _kartuMenu(menu);   // sama seperti Latihan 3
                  },
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
```

**Cara mengaktifkan realtime untuk tabel `menu`:** buka dashboard Supabase, cari pengaturan **Realtime** untuk tabel `menu` (di area *Database* / *Replication*, atau tombol *Realtime* pada Table Editor) dan aktifkan. Tanpa ini, daftar umumnya hanya menampilkan data awal dan tidak ikut berubah.

> Padding bawah `88` pada `ListView` disediakan agar baris terakhir tidak tertutup tombol "Tambah".

**Tugas mahasiswa:**
1. **Percobaan utama:** jalankan aplikasi di **dua perangkat** sekaligus (emulator + HP, atau dua emulator). Tambahkan satu menu dari perangkat pertama. Apakah perangkat kedua ikut berubah **tanpa** ditekan apa pun? Catat waktu yang dibutuhkan hingga data muncul.
2. Lakukan hal yang sama pada **Table Editor**: ubah harga sebuah menu dari dashboard. Apakah perubahan itu juga muncul di kedua perangkat?
3. Hapus satu baris dari Table Editor. Apakah baris itu ikut hilang di aplikasi?
4. Pada Latihan 1–3, setiap perubahan selalu diikuti pemanggilan `muatUlang()`. Pada versi realtime ini, hapus semua pemanggilan tersebut (termasuk yang masih tersisa pada penanganan hapus bila Anda menyalinnya dari Latihan 3). Apakah daftar tetap menampilkan data terbaru? Jelaskan mengapa.
5. Ubah `stream(primaryKey: ['id'])` menjadi `stream(primaryKey: ['nama'])`. Berhati-hatilah: nilai `nama` tidak unik. Apa yang terjadi, dan mengapa `primaryKey` harus benar-benar unik?
6. Pindahkan `_buatStream()` ke dalam `build()` sehingga stream dibuat setiap kali tampilan dibangun. Jalankan, lakukan beberapa kali gulir dan beberapa kali perubahan data. Gejala apa yang muncul? **Kembalikan** ke `initState`.
7. (Nilai tambah) Tambahkan pengurutan pilihan pengguna: tombol untuk mengurutkan berdasarkan nama, harga termurah, dan harga termahal.
8. (Nilai tambah) Tampilkan jumlah menu yang sedang ditampilkan, mis. `Menampilkan 3 dari 5 menu`.

> **Catatan asisten:** pertanyaan nomor 4 dan 6 adalah dua sisi dari konsep yang sama dengan Latihan 3 Pertemuan 4. Tekankan bahwa `Future` maupun `Stream` harus disimpan di luar `build()`, karena `build()` dapat dipanggil ratusan kali.

> **Catatan implementasi — `_kartuMenu` wajib disesuaikan.** Pada kode di atas, `_kartuMenu(menu)` adalah widget `Dismissible` + `Card` + `ListTile` dari Latihan 3, dipindahkan menjadi method tersendiri di dalam `_HalamanKatalogState`. Karena seluruh isi `_HalamanKatalogState` sudah diganti, **dua bagian berikut wajib diubah**. Bila tidak, kode tidak dapat dikompilasi (`futureMenu`, `_hapusLaluMuatUlang`, dan `muatUlang` sudah tidak ada lagi pada versi ini).
>
> ```dart
> Widget _kartuMenu(MenuItem menu) {
>   return Dismissible(
>     key: ValueKey(menu.id),
>     direction: DismissDirection.endToStart,
>     background: /* sama seperti Latihan 3 */,
>     confirmDismiss: /* sama seperti Latihan 3 — dialog konfirmasi */,
>
>     // PERUBAHAN 1 — daftar tidak lagi dimuat ulang secara manual.
>     onDismissed: (arah) async {
>       try {
>         await hapusMenu(menu.id);
>         if (!mounted) return;
>         ScaffoldMessenger.of(context).showSnackBar(
>           SnackBar(content: Text('"${menu.nama}" dihapus')),
>         );
>       } catch (e) {
>         if (!mounted) return;
>         ScaffoldMessenger.of(context).showSnackBar(
>           SnackBar(content: Text('Gagal menghapus: $e')),
>         );
>       }
>       // Tidak ada futureMenu maupun muatUlang() di sini:
>       // stream akan memperbarui daftar dengan sendirinya.
>     },
>
>     child: Card(
>       // ... sama seperti Latihan 3 ...
>       child: ListTile(
>         // ...
>
>         // PERUBAHAN 2 — tap membuka formulir mode edit.
>         onTap: () => _bukaForm(menu: menu),
>       ),
>     ),
>   );
> }
> ```
>
> Pemisahan ini bukan sekadar kerapian: `itemBuilder` pada Latihan 4 sudah cukup panjang, dan satu method khusus membuat kode lebih mudah dibaca.

---

## E. Tugas Mandiri (Dikumpulkan)

Bangun aplikasi **pendataan pribadi** yang seluruh datanya tersimpan di database Supabase milik Anda sendiri. Tema bebas (koleksi buku, daftar tugas, inventaris barang, daftar kontak, dan sebagainya), tetapi **bukan** tabel `menu` contoh dari praktikum.

**Ketentuan wajib:**

1. **Struktur database:** buat tabel baru dengan **minimal 6 kolom**, memuat sekurang-kurangnya:
   - satu primary key yang dibuat otomatis,
   - satu kolom `text` yang wajib diisi (`not null`),
   - satu kolom angka (`integer` atau `numeric`),
   - satu kolom kategori/pilihan (`text`),
   - satu kolom `boolean`,
   - satu kolom `timestamptz` dengan nilai default `now()`.
2. **Keamanan:** RLS **aktif** pada tabel tersebut, disertai policy `select`, `insert`, `update`, dan `delete`, serta `grant` yang sesuai.
3. **CRUD lengkap:**
   - **Create** — formulir dengan validasi (minimal 3 aturan validasi berbeda),
   - **Read** — daftar dengan pencarian dan filter kategori,
   - **Update** — formulir terisi data lama, dibuka dengan menekan baris,
   - **Delete** — wajib melalui dialog konfirmasi.
4. **Realtime:** daftar memakai `.stream()` sehingga perubahan dari perangkat lain langsung tampil. Sertakan bukti uji dua perangkat.
5. **Model class** dengan `factory fromJson` dan nilai default untuk seluruh kolom yang boleh `null`.
6. **Penanganan error:** semua operasi database dibungkus `try`/`catch` dengan `PostgrestException`; setiap kegagalan menampilkan pesan yang dapat dipahami pengguna (bukan pesan mentah). Aplikasi **tidak boleh berhenti (crash)** saat internet dimatikan di tengah operasi.
7. **Keadaan tampilan:** menunggu, gagal (dengan tombol "Coba Lagi"), berhasil, dan kosong — keempatnya ditangani.
8. **Pengurutan:** sediakan minimal dua pilihan pengurutan bagi pengguna.

**Nilai tambah (opsional):**
- Mengambil jumlah data dengan `.count()` dan menampilkannya di `AppBar`.
- Memuat data per halaman dengan `.range()` (pagination).
- Mengunggah foto ke Supabase Storage dan menampilkan tautannya.
- Memisahkan kode ke `lib/models/`, `lib/services/`, `lib/pages/`, dan `lib/widgets/`.

**Pengumpulan:**

1. Seluruh file `.dart`, **kecuali** `lib/config.dart` yang diganti menjadi contoh kosong (`config.example.dart`) agar kunci Anda tidak ikut terkumpul.
2. **Skrip SQL lengkap** yang Anda jalankan (buat tabel + policy + grant), ditulis di laporan.
3. **Screenshot:** (a) daftar data di aplikasi, (b) formulir tambah, (c) formulir ubah, (d) dialog konfirmasi hapus, (e) pesan error saat internet dimatikan, (f) **Table Editor** yang memperlihatkan data hasil input dari aplikasi, (g) uji dua perangkat pada mode realtime.
4. Laporan PDF yang memuat:
   - struktur tabel dan alasan pemilihan tipe data setiap kolom,
   - penjelasan alur satu operasi CRUD dari tombol di aplikasi hingga data tersimpan di database,
   - jawaban pertanyaan Latihan 1–4,
   - jawaban atas dua pertanyaan analisis berikut: **(i)** mengapa kunci *publishable* boleh disertakan di aplikasi sementara kunci *secret* tidak, dan **(ii)** apa yang akan terjadi bila aplikasi ini dipakai orang banyak dengan policy `using (true)` seperti sekarang, serta bagaimana cara memperbaikinya setelah fitur login tersedia.

> **Peringatan pengumpulan:** jangan pernah mengirim kunci *secret* / *service_role*, password database, atau *connection string* di dalam laporan, screenshot, maupun repositori. Bila hal itu sudah terjadi, segera ganti kuncinya dari dashboard sebelum dikumpulkan.

---

## F. Rubrik Penilaian (Total 100)

| Aspek | Bobot |
|---|---|
| Latihan 1–3 selesai dan jawaban pertanyaan benar | 25 |
| Latihan 4 (CRUD realtime + pencarian + filter) sesuai ketentuan wajib | 30 |
| Tugas Mandiri: struktur database, RLS + policy + grant, kelengkapan CRUD | 25 |
| Tugas Mandiri: kerapian kode, penanganan error & kreativitas tampilan | 20 |

**Catatan penilaian:**
- Tabel tanpa RLS, atau RLS aktif tetapi tanpa policy, dikenakan pengurangan pada aspek ketiga (dan dibahas langsung dengan mahasiswa, karena ini soal keamanan, bukan sekadar nilai).
- `update()` atau `delete()` tanpa filter `.eq()` dikenakan pengurangan pada aspek keempat.
- Menyertakan kunci *secret* / *service_role* di dalam kode atau laporan dikenakan pengurangan **berat** pada aspek keempat, karena berpotensi membocorkan seluruh isi database.
- Screenshot Table Editor bersifat **wajib**. Tanpa itu, aplikasi dianggap mungkin hanya menampilkan data statis di dalam kode.
- Aplikasi yang berhenti (crash) ketika internet dimatikan tidak dianggap memenuhi ketentuan penanganan error.

---

## G. Troubleshooting Umum

**Sebelum melapor error, lakukan tiga langkah ini lebih dulu:**

1. Buka **Table Editor** dan pastikan data memang ada di sana. Bila data tidak ada di dashboard, masalahnya ada pada operasi tulis, bukan pada tampilan.
2. Baca pesan error yang muncul. `PostgrestException` selalu memuat `message` dan `code` — tampilkan keduanya dengan `print('${e.code} — ${e.message}')`.
3. Periksa apakah seluruh skrip SQL pada bagian C.2 sudah dijalankan **tanpa ada perintah yang gagal**.

| Gejala | Penyebab umum | Solusi |
|---|---|---|
| `Invalid API key` atau `No API key found in request` | `supabaseUrl` / `supabaseKey` salah, kosong, atau masih berisi contoh | Periksa `lib/config.dart`; pastikan tidak ada spasi atau baris baru di dalam tanda kutip |
| `permission denied for table menu` | `grant` pada langkah 5 skrip SQL belum dijalankan | Jalankan `grant select, insert, update, delete on public.menu to anon;` |
| `new row violates row-level security policy` | RLS aktif tetapi policy `insert` belum ada | Jalankan policy `insert ... with check (true)` |
| `select()` selalu mengembalikan daftar kosong padahal data ada di Table Editor | Policy `select` atau `grant select` belum ada | Jalankan keduanya; pastikan perannya `anon` |
| `delete()` tidak error, tetapi data tidak terhapus | Dengan RLS, baris hanya terhapus bila terlihat oleh policy `SELECT` | Tambahkan policy `select` |
| Seluruh isi tabel terubah atau terhapus sekaligus | `.eq()` tertinggal pada `update()` / `delete()` | Selalu sertakan filter penentu baris |
| `relation "public.menu" does not exist` (kode `42P01`) | Tabel belum dibuat, nama salah, atau skrip SQL gagal sebagian | Jalankan ulang skrip bagian C.2 dan periksa pesan di SQL Editor |
| `The named parameter 'publishableKey' isn't defined` | Versi `supabase_flutter` masih lama | Perbarui dengan `flutter pub upgrade supabase_flutter`, atau sementara gunakan `anonKey` |
| `There should be exactly one item with [DropdownButton]'s value` | Nilai awal dropdown tidak ada di dalam `items` (kategori dari database di luar daftar) | Bangun `items` dari data (lihat `_pilihanKategori` pada Latihan 3) |
| `A dismissed Dismissible widget is still part of the tree` | Daftar dimuat ulang sebelum penghapusan selesai (pola `FutureBuilder` pada Latihan 1–3) | Hapus di database lebih dulu, baru muat ulang (lihat `_hapusLaluMuatUlang`). Pada versi realtime (Latihan 4), jangan memuat ulang sama sekali — cukup panggil `hapusMenu()` dan biarkan stream memperbarui daftar |
| `type 'String' is not a subtype of type 'int'` | Tipe kolom database tidak cocok dengan tipe Dart | Samakan (mis. `integer` ↔ `int`, `bigint` ↔ `int`) |
| `null check operator used on a null value` | Kolom boleh `null` tetapi dibaca sebagai tipe non-null | Gunakan `as String? ?? ''` dan sejenisnya |
| Realtime tidak bekerja (data tidak ikut berubah) | Realtime belum diaktifkan untuk tabel, atau `stream` dibuat di dalam `build()` | Aktifkan Realtime di dashboard; pindahkan pembuatan stream ke `initState` |
| `SocketException: Failed host lookup` | Tidak ada koneksi internet | Periksa jaringan perangkat |
| Aplikasi berhenti saat internet dimatikan di tengah proses simpan | Operasi tulis tidak dibungkus `try`/`catch` | Bungkus dengan `try`/`catch` dan tampilkan `SnackBar` |
| Aplikasi Android versi rilis tidak dapat terhubung | Izin INTERNET hanya ada pada manifest debug | Tambahkan `<uses-permission android:name="android.permission.INTERNET"/>` di `android/app/src/main/AndroidManifest.xml` |
| Project gratis tidak merespons setelah lama tidak dibuka | Project gratis dapat dinonaktifkan sementara oleh Supabase | Buka dashboard Supabase dan aktifkan kembali project tersebut |
| Perubahan kode tidak muncul saat dijalankan | Hot reload tidak menjalankan ulang `initState` maupun `Supabase.initialize` | Tekan hot **restart** (`R`) |

---

## H. Kaitan ke Pertemuan Berikutnya

Hari ini aplikasi kita sudah memiliki database sungguhan, tetapi **belum tahu siapa yang sedang memakainya**. Akibatnya policy harus dibiarkan terbuka (`using (true)`) dan seluruh pengguna bisa mengubah data siapa pun. Pada pertemuan berikutnya kita akan:

1. **Membuat sistem login** dengan Supabase Auth: `signUp()`, `signInWithPassword()`, `signOut()`, dan `onAuthStateChange`.
2. **Menyempitkan policy** menjadi berbasis pengguna, misalnya `using (auth.uid() = user_id)` sehingga setiap orang hanya dapat mengubah datanya sendiri — sekaligus menutup kembali celah keamanan yang kita buka hari ini untuk latihan.
3. **Menyimpan foto** ke Supabase Storage dan menampilkan foto profil dari database.
4. **Menampilkan data sesuai pengguna** yang sedang login pada halaman profil.

Tiga hal terpenting untuk diingat dari pertemuan ini: **RLS adalah pengaman di dalam database, bukan di dalam aplikasi**; **`update` dan `delete` wajib memakai filter**; dan **`Future` maupun `Stream` tidak boleh dibuat di dalam `build()`**.

---

## I. Referensi

Seluruh tautan berikut diakses dan diverifikasi saat modul ini disusun:

- Panduan resmi Supabase untuk Flutter (pembuatan project, tabel, RLS, dan `select` pertama) — https://supabase.com/docs/guides/getting-started/quickstarts/flutter
- Referensi SDK Dart/Flutter (`Supabase.initialize`, `select`, `insert`, `update`, `delete`, `stream`) — https://supabase.com/docs/reference/dart/initializing
- Halaman package `supabase_flutter` di pub.dev (versi terbaru: `2.18.3`, Oktober 2026) — https://pub.dev/packages/supabase_flutter
- Panduan Row Level Security pada Supabase — https://supabase.com/docs/guides/database/postgres/row-level-security
- Referensi widget `DropdownButtonFormField` (catatan deprecation parameter `value`) — https://api.flutter.dev/flutter/material/DropdownButtonFormField-class.html

---

*Modul ini disusun untuk praktikum Pertemuan 5, sebagai kelanjutan langsung dari Modul Pertemuan 4. Versi package dan perintah SQL pada modul ini mengikuti dokumentasi resmi per Oktober 2026; bila dashboard Supabase berubah tampilan, langkah-langkah di bagian C tetap dapat dilakukan melalui SQL Editor. Silakan sesuaikan waktu dan tingkat kesulitan dengan kondisi kelas.*
