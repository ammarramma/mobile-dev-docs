# MODUL PRAKTIKUM PERTEMUAN 3

## Mata Kuliah: Pemrograman Mobile dengan Flutter

### Daftar yang Bisa Digulir & Navigasi Halaman: ListView, ListTile, GridView, dan Navigator

**Program Studi:** Teknik Informatika — Politeknik Negeri Lhokseumawe
**Waktu:** 3 × 50 menit
**Prasyarat:** Mahasiswa telah mengikuti Pertemuan 2 (Row, Column, Container, Padding, Expanded, styling teks) dan menyelesaikan Tugas Mandiri "Menu Makanan"

---

## A. Tujuan Praktikum

Setelah menyelesaikan praktikum ini, mahasiswa mampu:

1. Menjelaskan keterbatasan `Column` saat konten melebihi tinggi layar dan solusinya.
2. Menampilkan daftar data menggunakan `ListView`, `ListView.builder`, dan `ListView.separated`.
3. Menggunakan `ListTile` dan `Card` untuk membangun baris daftar yang rapi.
4. Menampilkan data dalam bentuk kisi (grid) 2 dimensi dengan `GridView.builder`.
5. Memodelkan data aplikasi ke dalam sebuah **class model** (bukan lagi list of String).
6. Berpindah antar halaman menggunakan `Navigator.push`, `MaterialPageRoute`, dan `Navigator.pop`.
7. Mengirim data dari halaman daftar ke halaman detail melalui parameter konstruktor.

---

## B. Ringkasan Materi

### B.1 Masalah: Layar Terbatas, Konten Panjang

Pada Pertemuan 2, semua widget diletakkan di dalam `Column`. `Column` **tidak bisa digulir (scroll)** — begitu tinggi total isinya melebihi layar, muncul garis kuning-hitam `RenderFlex overflowed by X pixels`.

Contoh kasus nyata: daftar 20 menu, 50 mahasiswa, atau 100 produk. Solusinya bukan memperkecil font, melainkan memakai widget **scrollable**.

| Widget                    | Kegunaan                                             | Kapan dipakai                                                    |
| ------------------------- | ---------------------------------------------------- | ---------------------------------------------------------------- |
| `SingleChildScrollView` | Membuat satu child (biasanya`Column`) bisa digulir | Halaman detail / profil yang isinya panjang                      |
| `ListView`              | Daftar gulir dengan`children` statis               | Item sedikit dan sudah pasti jumlahnya                           |
| `ListView.builder`      | Membangun item**saat dibutuhkan**              | Item banyak / dari data dinamis**(paling sering dipakai)** |
| `ListView.separated`    | Seperti`builder`, ditambah garis pemisah otomatis  | Daftar teks polos tanpa`Card`                                  |
| `GridView.builder`      | Kisi 2 dimensi (baris × kolom)                      | Katalog produk, kategori, galeri foto                            |

### B.2 ListView Dasar

```dart
ListView(
  children: const [
    ListTile(leading: Icon(Icons.home), title: Text('Beranda')),
    ListTile(leading: Icon(Icons.school), title: Text('Akademik')),
    ListTile(leading: Icon(Icons.person), title: Text('Profil')),
  ],
)
```

`ListView` sudah membungkus dirinya sendiri dengan kemampuan scroll, sehingga **tidak butuh** `SingleChildScrollView` lagi.

### B.3 ListView.builder — Pola yang Paling Sering Dipakai

```dart
ListView.builder(
  itemCount: daftarJurusan.length,
  itemBuilder: (context, index) {
    return ListTile(title: Text(daftarJurusan[index]));
  },
)
```

- `itemCount` → jumlah item.
- `itemBuilder` → dipanggil setiap kali Flutter butuh menggambar satu baris. **Hanya baris yang terlihat di layar** yang dibangun, sehingga hemat memori meski datanya ratusan.
- `index` → nomor urut item, dimulai dari `0`.

Versi dengan pemisah otomatis:

```dart
ListView.separated(
  itemCount: daftarJurusan.length,
  separatorBuilder: (context, index) => const Divider(),
  itemBuilder: (context, index) => ListTile(title: Text(daftarJurusan[index])),
)
```

### B.4 Anatomi ListTile

`ListTile` adalah *template* baris siap pakai. Menghafal bagian-bagiannya akan sangat menghemat waktu:

```
┌──────────────────────────────────────────────────────┐
│  [leading]   title                          trailing │
│  (ikon/avatar)  subtitle                             │
└──────────────────────────────────────────────────────┘
                       onTap → aksi saat baris disentuh
```

```dart
ListTile(
  leading: const Icon(Icons.fastfood),          // kiri  : ikon / CircleAvatar
  title: const Text('Mie Aceh'),                // utama : judul
  subtitle: const Text('Bumbu rempah khas Aceh'),// kedua : keterangan
  trailing: const Text('Rp 25.000'),            // kanan : harga / ikon panah
  onTap: () { /* aksi */ },
)
```

> `ListTile` otomatis membatasi jumlah baris `title` dan `subtitle`. Jika teks panjang, gunakan `maxLines` + `overflow: TextOverflow.ellipsis` pada `subtitle`.

### B.5 Card + onTap: Membuat Baris Terlihat Seperti Tombol

`Card` hanya menyediakan latar dan bayangan — ia **tidak** memiliki efek sentuhan. Agar terasa bisa ditekan, letakkan `ListTile` (punya `onTap`) **di dalam** `Card`, atau bungkus dengan `InkWell`.

```dart
Card(
  elevation: 3,
  margin: const EdgeInsets.only(bottom: 12),
  shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(16)),
  child: ListTile(
    leading: const Icon(Icons.fastfood),
    title: const Text('Mie Aceh'),
    onTap: () {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Mie Aceh dipilih')),
      );
    },
  ),
)
```

> **Deprecation:** pada Flutter 3.27+ fungsi `warna.withOpacity(0.15)` sudah *deprecated*. Gunakan `withValues(alpha: 0.15)` atau pilih langsung varian `Colors.teal.shade50`.

### B.6 GridView — Tampilan Kisi

```dart
GridView.builder(
  padding: const EdgeInsets.all(16),
  gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
    crossAxisCount: 2,      // jumlah kolom
    mainAxisSpacing: 12,    // jarak antar baris
    crossAxisSpacing: 12,   // jarak antar kolom
    childAspectRatio: 1.0,  // lebar : tinggi tiap kotak
  ),
  itemCount: daftarKategori.length,
  itemBuilder: (context, index) => /* satu kartu kategori */,
)
```

- `childAspectRatio > 1` → kotak lebih lebar (pendek).
- `childAspectRatio < 1` → kotak lebih tinggi.
- Jika isi kotak terlihat "terpotong", biasanya penyebabnya nilai ini.

### B.7 Model Class — dari List of String ke List of Objek

Mulai pertemuan ini, data **tidak lagi** disimpan sebagai `List<String>`. Kita membuat class model agar setiap item punya beberapa atribut sekaligus:

```dart
class MenuItem {
  final String nama;
  final String deskripsi;
  final int harga;
  final IconData ikon;

  const MenuItem({
    required this.nama,
    required this.deskripsi,
    required this.harga,
    required this.ikon,
  });
}
```

```dart
final List<MenuItem> daftarMenu = const [
  MenuItem(nama: 'Mie Aceh', deskripsi: '...', harga: 25000, ikon: Icons.ramen_dining),
  MenuItem(nama: 'Kopi Sanger', deskripsi: '...', harga: 15000, ikon: Icons.local_cafe),
];
```

Inilah jembatan menuju materi berikutnya: data dari API/database nantinya juga akan diubah menjadi objek seperti ini.

### B.8 Navigasi Antar Halaman

Flutter memakai konsep **stack halaman**. Halaman baru didorong ke atas stack, tombol back akan memop halaman teratas.

```dart
// 1. Membuka halaman baru
Navigator.push(
  context,
  MaterialPageRoute(
    builder: (context) => HalamanDetail(menu: menu),
  ),
);

// 2. Kembali ke halaman sebelumnya
Navigator.pop(context);
```

**Mengirim data ke halaman tujuan** — caranya lewat parameter konstruktor:

```dart
class HalamanDetail extends StatelessWidget {
  const HalamanDetail({super.key, required this.menu});

  final MenuItem menu;   // data yang diterima dari halaman daftar

  @override
  Widget build(BuildContext context) {
    return Scaffold(appBar: AppBar(title: Text(menu.nama)), /* ... */);
  }
}
```

> `Navigator.pop(context)` tidak perlu dituliskan untuk tombol back di AppBar — Flutter sudah menyediakannya otomatis saat halaman dibuka dengan `Navigator.push`. Tombol pop manual dipakai untuk tombol "Selesai" / "Kembali ke Daftar" di dalam body.

### B.9 Alur Aplikasi yang Akan Dibangun

```
HalamanKatalog (ListView.builder)
        │
        │  onTap → Navigator.push(..., menu: menu)
        ▼
HalamanDetail (menerima objek MenuItem)
        │
        │  Navigator.pop(context)
        ▼
kembali ke HalamanKatalog
```

---

## C. Persiapan

1. Flutter SDK terinstal dan `flutter doctor` tanpa error kritis (sudah dicek pada Pertemuan 1).
2. Siapkan hasil Tugas Mandiri Pertemuan 2 (aplikasi "Menu Makanan") di folder terpisah — akan dipakai sebagai bahan di Latihan 2–4.
3. Buat project baru:

```bash
flutter create pnl_katalog
cd pnl_katalog
flutter run
```

4. Karena latihan hari ini cukup panjang, seluruh kode akan ditulis di dalam satu file `lib/main.dart` agar mudah dijalankan. Pemisahan ke beberapa file akan dibahas sebagai nilai tambah.

---

## D. Praktikum Terpandu

### Latihan 1 — Membuktikan Masalah Overflow, lalu Memperbaiki dengan ListView (20 menit)

**Tahap A — reproduksi masalah.**

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
        appBar: AppBar(title: const Text('Latihan 1 - Column vs ListView')),
        body: Column(
          children: List.generate(
            20,
            (index) => Container(
              height: 80,
              margin: const EdgeInsets.all(8),
              color: Colors.teal.shade100,
              alignment: Alignment.center,
              child: Text('Item ke-${index + 1}'),
            ),
          ),
        ),
      ),
    );
  }
}
```

Jalankan aplikasi. Garis kuning-hitam akan muncul di bagian bawah layar dengan pesan `RenderFlex overflowed by ... pixels`. **Ini perilaku yang benar** — Flutter sedang memberi tahu bahwa isi `Column` tidak muat di layar.

**Tahap B — perbaikan.** Ubah `Column` pada `body` menjadi `ListView`:

```dart
body: ListView(
  children: List.generate(
    20,
    (index) => Container(
      height: 80,
      margin: const EdgeInsets.all(8),
      color: Colors.teal.shade100,
      alignment: Alignment.center,
      child: Text('Item ke-${index + 1}'),
    ),
  ),
),
```

**Tugas mahasiswa:**

1. Tuliskan pesan error lengkap yang muncul pada Tahap A di laporan Anda.
2. Setelah Tahap B, gulir layar ke bawah. Apakah semua 20 item dapat dilihat?
3. Bungkus `ListView` di atas dengan `SingleChildScrollView(...)`. Jalankan — apa yang terjadi? Jelaskan mengapa.
4. Ubah `ListView` menjadi `ListView.builder` dengan `itemCount: 20` dan `itemBuilder: (context, index) => ...`. Apakah tampilannya sama dengan Tahap B?

> **Catatan asisten:** tujuan tahap A adalah menunjukkan gejala overflow secara sengaja (sudah disebut pada modul Pertemuan 2). Jangan langsung memberi solusi — biarkan mahasiswa membaca pesan error dan mencoba `SingleChildScrollView` yang salah lebih dulu pada tugas nomor 3.

> **Catatan asisten:** pada tugas nomor 3, `SingleChildScrollView` yang membungkus `ListView` **tidak error**, tetapi scroll-nya menjadi aneh/berat karena terjadi dua lapis area gulir. Kaitkan dengan aturan praktis: *jangan menaruh widget scrollable di dalam widget scrollable dengan arah yang sama.*

### Latihan 2 — ListView.builder + Card + ListTile + Model Class (25 menit)

```dart
import 'package:flutter/material.dart';

void main() => runApp(const MyApp());

/// Model data menu. Satu objek menyimpan 4 informasi sekaligus.
class MenuItem {
  final String nama;
  final String deskripsi;
  final int harga;
  final IconData ikon;

  const MenuItem({
    required this.nama,
    required this.deskripsi,
    required this.harga,
    required this.ikon,
  });
}

/// Helper kecil: mengubah 25000 menjadi "Rp 25.000". Boleh disalin apa adanya.
String formatRupiah(int nilai) {
  final pola = RegExp(r'\B(?=(\d{3})+(?!\d))');
  final hasil = nilai.toString().replaceAllMapped(pola, (match) => '.');
  return 'Rp $hasil';
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  final List<MenuItem> daftarMenu = const [
    MenuItem(
      nama: 'Mie Aceh',
      deskripsi: 'Mie tebal dengan kuah bumbu rempah khas Aceh',
      harga: 25000,
      ikon: Icons.ramen_dining,
    ),
    MenuItem(
      nama: 'Kopi Sanger',
      deskripsi: 'Kopi robusta diseduh dengan susu kental manis',
      harga: 15000,
      ikon: Icons.local_cafe,
    ),
    MenuItem(
      nama: 'Ayam Tangkap',
      deskripsi: 'Ayam goreng dengan daun kari dan daun pandan',
      harga: 35000,
      ikon: Icons.lunch_dining,
    ),
    MenuItem(
      nama: 'Pisang Goreng Keju',
      deskripsi: 'Pisang goreng renyah dengan topping keju parut',
      harga: 12000,
      ikon: Icons.bakery_dining,
    ),
    MenuItem(
      nama: 'Es Timun Serut',
      deskripsi: 'Minuman segar dari timun serut dan jeruk nipis',
      harga: 10000,
      ikon: Icons.local_drink,
    ),
  ];

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Latihan 2 - Daftar Menu'),
          backgroundColor: Colors.teal,
          foregroundColor: Colors.white,
        ),
        body: ListView.builder(
          padding: const EdgeInsets.all(12),
          itemCount: daftarMenu.length,
          itemBuilder: (context, index) {
            final menu = daftarMenu[index];

            return Card(
              margin: const EdgeInsets.only(bottom: 12),
              elevation: 3,
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(16),
              ),
              child: ListTile(
                contentPadding: const EdgeInsets.symmetric(
                  horizontal: 16,
                  vertical: 8,
                ),
                leading: CircleAvatar(
                  backgroundColor: Colors.teal.shade50,
                  child: Icon(menu.ikon, color: Colors.teal),
                ),
                title: Text(
                  menu.nama,
                  style: const TextStyle(fontWeight: FontWeight.bold),
                ),
                subtitle: Text(
                  menu.deskripsi,
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
                onTap: () {
                  ScaffoldMessenger.of(context).showSnackBar(
                    SnackBar(
                      content: Text('Anda memilih ${menu.nama}'),
                      duration: const Duration(seconds: 1),
                    ),
                  );
                },
              ),
            );
          },
        ),
      ),
    );
  }
}
```

**Tugas mahasiswa:**

1. Tambahkan **dua menu baru** dengan ikon berbeda (lihat daftar ikon di `Icons.`).
2. Hapus `subtitle`. Bagaimana perubahan tinggi tiap baris?
3. Ubah `ListView.builder` menjadi `ListView.separated` dan gunakan `Divider()` sebagai pemisah. Apa yang berubah pada tampilan `Card`?
4. Coba hapus `onTap` dari `ListTile` dan pindahkan ke `Card` (menulis `onTap:` di dalam `Card`). Apakah kode bisa dijalankan? Jelaskan hasilnya di laporan.
5. Ubah `elevation: 3` menjadi `elevation: 0`. Apa yang hilang dari tampilan?

> **Catatan asisten:** tugas nomor 4 sengaja menjebak — `Card` **tidak memiliki** properti `onTap`, sehingga muncul error "The named parameter 'onTap' isn't defined". Gunakan momen ini untuk menegaskan bahwa kita harus membaca pesan error IDE, bukan menebak. Solusi resminya adalah `InkWell` di dalam `Card`.

### Latihan 3 — GridView: Halaman Kategori (20 menit)

Buat file sementara (boleh menimpa `main.dart`, salin dulu Latihan 2 jika ingin disimpan):

```dart
import 'package:flutter/material.dart';

void main() => runApp(const MyApp());

class Kategori {
  final String nama;
  final IconData ikon;
  final Color warna;

  const Kategori(this.nama, this.ikon, this.warna);
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  final List<Kategori> daftarKategori = const [
    Kategori('Makanan', Icons.restaurant, Colors.orange),
    Kategori('Minuman', Icons.local_drink, Colors.teal),
    Kategori('Kue & Roti', Icons.cake, Colors.pink),
    Kategori('Kopi', Icons.coffee, Colors.brown),
    Kategori('Jajanan', Icons.bakery_dining, Colors.indigo),
    Kategori('Buah', Icons.eco, Colors.green),
  ];

  Widget kartuKategori(Kategori kategori) {
    return Container(
      decoration: BoxDecoration(
        color: kategori.warna.withValues(alpha: 0.12),
        borderRadius: BorderRadius.circular(16),
        border: Border.all(color: kategori.warna.withValues(alpha: 0.4)),
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          Icon(kategori.ikon, size: 40, color: kategori.warna),
          const SizedBox(height: 10),
          Text(
            kategori.nama,
            style: TextStyle(
              fontWeight: FontWeight.bold,
              color: kategori.warna,
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        appBar: AppBar(
          title: const Text('Latihan 3 - Kategori'),
          backgroundColor: Colors.teal,
          foregroundColor: Colors.white,
        ),
        body: GridView.builder(
          padding: const EdgeInsets.all(16),
          gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
            crossAxisCount: 2,
            mainAxisSpacing: 12,
            crossAxisSpacing: 12,
            childAspectRatio: 1.1,
          ),
          itemCount: daftarKategori.length,
          itemBuilder: (context, index) => kartuKategori(daftarKategori[index]),
        ),
      ),
    );
  }
}
```

> Jika Flutter Anda versi di bawah 3.27, ganti `withValues(alpha: 0.12)` menjadi `withOpacity(0.12)`.

**Tugas mahasiswa:**

1. Ubah `crossAxisCount` menjadi `3`, lalu `1`. Amati perubahan ukuran dan jumlah kolom.
2. Ubah `childAspectRatio` menjadi `0.7`, lalu `1.6`. Kapan isi kotak mulai terlihat terpotong?
3. Ganti `GridView.builder` dengan `GridView.count`, isi `children` secara manual dengan `kartuKategori(...)`. Apa perbedaan penulisan keduanya?
4. Tambahkan `onTap` pada tiap kartu kategori (bungkus dengan `GestureDetector` atau `InkWell`) yang menampilkan `SnackBar` berisi nama kategori.

> **Catatan asisten:** bila mahasiswa melaporkan "kotak jadi tinggi aneh / teks kepotong", itu murni efek `childAspectRatio`. Arahkan untuk menghitung: lebar layar ÷ jumlah kolom, lalu bandingkan dengan tinggi yang dihasilkan rasio tersebut.

### Latihan 4 — Proyek Mini: Katalog + Halaman Detail (35 menit)

Ini latihan inti hari ini: menggabungkan daftar gulir dengan navigasi ke halaman detail. Mahasiswa mengerjakan mandiri, dosen/asisten berkeliling membimbing.

**Ketentuan wajib:**

1. Satu halaman **Katalog** berisi `ListView.builder` minimal 6 item menu.
2. Setiap item memakai `Card` + `ListTile`, dan **seluruh `Card` (bukan hanya sebagian baris) dapat ditekan**.
3. Menekan sebuah item membuka halaman **Detail** yang menampilkan: ikon/foto besar, nama, harga, dan deskripsi yang lebih panjang.
4. Halaman Detail menerima objek `MenuItem` melalui **konstruktor**, bukan variabel global.
5. Terdapat tombol **"Kembali ke Daftar"** di halaman Detail yang memanggil `Navigator.pop(context)`.
6. Halaman Detail dapat digulir (gunakan `SingleChildScrollView`) dan tidak menghasilkan overflow pada layar kecil.

**Struktur pohon widget yang disarankan (hint):**

```
MaterialApp
└── HalamanKatalog (Scaffold)
    ├── AppBar
    └── ListView.builder
        └── Card
            └── ListTile
                ├── leading : CircleAvatar + Hero
                ├── title   : Text(nama)
                ├── subtitle: Text(deskripsi)
                ├── trailing: Text(harga)
                └── onTap → Navigator.push
                               └── HalamanDetail (Scaffold)
                                   ├── AppBar
                                   └── SingleChildScrollView
                                       └── Column
                                           ├── Hero + CircleAvatar (ikon besar)
                                           ├── Text(nama)
                                           ├── Text(harga)
                                           ├── Divider
                                           ├── Text(deskripsi)
                                           └── ElevatedButton "Kembali ke Daftar"
```

**Kode acuan:**

```dart
import 'package:flutter/material.dart';

void main() => runApp(const MyApp());

class MenuItem {
  final String nama;
  final String deskripsi;
  final int harga;
  final IconData ikon;

  const MenuItem({
    required this.nama,
    required this.deskripsi,
    required this.harga,
    required this.ikon,
  });
}

String formatRupiah(int nilai) {
  final pola = RegExp(r'\B(?=(\d{3})+(?!\d))');
  final hasil = nilai.toString().replaceAllMapped(pola, (match) => '.');
  return 'Rp $hasil';
}

const Color warnaTema = Colors.teal;

// ---------------- HALAMAN 1: KATALOG ----------------
class HalamanKatalog extends StatelessWidget {
  const HalamanKatalog({super.key});

  final List<MenuItem> daftarMenu = const [
    MenuItem(
      nama: 'Mie Aceh',
      deskripsi: 'Mie tebal dengan kuah bumbu rempah khas Aceh, disajikan dengan '
          'acar bawang dan emping. Tersedia pilihan goreng maupun kuah.',
      harga: 25000,
      ikon: Icons.ramen_dining,
    ),
    MenuItem(
      nama: 'Kopi Sanger',
      deskripsi: 'Kopi robusta Gayo diseduh dengan susu kental manis, disajikan '
          'panas dalam gelas kaca. Menu wajib bagi penikmat kopi Aceh.',
      harga: 15000,
      ikon: Icons.local_cafe,
    ),
    MenuItem(
      nama: 'Ayam Tangkap',
      deskripsi: 'Ayam goreng khas Aceh yang ditaburi daun kari dan daun pandan '
          'goreng. Aromanya kuat dan gurih.',
      harga: 35000,
      ikon: Icons.lunch_dining,
    ),
    MenuItem(
      nama: 'Pisang Goreng Keju',
      deskripsi: 'Pisang goreng renyah dengan topping keju parut dan susu kental '
          'manis. Cocok sebagai camilan sore.',
      harga: 12000,
      ikon: Icons.bakery_dining,
    ),
    MenuItem(
      nama: 'Es Timun Serut',
      deskripsi: 'Minuman segar dari timun serut, jeruk nipis, dan sirup gula. '
          'Pelepas dahaga paling pas di siang hari.',
      harga: 10000,
      ikon: Icons.local_drink,
    ),
    MenuItem(
      nama: 'Timphan',
      deskripsi: 'Kue tradisional Aceh dari tepung ketan berisi serikaya, '
          'dibungkus daun pisang lalu dikukus.',
      harga: 8000,
      ikon: Icons.cake,
    ),
  ];

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Katalog Menu'),
        backgroundColor: warnaTema,
        foregroundColor: Colors.white,
      ),
      body: ListView.builder(
        padding: const EdgeInsets.all(12),
        itemCount: daftarMenu.length,
        itemBuilder: (context, index) {
          final menu = daftarMenu[index];

          return Card(
            margin: const EdgeInsets.only(bottom: 12),
            elevation: 3,
            shape: RoundedRectangleBorder(
              borderRadius: BorderRadius.circular(16),
            ),
            child: ListTile(
              contentPadding: const EdgeInsets.symmetric(
                horizontal: 16,
                vertical: 8,
              ),
              leading: CircleAvatar(
                backgroundColor: warnaTema.shade50,
                child: Icon(menu.ikon, color: warnaTema),
              ),
              title: Text(
                menu.nama,
                style: const TextStyle(fontWeight: FontWeight.bold),
              ),
              subtitle: Text(
                menu.deskripsi,
                maxLines: 1,
                overflow: TextOverflow.ellipsis,
              ),
              trailing: Text(
                formatRupiah(menu.harga),
                style: const TextStyle(
                  fontWeight: FontWeight.bold,
                  color: warnaTema,
                ),
              ),
              onTap: () {
                Navigator.push(
                  context,
                  MaterialPageRoute(
                    builder: (context) => HalamanDetail(menu: menu),
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

// ---------------- HALAMAN 2: DETAIL ----------------
class HalamanDetail extends StatelessWidget {
  const HalamanDetail({super.key, required this.menu});

  final MenuItem menu; // data yang diterima dari halaman katalog

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(menu.nama),
        backgroundColor: warnaTema,
        foregroundColor: Colors.white,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            CircleAvatar(
              radius: 56,
              backgroundColor: warnaTema.shade50,
              child: Icon(menu.ikon, size: 56, color: warnaTema),
            ),
            const SizedBox(height: 24),
            Text(
              menu.nama,
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Text(
              formatRupiah(menu.harga),
              textAlign: TextAlign.center,
              style: const TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: warnaTema,
              ),
            ),
            const SizedBox(height: 24),
            const Divider(),
            const SizedBox(height: 8),
            const Text(
              'Deskripsi',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Text(menu.deskripsi, style: const TextStyle(height: 1.5)),
            const SizedBox(height: 32),
            ElevatedButton.icon(
              onPressed: () => Navigator.pop(context),
              icon: const Icon(Icons.arrow_back),
              label: const Text('Kembali ke Daftar'),
            ),
          ],
        ),
      ),
    );
  }
}

// ---------------- ENTRY POINT ----------------
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
```

**Tugas mahasiswa:**

1. Jalankan aplikasi, tekan beberapa item, dan pastikan halaman detail tampil sesuai item yang ditekan.
2. Tambahkan **"Pilihan Level Pedas"** pada halaman detail: `Row` berisi tiga `ChoiceChip` (Level 1, 2, 3). Karena pilihan ini berubah, halaman detail harus diubah menjadi `StatefulWidget`. Jelaskan perubahan apa saja yang Anda lakukan di laporan.
3. Tambahkan baris `Text('Total: ...')` di halaman detail yang menghitung `harga × jumlah`. Gunakan variabel `int jumlah` dan tombol `+` / `−` (opsional).
4. Bungkus `CircleAvatar` pada halaman katalog dengan `Hero(tag: menu.nama, child: ...)` dan lakukan hal yang sama di halaman detail. Jalankan perlahan — efek animasi apa yang muncul?
5. Pisahkan kode menjadi tiga file: `lib/models/menu_item.dart`, `lib/pages/halaman_katalog.dart`, dan `lib/pages/halaman_detail.dart`. **Ini nilai tambah** — jangan lakukan sebelum aplikasi utama berjalan lancar.

> **Catatan asisten:** kesalahan paling sering di latihan ini adalah (a) lupa mengirim `menu:` saat `Navigator.push`, sehingga muncul error "required argument", dan (b) menulis `HalamanDetail()` tanpa parameter. Keduanya sudah dicakup di tabel troubleshooting bagian G.

---

## E. Tugas Mandiri (Dikumpulkan)

Kembangkan **hasil Tugas Mandiri Pertemuan 2 (Menu Makanan)** menjadi aplikasi dua halaman yang lengkap. Ketentuan:

1. **Halaman Katalog** — `AppBar` berjudul nama kafe/rumah makan pilihan Anda, berisi `ListView.builder` dengan **minimal 8 item menu**. Setiap item wajib memakai `Card` + `ListTile` yang dapat ditekan.
2. **Halaman Kategori** — satu halaman berisi `GridView.builder` dengan **minimal 6 kategori** (contoh: Makanan, Minuman, Kopi, Kue, Jajanan, Buah). Halaman ini dapat dibuka dari tombol pada `AppBar` halaman katalog (`actions: [IconButton(...)]`).
3. **Halaman Detail** — terbuka saat item katalog ditekan, menampilkan ikon/foto besar, nama, harga, deskripsi lengkap, dan tombol kembali.
4. **Model class** `MenuItem` (atau nama lain yang relevan) dengan minimal 4 atribut, digunakan untuk seluruh data aplikasi.
5. **Ketentuan teknis:**
   - Minimal 3 halaman saling terhubung dengan `Navigator.push`.
   - Mengirim data antar halaman melalui parameter konstruktor (`required this.xxx`).
   - Halaman detail memakai `SingleChildScrollView` dan tidak menghasilkan overflow.
   - Warna tema konsisten, `borderRadius`, dan `boxShadow` diterapkan pada kartu.
6. **Nilai tambah (opsional):**
   - `Hero` animation pada ikon antara katalog dan detail.
   - `SnackBar` konfirmasi saat tombol "Pesan" di halaman detail ditekan.
   - Memisahkan kode ke dalam beberapa file (`models/`, `pages/`).
   - Judul `AppBar` katalog menampilkan jumlah item, misal "Katalog Menu (8)".

**Pengumpulan:** seluruh file `.dart` (atau arsip project) + **screenshot 3 halaman** (katalog, kategori, detail) + laporan singkat (PDF) yang menjawab pertanyaan pada setiap Latihan 1–4. Kumpulkan sebelum pertemuan berikutnya.

---

## F. Rubrik Penilaian (Total 100)

| Aspek                                                                      | Bobot |
| -------------------------------------------------------------------------- | ----- |
| Latihan 1–3 selesai dan jawaban pertanyaan benar                          | 25    |
| Latihan 4 (Katalog + Detail) sesuai semua ketentuan wajib                  | 30    |
| Tugas Mandiri: kelengkapan ketentuan (3 halaman, jumlah item, model class) | 25    |
| Tugas Mandiri: kerapian kode, struktur folder & kreativitas tampilan       | 20    |

**Catatan penilaian:**

- Penggunaan `List<String>` untuk data menu (bukan model class) pada Tugas Mandiri dikenakan pengurangan pada aspek ketiga.
- Aplikasi yang berjalan tetapi halaman detail tidak menerima data yang benar (mis. selalu menampilkan item pertama) tidak dianggap memenuhi ketentuan nomor 3.

---

## G. Troubleshooting Umum

| Gejala                                                 | Penyebab umum                                                                         | Solusi                                                                                                                                       |
| ------------------------------------------------------ | ------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------- |
| `RenderFlex overflowed by X pixels`                  | `Column` berisi konten lebih tinggi dari layar                                      | Ganti ke`ListView` / `SingleChildScrollView`                                                                                             |
| `Vertical viewport was given unbounded height`       | `ListView` diletakkan di dalam `Column` tanpa batas tinggi                        | Bungkus dengan`Expanded`, atau beri `SizedBox(height: ...)`, atau set `shrinkWrap: true` + `physics: NeverScrollableScrollPhysics()` |
| `The named parameter 'onTap' isn't defined`          | Menulis`onTap` langsung di dalam `Card`                                           | Pindahkan`onTap` ke `ListTile` di dalam `Card`, atau bungkus `Card` dengan `InkWell`                                               |
| `The required argument 'menu' must be provided`      | Objek tidak dikirim saat`Navigator.push`                                            | Tulis`MaterialPageRoute(builder: (context) => HalamanDetail(menu: menu))`                                                                  |
| Halaman detail kosong / data salah                     | Menerima data lewat variabel global, bukan konstruktor                                | Jadikan`final MenuItem menu;` dan isi dari parameter `required this.menu`                                                                |
| Konten grid terlihat terpotong / kotak terlalu tinggi  | Nilai`childAspectRatio` tidak sesuai isi                                            | Sesuaikan:`> 1` lebih lebar, `< 1` lebih tinggi                                                                                          |
| `setState() or markNeedsBuild() called during build` | Memanggil`setState` di dalam `build`                                              | Pindahkan`setState` ke dalam callback (`onPressed`, `onTap`)                                                                           |
| `setState() called after dispose()`                  | Berpindah halaman saat proses asinkron masih berjalan                                 | Periksa`if (!mounted) return;` sebelum `setState`                                                                                        |
| Scroll pada halaman detail tidak jalan                 | `SingleChildScrollView` diletakkan di dalam `Column` yang lebih tinggi dari layar | Pastikan`SingleChildScrollView` menjadi **anak langsung** `Scaffold.body`                                                          |
| Perubahan kode tidak muncul setelah edit model class   | Hot reload tidak selalu memperbarui perubahan struktur class                          | Tekan**hot restart** (`R` besar di terminal / ikon restart di IDE)                                                                   |

---

## H. Kaitan ke Pertemuan Berikutnya

Aplikasi yang dibangun hari ini masih menyimpan data di dalam kode (`hardcoded`). Pada pertemuan berikutnya kita akan:

1. Mengambil data dari **internet** menggunakan package `http` dan menampilkan hasilnya di `ListView.builder` (dengan indikator loading dan penanganan error).
2. Mengubah respons JSON menjadi objek model — pola yang sama dengan `MenuItem` hari ini.
3. Menyimpan data sederhana di perangkat, serta memperkenalkan `FutureBuilder`.

Fondasi yang paling penting untuk diingat: **`ListView.builder` + model class + `Navigator`** akan terus dipakai sampai akhir semester.

---

*Modul ini disusun untuk praktikum Pertemuan 3, sebagai kelanjutan langsung dari Modul Pertemuan 2. Silakan sesuaikan waktu dan tingkat kesulitan dengan kondisi kelas.*
