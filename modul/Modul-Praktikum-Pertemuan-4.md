# MODUL PRAKTIKUM PERTEMUAN 4
## Mata Kuliah: Pemrograman Mobile dengan Flutter
### Mengambil Data dari Internet: Package http, JSON, dan FutureBuilder

**Program Studi:** Teknik Informatika — Politeknik Negeri Lhokseumawe
**Waktu:** 3 × 50 menit
**Prasyarat:** Mahasiswa telah mengikuti Pertemuan 3 (ListView.builder, Card + ListTile, model class, dan `Navigator.push` ke halaman detail)

---

## A. Tujuan Praktikum

Setelah menyelesaikan praktikum ini, mahasiswa mampu:

1. Menjelaskan konsep client–server dan REST API serta membedakannya dengan data *hardcoded*.
2. Menambahkan package eksternal (`http`) ke dalam project Flutter melalui `pubspec.yaml`.
3. Menggunakan `Future` dan `async`/`await` untuk menunggu proses yang butuh waktu.
4. Mengambil data dari server dengan `http.get()` dan memeriksa `statusCode`.
5. Mengubah (decode) respons JSON dari server menjadi objek Dart dengan `factory fromJson`.
6. Menampilkan tiga keadaan pengambilan data — **menunggu**, **berhasil**, dan **gagal** — menggunakan `FutureBuilder`.
7. Menampilkan gambar dari internet dengan `Image.network` beserta penanganan kegagalannya.

---

## B. Ringkasan Materi

### B.1 Dari Data Hardcoded ke Data dari Server

Seluruh aplikasi yang kita bangun pada Pertemuan 2 dan 3 menyimpan data **di dalam kode**:

```dart
final List<MenuItem> daftarMenu = const [
  MenuItem(nama: 'Mie Aceh', harga: 25000, ...),
  // ...
];
```

Cara ini punya tiga masalah: data tidak bisa berubah tanpa membangun ulang aplikasi, tidak bisa dibagikan ke semua pengguna, dan tidak cocok untuk data yang banyak. Aplikasi nyata mengambil data dari **server** melalui internet.

```
   Aplikasi Flutter                     Server (API)
   (client)                             
        │                                   
        │  1. HTTP GET /filter.php?c=Seafood
        ├──────────────────────────────────►
        │                                   
        │  2. respons JSON
        ◄──────────────────────────────────┤
        │                                   
   3. decode JSON → List<Meal> → tampilkan
```

Poin penting yang harus dipahami mahasiswa:

- **API** = pintu masuk resmi untuk meminta data ke server, berbentuk alamat (endpoint) yang mengembalikan data terstruktur (umumnya JSON).
- **Endpoint** = satu alamat spesifik, misalnya `lookup.php?i=52772`.
- Aplikasi Flutter **tidak** bisa memanggil database server secara langsung — selalu melalui API.

### B.2 Menambahkan Package http

Package `http` bukan bagian dari Flutter SDK, sehingga harus ditambahkan dulu. Cara paling mudah dan disarankan:

```bash
flutter pub add http
```

Perintah tersebut otomatis mengubah `pubspec.yaml` menjadi seperti berikut:

```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^1.6.0          # versi terbaru saat modul ini disusun
```

Setelah itu jalankan `flutter pub get` (biasanya sudah otomatis), lalu tambahkan import di file Dart:

```dart
import 'dart:convert';          // untuk jsonDecode
import 'package:http/http.dart' as http;
```

> `as http` berfungsi memberi nama panggilan pada package, sehingga penulisannya menjadi `http.get(...)` dan menghindari benturan nama dengan class lain.

### B.3 Future dan async/await

Mengambil data dari internet **butuh waktu** (bisa 0,5 detik, bisa 10 detik jika jaringan lambat). Dart menangani proses seperti ini dengan `Future`.

```dart
Future<String> ambilPesan() async {
  await Future.delayed(const Duration(seconds: 2)); // meniru proses lambat
  return 'Data sudah siap';
}

void main() async {
  print('Mulai meminta data...');
  final hasil = await ambilPesan();  // berhenti menunggu, tidak membekukan layar
  print(hasil);                      // baru dijalankan setelah data siap
}
```

Aturan praktis:

| Kata kunci | Arti |
|---|---|
| `Future<T>` | "Nanti akan ada nilai bertipe `T`" |
| `async` | Menandai fungsi yang di dalamnya ada proses menunggu |
| `await` | Menunggu sampai `Future` selesai, lalu mengambil nilainya |
| Hanya boleh dipakai di dalam fungsi `async` | `await` di luar fungsi `async` akan error |

**Analogi yang aman dipakai di kelas:** memesan makanan di restoran. Anda tidak berdiri di dapur menunggu (itu artinya layar membeku), melainkan menerima *nomor pesanan* (`Future`) dan melanjutkan aktivitas lain sampai pesanan dipanggil (`await`).

### B.4 http.get dan Status Code

```dart
final response = await http.get(
  Uri.parse('https://www.themealdb.com/api/json/v1/1/filter.php?c=Seafood'),
);

print(response.statusCode);  // 200 kalau berhasil
print(response.body);        // isi respons berupa teks (string JSON)
```

`response.body` masih berupa **teks**, belum bisa dipakai sebagai data.

| Status | Arti | Yang harus dilakukan aplikasi |
|---|---|---|
| `200` | OK | Lanjut memproses data |
| `201` | Created | Data berhasil dikirim (khusus POST) |
| `400` | Bad Request | Parameter permintaan salah |
| `401` / `403` | Unauthorized / Forbidden | Perlu login atau API key |
| `404` | Not Found | Endpoint salah atau data tidak ada |
| `500` | Server Error | Masalah di sisi server, tampilkan pesan "coba lagi nanti" |

> Kesalahan paling umum mahasiswa: **tidak memeriksa `statusCode`** dan langsung memanggil `jsonDecode`. Jika server membalas halaman HTML error, `jsonDecode` akan gagal dengan `FormatException`.

### B.5 jsonDecode: Objek vs Array

`jsonDecode()` (dari `dart:convert`) mengubah teks JSON menjadi struktur Dart.

**Kasus 1 — respons berupa array.** Perhatikan karakter pertamanya `[`:

```json
[
  { "userId": 1, "id": 1, "title": "sunt aut facere..." },
  { "userId": 1, "id": 2, "title": "qui est esse" }
]
```

```dart
final data = jsonDecode(response.body) as List<dynamic>;
print(data.length);          // jumlah item
print(data[0]['title']);     // ambil field dari item pertama
```

**Kasus 2 — respons berupa objek.** Perhatikan karakter pertamanya `{`:

```json
{
  "meals": [
    { "strMeal": "Baked salmon with fennel & tomatoes", "idMeal": "52959" }
  ]
}
```

```dart
final data = jsonDecode(response.body) as Map<String, dynamic>;
final daftar = data['meals'] as List<dynamic>;   // array-nya ada di dalam key "meals"
print(daftar.first['strMeal']);
```

**Aturan cepat:** buka endpoint di browser, lihat karakter pertama responsnya.

- Diawali `[` → `as List<dynamic>`
- Diawali `{` → `as Map<String, dynamic>`, lalu ambil array di dalam key tertentu

> Perhatikan juga perbedaan **`[]` untuk List** dan **`['key']` untuk Map**. Salah memilih akan menghasilkan error `type 'List<dynamic>' is not a subtype of type 'Map<String, dynamic>'`.

### B.6 Model Class dengan factory fromJson

Sama seperti Pertemuan 3, data dari API juga diubah menjadi objek. Bedanya, sekarang objek dibuat **dari JSON**, bukan ditulis manual:

```dart
class Meal {
  final String id;
  final String nama;
  final String gambar;
  final String area;
  final String kategori;
  final String instruksi;

  const Meal({
    required this.id,
    required this.nama,
    required this.gambar,
    required this.area,
    required this.kategori,
    required this.instruksi,
  });

  /// Membuat objek Meal dari satu Map hasil jsonDecode.
  factory Meal.fromJson(Map<String, dynamic> json) {
    return Meal(
      id: json['idMeal'] as String? ?? '',
      nama: json['strMeal'] as String? ?? 'Tanpa Nama',
      gambar: json['strMealThumb'] as String? ?? '',
      area: json['strArea'] as String? ?? 'Internasional',
      kategori: json['strCategory'] as String? ?? '-',
      instruksi: json['strInstructions'] as String? ?? 'Belum ada instruksi.',
    );
  }
}
```

Dua hal yang wajib dijelaskan:

1. **`factory`** adalah constructor khusus yang melakukan perhitungan sebelum mengembalikan objek. Di sini tugasnya mengubah `Map` menjadi objek.
2. **`as String? ?? 'nilai default'`** sangat penting. JSON dari server bisa berisi `null` pada suatu field. Tanpa `??` dan tanpa `String?`, aplikasi akan berhenti dengan error `type 'Null' is not a subtype of type 'String'`.

### B.7 Menampilkan Gambar dari Internet

```dart
Image.network(
  meal.gambar,
  width: 64,
  height: 64,
  fit: BoxFit.cover,
  loadingBuilder: (context, child, progress) {
    if (progress == null) return child;               // gambar selesai dimuat
    return const SizedBox(
      width: 64,
      height: 64,
      child: Center(child: CircularProgressIndicator(strokeWidth: 2)),
    );
  },
  errorBuilder: (context, error, stackTrace) {
    return const Icon(Icons.broken_image, size: 40);  // jika URL salah / offline
  },
)
```

`errorBuilder` bukan pelengkap, melainkan **keharusan**: URL gambar saat ini banyak yang dinamis dan bisa berubah. Tanpa `errorBuilder`, aplikasi menampilkan kotak merah "Exception caught by image resource service".

### B.8 Tiga Keadaan Pengambilan Data

Saat data diambil dari internet, aplikasi **selalu** berada di salah satu dari tiga keadaan berikut. Aplikasi yang baik menangani ketiganya:

| Keadaan | Yang dilihat pengguna |
|---|---|
| Menunggu (loading) | `CircularProgressIndicator` atau *skeleton* |
| Berhasil | Daftar data |
| Gagal | Pesan jelas + tombol "Coba Lagi" |

**Cara 1 — manual dengan `setState` (dari Latihan 1 dan 2).** Kita menyimpan sendiri status loading dan pesan error:

```dart
bool sedangMemuat = true;
String pesanError = '';
List<Meal> daftarMeal = [];
```

**Cara 2 — `FutureBuilder` (dari Latihan 3).** Flutter yang mengelola ketiga keadaan tersebut:

```dart
FutureBuilder<List<Meal>>(
  future: futureMeal,                        // Future yang sedang ditunggu
  builder: (context, snapshot) {
    // 1. Menunggu
    if (snapshot.connectionState == ConnectionState.waiting) {
      return const Center(child: CircularProgressIndicator());
    }
    // 2. Gagal
    if (snapshot.hasError) {
      return Center(child: Text('Gagal memuat data:\n${snapshot.error}'));
    }
    // 3. Berhasil
    final daftar = snapshot.data ?? [];
    return ListView.builder(itemCount: daftar.length, itemBuilder: ...);
  },
)
```

Perbedaan keduanya:

| Aspek | `setState` manual | `FutureBuilder` |
|---|---|---|
| Kode | Lebih panjang | Lebih ringkas |
| Keadaan loading/error | Dikelola sendiri | Disediakan `snapshot` |
| Kontrol | Bebas, mudah menambahkan logika | Terikat pada alur `snapshot` |
| Cocok untuk | Aksi tombol, proses bertahap | Menampilkan hasil satu permintaan |

> Mahasiswa harus **mencoba keduanya**: Latihan 1–2 memang sengaja memakai `setState` agar terlihat jelas apa yang sebenarnya terjadi, baru Latihan 3 memakai `FutureBuilder` sebagai cara yang lebih ringkas.

### B.9 API yang Dipakai Praktikum Ini

Seluruh latihan memakai **TheMealDB** (gratis, tanpa API key, data berupa resep makanan — lanjutan tema katalog menu Pertemuan 2 dan 3). Kedua endpoint berikut sudah diuji dan berjalan.

| Kegunaan | Endpoint | Bentuk respons |
|---|---|---|
| Daftar ringkas (untuk katalog) | `https://www.themealdb.com/api/json/v1/1/filter.php?c=Seafood` | Objek berisi array `meals` (idMeal, strMeal, strMealThumb, strArea) |
| Detail lengkap satu item | `https://www.themealdb.com/api/json/v1/1/lookup.php?i=52772` | Objek berisi array `meals` **berisi satu item** (ditambah strCategory, strInstructions) |

Perhatikan: endpoint `filter.php` **tidak** mengembalikan `strInstructions`. Itulah sebabnya halaman detail harus meminta data lagi ke server. Inilah yang terjadi pada aplikasi nyata — daftar dan detail sering berasal dari dua endpoint berbeda.

### B.10 Alur Aplikasi yang Akan Dibangun

```
HalamanKatalog
      │
      │  GET filter.php?c=Seafood          → List<Meal> (id, nama, gambar, area)
      │  tampil: FutureBuilder + ListView.builder
      ▼
   tap salah satu item
      │
      │  Navigator.push  ... mengirim idMeal saja (bukan seluruh objek)
      ▼
HalamanDetail
      │
      │  GET lookup.php?i={idMeal}         → Meal lengkap (instruksi, kategori)
      │  tampil: FutureBuilder + SingleChildScrollView
      ▼
   pengguna membaca resep, lalu kembali (Navigator.pop)
```

> **Poin desain penting:** halaman detail hanya menerima **`idMeal`**, bukan seluruh objek `Meal`. Cara ini lebih efisien dan memastikan data yang ditampilkan selalu versi terbaru dari server. Ini juga pertanyaan ujian yang bagus.

---

## C. Persiapan

1. Flutter SDK terinstal dan `flutter doctor` tanpa error kritis.
2. Perangkat/emulator **terhubung ke internet** (uji dengan membuka browser di perangkat).
3. Buat project baru:

```bash
flutter create pnl_api
cd pnl_api
flutter pub add http
```

4. Verifikasi endpoint di browser terlebih dahulu — buka:
   `https://www.themealdb.com/api/json/v1/1/filter.php?c=Seafood`
   Jika JSON tampil di browser, berarti API dan jaringan baik. **Selalu lakukan langkah ini sebelum menulis kode**, agar bisa membedakan masalah jaringan dengan masalah kode.
5. Karena kode hari ini cukup panjang, seluruhnya ditulis di `lib/main.dart`. Pemisahan ke `lib/models/`, `lib/services/`, dan `lib/pages/` menjadi nilai tambah.

---

## D. Praktikum Terpandu

### Latihan 1 — Permintaan HTTP Pertama dan Membaca JSON Mentah (20 menit)

Tujuan latihan ini **bukan** membuat tampilan cantik, melainkan membuktikan bahwa data benar-benar datang dari internet. Tampilkan dulu JSON mentahnya, baru dirapikan di latihan berikutnya.

Ganti seluruh isi `lib/main.dart` dengan kode berikut:

```dart
import 'dart:convert';                        // untuk jsonDecode
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;      // package yang baru ditambahkan

/// Endpoint daftar resep kategori Seafood.
const String urlDaftar =
    'https://www.themealdb.com/api/json/v1/1/filter.php?c=Seafood';

void main() => runApp(const MyApp());

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: HalamanUjiApi(),
    );
  }
}

class HalamanUjiApi extends StatefulWidget {
  const HalamanUjiApi({super.key});

  @override
  State<HalamanUjiApi> createState() => _HalamanUjiApiState();
}

class _HalamanUjiApiState extends State<HalamanUjiApi> {
  bool sedangMemuat = true;
  String pesan = '';

  @override
  void initState() {
    super.initState();
    ambilData();   // dijalankan sekali saat halaman pertama kali dibuat
  }

  Future<void> ambilData() async {
    setState(() {
      sedangMemuat = true;
      pesan = '';
    });

    String hasil;
    try {
      final response = await http.get(Uri.parse(urlDaftar));

      if (response.statusCode == 200) {
        final data = jsonDecode(response.body) as Map<String, dynamic>;

        // 'meals' bisa bernilai null jika kategori tidak punya data.
        final daftar = (data['meals'] as List<dynamic>?) ?? const [];
        final contoh = daftar.isEmpty ? '(tidak ada data)' : '${daftar.first}';

        hasil = 'Status code : ${response.statusCode}\n'
            'Panjang body: ${response.body.length} karakter\n'
            'Jumlah item : ${daftar.length}\n'
            'Tipe data   : ${daftar.runtimeType}\n\n'
            'Isi item pertama (JSON mentah):\n\n$contoh';
      } else {
        hasil = 'Server membalas dengan status ${response.statusCode}.';
      }
    } catch (e) {
      hasil = 'Gagal terhubung ke server.\n\n$e';
    }

    if (!mounted) return;   // halaman mungkin sudah ditutup saat data tiba
    setState(() {
      pesan = hasil;
      sedangMemuat = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Latihan 1 - Uji API'),
        backgroundColor: Colors.teal,
        foregroundColor: Colors.white,
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: sedangMemuat
            ? const Center(child: CircularProgressIndicator())
            : Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Expanded(
                    child: SingleChildScrollView(
                      child: Text(
                        pesan,
                        style: const TextStyle(fontSize: 13, height: 1.5),
                      ),
                    ),
                  ),
                  const SizedBox(height: 16),
                  ElevatedButton.icon(
                    onPressed: ambilData,
                    icon: const Icon(Icons.refresh),
                    label: const Text('Coba Ambil Lagi'),
                  ),
                ],
              ),
      ),
    );
  }
}
```

> **Catatan asisten:** sebelum mahasiswa menulis kode apa pun, minta mereka memprediksi dulu isi layar: berapa jumlah item dan seperti apa bentuk JSON-nya. Prediksi yang meleset jauh adalah momen belajar yang paling efektif di latihan ini.

**Tugas mahasiswa:**
1. Jalankan aplikasi. Catat **status code**, **jumlah item**, dan tuliskan isi JSON item pertama pada laporan.
2. Ganti kategori pada URL dari `c=Seafood` menjadi `c=Dessert`, lalu tekan "Coba Ambil Lagi". Berapa jumlah itemnya sekarang?
3. Rusak URL-nya (ubah `filter.php` menjadi `filterr.php`) dan jalankan. Apakah masuk ke blok `catch` atau ke cabang `statusCode != 200`? Jelaskan mengapa.
4. Hapus kata `await` pada baris `http.get(...)`. Jalankan — error apa yang muncul? (Petunjuk: perhatikan tipe variabel `response`.)
5. Matikan internet perangkat (mode pesawat), lalu tekan "Coba Ambil Lagi". Salin pesan error yang muncul ke laporan.
6. Jelaskan dengan kalimat sendiri: mengapa hasil `await` tidak langsung dimasukkan ke dalam `setState` di dalam blok `try`?

> **Catatan asisten:** tugas nomor 3 sengaja menuntun mahasiswa memahami perbedaan **error jaringan** (masuk ke `catch`) dengan **error dari server** (status code bukan 200, tidak masuk `catch`). Banyak mahasiswa menganggap keduanya sama.

> **Catatan asisten:** jawaban tugas nomor 4 adalah `response` bertipe `Future<http.Response>`, sehingga `response.statusCode` tidak dikenali (error: "The getter 'statusCode' isn't defined for the type 'Future'"). Inilah cara paling efektif menjelaskan kegunaan `await`.

### Latihan 2 — Model Class + ListView.builder Berisi Data dari API (30 menit)

Sekarang JSON mentah diubah menjadi objek dan ditampilkan sebagai daftar, seperti katalog pada Pertemuan 3.

```dart
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

const String urlDaftar =
    'https://www.themealdb.com/api/json/v1/1/filter.php?c=Seafood';

// ---------------- MODEL ----------------
class Meal {
  final String id;
  final String nama;
  final String gambar;
  final String area;

  const Meal({
    required this.id,
    required this.nama,
    required this.gambar,
    required this.area,
  });

  factory Meal.fromJson(Map<String, dynamic> json) {
    return Meal(
      id: json['idMeal'] as String? ?? '',
      nama: json['strMeal'] as String? ?? 'Tanpa Nama',
      gambar: json['strMealThumb'] as String? ?? '',
      area: json['strArea'] as String? ?? 'Internasional',
    );
  }
}

// ---------------- LAYANAN API ----------------
/// Mengambil data dari server dan mengubahnya menjadi List<Meal>.
/// Melempar Exception jika server tidak membalas status 200.
Future<List<Meal>> ambilDaftarMeal() async {
  final response = await http.get(Uri.parse(urlDaftar));

  if (response.statusCode != 200) {
    throw Exception('Server membalas status ${response.statusCode}');
  }

  final data = jsonDecode(response.body) as Map<String, dynamic>;
  final daftar = (data['meals'] as List<dynamic>?) ?? const [];

  return daftar
      .map((item) => Meal.fromJson(item as Map<String, dynamic>))
      .toList();
}

// ---------------- TAMPILAN ----------------
void main() => runApp(const MyApp());

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
  bool sedangMemuat = true;
  String pesanError = '';
  List<Meal> daftarMeal = [];

  @override
  void initState() {
    super.initState();
    muatData();
  }

  Future<void> muatData() async {
    setState(() {
      sedangMemuat = true;
      pesanError = '';
    });

    try {
      final hasil = await ambilDaftarMeal();
      if (!mounted) return;
      setState(() {
        daftarMeal = hasil;
        sedangMemuat = false;
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        pesanError = e.toString();
        sedangMemuat = false;
      });
    }
  }

  Widget _gambarMenu(String url) {
    return ClipRRect(
      borderRadius: BorderRadius.circular(8),
      child: Image.network(
        url,
        width: 64,
        height: 64,
        fit: BoxFit.cover,
        loadingBuilder: (context, child, progress) {
          if (progress == null) return child;
          return const SizedBox(
            width: 64,
            height: 64,
            child: Center(
              child: CircularProgressIndicator(strokeWidth: 2),
            ),
          );
        },
        errorBuilder: (context, error, stackTrace) {
          return Container(
            width: 64,
            height: 64,
            color: Colors.grey.shade200,
            child: const Icon(Icons.broken_image, color: Colors.grey),
          );
        },
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Katalog Resep'),
        backgroundColor: Colors.teal,
        foregroundColor: Colors.white,
      ),
      body: sedangMemuat
          ? const Center(child: CircularProgressIndicator())
          : pesanError.isNotEmpty
              ? Center(
                  child: Padding(
                    padding: const EdgeInsets.all(24),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      children: [
                        const Icon(Icons.cloud_off, size: 56, color: Colors.grey),
                        const SizedBox(height: 16),
                        Text(
                          'Gagal memuat data',
                          style: TextStyle(
                            fontSize: 16,
                            fontWeight: FontWeight.bold,
                            color: Colors.grey.shade800,
                          ),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          pesanError,
                          textAlign: TextAlign.center,
                          style: const TextStyle(fontSize: 12),
                        ),
                        const SizedBox(height: 20),
                        ElevatedButton.icon(
                          onPressed: muatData,
                          icon: const Icon(Icons.refresh),
                          label: const Text('Coba Lagi'),
                        ),
                      ],
                    ),
                  ),
                )
              : ListView.builder(
                  padding: const EdgeInsets.all(12),
                  itemCount: daftarMeal.length,
                  itemBuilder: (context, index) {
                    final meal = daftarMeal[index];

                    return Card(
                      margin: const EdgeInsets.only(bottom: 12),
                      elevation: 3,
                      shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(16),
                      ),
                      child: ListTile(
                        contentPadding: const EdgeInsets.symmetric(
                          horizontal: 12,
                          vertical: 8,
                        ),
                        leading: _gambarMenu(meal.gambar),
                        title: Text(
                          meal.nama,
                          maxLines: 2,
                          overflow: TextOverflow.ellipsis,
                          style: const TextStyle(fontWeight: FontWeight.bold),
                        ),
                        subtitle: Text(meal.area),
                        trailing: const Icon(Icons.chevron_right),
                        onTap: () {
                          ScaffoldMessenger.of(context).showSnackBar(
                            SnackBar(
                              content: Text('idMeal: ${meal.id}'),
                              duration: const Duration(seconds: 1),
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
```

**Tugas mahasiswa:**
1. Ganti kategori menjadi `c=Chicken`. Catat jumlah item yang tampil.
2. Tambahkan field `kategori` pada class `Meal` dengan key JSON `strCategory`. **Apakah isinya terisi?** Jelaskan mengapa demikian, lalu hubungkan jawabannya dengan rencana Latihan 4.
3. Tampilkan jumlah item pada judul `AppBar` (contoh: `Katalog Resep (85)`).
4. Hapus `errorBuilder` dari fungsi `_gambarMenu`, lalu ubah `gambar` menjadi URL yang salah (`'https://contoh-salah.com/x.jpg'`). Amati apa yang muncul di layar, lalu **kembalikan** `errorBuilder`.
5. Jelaskan fungsi `factory Meal.fromJson(...)` dengan bahasa sendiri, dan apa jadinya jika `?? 'Tanpa Nama'` dihapus.
6. Tambahkan `RefreshIndicator` yang membungkus `ListView` dan memanggil `muatData()`. (Petunjuk: `onRefresh: muatData`.)

> **Catatan asisten:** jawaban tugas nomor 2 adalah **tidak terisi**, karena endpoint `filter.php` tidak menyediakan `strCategory` — hanya `lookup.php` yang menyediakannya. Gunakan temuan ini sebagai jembatan alami ke Latihan 4 (halaman detail harus meminta data sendiri ke server).

> **Catatan asisten:** untuk tugas nomor 6, `RefreshIndicator` hanya bekerja di dalam widget yang bisa digulir dan **tidak** akan berfungsi bila kondisinya masih menampilkan `Center` (pesan error). Arahkan mahasiswa agar membungkus `ListView.builder` saja.

### Latihan 3 — Merapikan dengan FutureBuilder (20 menit)

Bagian model, layanan API, dan tampilan daftar **tidak berubah**. Yang diganti hanya class `_HalamanKatalogState` — perhatikan bagaimana loading, error, dan data ditangani oleh satu widget.

```dart
class _HalamanKatalogState extends State<HalamanKatalog> {
  // Future disimpan di variabel, BUKAN dibuat langsung di dalam build().
  late Future<List<Meal>> futureMeal;

  @override
  void initState() {
    super.initState();
    futureMeal = ambilDaftarMeal();   // permintaan dikirim sekali saja
  }

  void muatUlang() {
    setState(() {
      futureMeal = ambilDaftarMeal();  // permintaan baru → FutureBuilder membangun ulang
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Katalog Resep (FutureBuilder)'),
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
      body: FutureBuilder<List<Meal>>(
        future: futureMeal,
        builder: (context, snapshot) {
          // ---- Keadaan 1: masih menunggu ----
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          // ---- Keadaan 2: gagal ----
          if (snapshot.hasError) {
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
                    Text(
                      '${snapshot.error}',
                      textAlign: TextAlign.center,
                      style: const TextStyle(fontSize: 12),
                    ),
                    const SizedBox(height: 20),
                    ElevatedButton.icon(
                      onPressed: muatUlang,
                      icon: const Icon(Icons.refresh),
                      label: const Text('Coba Lagi'),
                    ),
                  ],
                ),
              ),
            );
          }

          // ---- Keadaan 3: berhasil ----
          final daftar = snapshot.data ?? [];
          if (daftar.isEmpty) {
            return const Center(child: Text('Tidak ada data untuk kategori ini.'));
          }

          return RefreshIndicator(
            onRefresh: () async => muatUlang(),
            child: ListView.builder(
              padding: const EdgeInsets.all(12),
              itemCount: daftar.length,
              itemBuilder: (context, index) {
                final meal = daftar[index];

                return Card(
                  margin: const EdgeInsets.only(bottom: 12),
                  elevation: 3,
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(16),
                  ),
                  child: ListTile(
                    contentPadding: const EdgeInsets.symmetric(
                      horizontal: 12,
                      vertical: 8,
                    ),
                    leading: ClipRRect(
                      borderRadius: BorderRadius.circular(8),
                      child: Image.network(
                        meal.gambar,
                        width: 64,
                        height: 64,
                        fit: BoxFit.cover,
                        errorBuilder: (context, error, stackTrace) => Container(
                          width: 64,
                          height: 64,
                          color: Colors.grey.shade200,
                          child: const Icon(Icons.broken_image, color: Colors.grey),
                        ),
                      ),
                    ),
                    title: Text(
                      meal.nama,
                      maxLines: 2,
                      overflow: TextOverflow.ellipsis,
                      style: const TextStyle(fontWeight: FontWeight.bold),
                    ),
                    subtitle: Text(meal.area),
                    trailing: const Icon(Icons.chevron_right),
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
```

**Perbandingan hasil akhir Latihan 2 dan Latihan 3:**

| Hal | Latihan 2 (`setState`) | Latihan 3 (`FutureBuilder`) |
|---|---|---|
| Variabel keadaan | `sedangMemuat`, `pesanError`, `daftarMeal` (3 buah) | `futureMeal` (1 buah) |
| Penanganan error | Blok `try`/`catch` + pengondisian di `build` | Otomatis lewat `snapshot.hasError` |
| Sumber kebenaran | Tiga variabel yang harus konsisten | Satu `Future` |

**Tugas mahasiswa:**
1. Hitung jumlah baris class `_HalamanKatalogState` pada Latihan 2 dan Latihan 3. Catat selisihnya di laporan.
2. Tambahkan `print(snapshot.connectionState);` pada baris pertama di dalam `builder`, lalu jalankan. Tuliskan urutan nilai yang tercetak di console dan jelaskan artinya.
3. Ubah `future: futureMeal` menjadi `future: ambilDaftarMeal()` (langsung memanggil fungsi). Jalankan dan amati perilaku aplikasi. Mengapa hal ini berbahaya? (Petunjuk: kapan `build()` dipanggil?)
4. Ubah `snapshot.data ?? []` menjadi `snapshot.data!`. Kapan aplikasi akan berhenti dengan error? Jelaskan.
5. Untuk Tugas Mandiri nanti, mana yang Anda pilih: pendekatan `setState` atau `FutureBuilder`? Tuliskan alasannya dalam 3–4 baris.

> **Catatan asisten:** tugas nomor 3 adalah konsep paling penting di latihan ini. Jika `Future` dibuat di dalam `build()`, setiap perubahan tampilan (termasuk saat animasi gulir) akan mengirim permintaan HTTP baru **tanpa henti**. Cara mendeteksinya: perhatikan console/log server yang terus bertambah, atau tambahkan `print` sebelum `http.get`.

> **Catatan asisten:** urutan `connectionState` yang benar pada tugas nomor 2 adalah `waiting` → `done` (kadang `none` muncul lebih dulu). Jika mahasiswa melaporkan `waiting` tercetak berulang-ulang, arahkan untuk memeriksa tugas nomor 3.

### Latihan 4 — Proyek Mini: Katalog + Detail dari Dua Endpoint (35 menit)

Ini latihan inti hari ini. Bedanya dengan Pertemuan 3: halaman detail **tidak** menerima seluruh objek, melainkan **hanya `idMeal`**, lalu mengambil sendiri data lengkapnya dari server. Inilah pola yang dipakai aplikasi nyata.

Mahasiswa mengerjakan mandiri, dosen/asisten berkeliling membimbing.

**Ketentuan wajib:**
1. Halaman **Katalog** menampilkan daftar dari `filter.php` menggunakan `FutureBuilder` + `ListView.builder`.
2. Menekan sebuah item membuka halaman **Detail** dengan mengirim **`idMeal` dan nama** saja.
3. Halaman **Detail** memanggil `lookup.php?i={idMeal}` dan memakai `FutureBuilder` sendiri.
4. Halaman Detail menampilkan: gambar besar, nama, kategori, area, dan cara membuat (instruksi) yang dapat digulir.
5. Ketiga keadaan (menunggu, gagal, berhasil) ditangani di **kedua** halaman, lengkap dengan tombol **"Coba Lagi"** pada keadaan gagal.
6. Gambar memakai `Image.network` **dengan** `errorBuilder`.
7. Model `Meal` memiliki `factory fromJson` dan dipakai di kedua endpoint.

**Struktur pohon widget yang disarankan (hint):**

```
HalamanKatalog (StatefulWidget)
├── Scaffold + AppBar (aksi: refresh)
└── FutureBuilder<List<Meal>>
    ├── waiting  → CircularProgressIndicator
    ├── error    → pesan + tombol "Coba Lagi"
    └── data     → ListView.builder
                    └── Card → ListTile
                         ├── leading : Image.network (errorBuilder)
                         ├── title   : nama
                         ├── subtitle: area
                         └── onTap   → Navigator.push(HalamanDetail(idMeal, nama))

HalamanDetail (StatefulWidget) — menerima idMeal
├── Scaffold + AppBar (judul = nama yang dikirim)
└── FutureBuilder<Meal>
    ├── waiting  → CircularProgressIndicator
    ├── error    → pesan + tombol "Coba Lagi"
    └── data     → SingleChildScrollView → Column
                    ├── Image.network (tinggi 220, fit: cover)
                    ├── Text(nama)
                    ├── Wrap → chip kategori + chip area
                    ├── Divider
                    ├── Text("Cara Membuat")
                    ├── Text(instruksi)
                    └── ElevatedButton "Kembali ke Katalog"
```

**Kode acuan:**

```dart
import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

// ---------------- ENDPOINT ----------------
const String urlDaftar =
    'https://www.themealdb.com/api/json/v1/1/filter.php?c=Seafood';

String urlDetail(String idMeal) =>
    'https://www.themealdb.com/api/json/v1/1/lookup.php?i=$idMeal';

// ---------------- MODEL ----------------
/// Model yang sama dipakai untuk respons filter.php maupun lookup.php.
/// Field yang tidak tersedia di salah satu endpoint akan berisi nilai default.
class Meal {
  final String id;
  final String nama;
  final String gambar;
  final String area;
  final String kategori;
  final String instruksi;

  const Meal({
    required this.id,
    required this.nama,
    required this.gambar,
    required this.area,
    required this.kategori,
    required this.instruksi,
  });

  factory Meal.fromJson(Map<String, dynamic> json) {
    return Meal(
      id: json['idMeal'] as String? ?? '',
      nama: json['strMeal'] as String? ?? 'Tanpa Nama',
      gambar: json['strMealThumb'] as String? ?? '',
      area: json['strArea'] as String? ?? 'Internasional',
      kategori: json['strCategory'] as String? ?? '-',
      // Instruksi dari API memakai \r\n; diseragamkan menjadi \n agar rapi.
      instruksi: (json['strInstructions'] as String? ?? 'Belum ada instruksi.')
          .replaceAll('\r\n', '\n'),
    );
  }
}

// ---------------- LAYANAN API ----------------
Future<List<Meal>> ambilDaftarMeal() async {
  final response = await http.get(Uri.parse(urlDaftar));

  if (response.statusCode != 200) {
    throw Exception('Server membalas status ${response.statusCode}');
  }

  final data = jsonDecode(response.body) as Map<String, dynamic>;
  final daftar = (data['meals'] as List<dynamic>?) ?? const [];

  return daftar
      .map((item) => Meal.fromJson(item as Map<String, dynamic>))
      .toList();
}

Future<Meal> ambilDetailMeal(String idMeal) async {
  final response = await http.get(Uri.parse(urlDetail(idMeal)));

  if (response.statusCode != 200) {
    throw Exception('Server membalas status ${response.statusCode}');
  }

  final data = jsonDecode(response.body) as Map<String, dynamic>;

  // Untuk id yang tidak dikenal, server membalas {"meals": null}.
  // Tanpa pengecekan ini, akses .first akan membuat aplikasi berhenti.
  final daftar = data['meals'] as List<dynamic>?;
  if (daftar == null || daftar.isEmpty) {
    throw Exception('Detail resep tidak ditemukan');
  }

  return Meal.fromJson(daftar.first as Map<String, dynamic>);
}

// ---------------- HALAMAN 1: KATALOG ----------------
void main() => runApp(const MyApp());

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
  late Future<List<Meal>> futureMeal;

  @override
  void initState() {
    super.initState();
    futureMeal = ambilDaftarMeal();
  }

  void muatUlang() {
    setState(() {
      futureMeal = ambilDaftarMeal();
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Katalog Resep'),
        backgroundColor: Colors.teal,
        foregroundColor: Colors.white,
        actions: [
          IconButton(
            onPressed: muatUlang,
            icon: const Icon(Icons.refresh),
          ),
        ],
      ),
      body: FutureBuilder<List<Meal>>(
        future: futureMeal,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError) {
            return _tampilanError(snapshot.error.toString(), muatUlang);
          }

          final daftar = snapshot.data ?? [];
          if (daftar.isEmpty) {
            return const Center(child: Text('Tidak ada resep untuk kategori ini.'));
          }

          return ListView.builder(
            padding: const EdgeInsets.all(12),
            itemCount: daftar.length,
            itemBuilder: (context, index) {
              final meal = daftar[index];

              return Card(
                margin: const EdgeInsets.only(bottom: 12),
                elevation: 3,
                shape: RoundedRectangleBorder(
                  borderRadius: BorderRadius.circular(16),
                ),
                child: ListTile(
                  contentPadding: const EdgeInsets.symmetric(
                    horizontal: 12,
                    vertical: 8,
                  ),
                  leading: ClipRRect(
                    borderRadius: BorderRadius.circular(8),
                    child: Image.network(
                      meal.gambar,
                      width: 64,
                      height: 64,
                      fit: BoxFit.cover,
                      errorBuilder: (context, error, stackTrace) => Container(
                        width: 64,
                        height: 64,
                        color: Colors.grey.shade200,
                        child: const Icon(Icons.broken_image, color: Colors.grey),
                      ),
                    ),
                  ),
                  title: Text(
                    meal.nama,
                    maxLines: 2,
                    overflow: TextOverflow.ellipsis,
                    style: const TextStyle(fontWeight: FontWeight.bold),
                  ),
                  subtitle: Text(meal.area),
                  trailing: const Icon(Icons.chevron_right),
                  onTap: () {
                    // Hanya mengirim ID, bukan seluruh objek Meal.
                    Navigator.push(
                      context,
                      MaterialPageRoute(
                        builder: (context) => HalamanDetail(
                          idMeal: meal.id,
                          nama: meal.nama,
                        ),
                      ),
                    );
                  },
                ),
              );
            },
          );
        },
      ),
    );
  }
}

/// Widget bantuan: pesan error + tombol coba lagi. Dipakai di kedua halaman.
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
          Text(
            pesan,
            textAlign: TextAlign.center,
            style: const TextStyle(fontSize: 12),
          ),
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

// ---------------- HALAMAN 2: DETAIL ----------------
class HalamanDetail extends StatefulWidget {
  const HalamanDetail({super.key, required this.idMeal, required this.nama});

  final String idMeal;   // data satu-satunya yang dikirim dari katalog
  final String nama;     // dipakai untuk judul AppBar sebelum data tiba

  @override
  State<HalamanDetail> createState() => _HalamanDetailState();
}

class _HalamanDetailState extends State<HalamanDetail> {
  late Future<Meal> futureDetail;

  @override
  void initState() {
    super.initState();
    // Di dalam State, properti widget diakses lewat kata kunci 'widget'.
    futureDetail = ambilDetailMeal(widget.idMeal);
  }

  void muatUlang() {
    setState(() {
      futureDetail = ambilDetailMeal(widget.idMeal);
    });
  }

  Widget _chip(IconData ikon, String teks) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 6),
      decoration: BoxDecoration(
        color: Colors.teal.shade50,
        borderRadius: BorderRadius.circular(20),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(ikon, size: 16, color: Colors.teal),
          const SizedBox(width: 6),
          Text(
            teks,
            style: const TextStyle(
              fontSize: 12,
              color: Colors.teal,
              fontWeight: FontWeight.w500,
            ),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.nama, overflow: TextOverflow.ellipsis),
        backgroundColor: Colors.teal,
        foregroundColor: Colors.white,
      ),
      body: FutureBuilder<Meal>(
        future: futureDetail,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError) {
            return _tampilanError(snapshot.error.toString(), muatUlang);
          }

          final meal = snapshot.data!;

          return SingleChildScrollView(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Image.network(
                  meal.gambar,
                  height: 220,
                  fit: BoxFit.cover,
                  errorBuilder: (context, error, stackTrace) => Container(
                    height: 220,
                    color: Colors.grey.shade200,
                    child: const Icon(Icons.broken_image, size: 56, color: Colors.grey),
                  ),
                ),
                Padding(
                  padding: const EdgeInsets.all(20),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        meal.nama,
                        style: const TextStyle(
                          fontSize: 22,
                          fontWeight: FontWeight.bold,
                        ),
                      ),
                      const SizedBox(height: 12),
                      Wrap(
                        spacing: 8,
                        runSpacing: 8,
                        children: [
                          _chip(Icons.restaurant_menu, meal.kategori),
                          _chip(Icons.public, meal.area),
                          _chip(Icons.tag, meal.id),
                        ],
                      ),
                      const SizedBox(height: 20),
                      const Divider(),
                      const SizedBox(height: 12),
                      const Text(
                        'Cara Membuat',
                        style: TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                      ),
                      const SizedBox(height: 8),
                      Text(
                        meal.instruksi,
                        style: const TextStyle(fontSize: 14, height: 1.6),
                      ),
                      const SizedBox(height: 28),
                      ElevatedButton.icon(
                        onPressed: () => Navigator.pop(context),
                        icon: const Icon(Icons.arrow_back),
                        label: const Text('Kembali ke Katalog'),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }
}
```

**Tugas mahasiswa:**
1. Jalankan aplikasi, tekan beberapa item, dan pastikan halaman detail menampilkan resep yang **sesuai** dengan item yang ditekan.
2. Hapus pengecekan `if (daftar == null || daftar.isEmpty)` di `ambilDetailMeal`, lalu ubah `urlDetail` menjadi `i=9999999`. Jalankan. Error apa yang muncul? Jelaskan mengapa pengecekan itu penting, lalu **kembalikan** kodenya.
3. **Pertanyaan analisis:** bandingkan cara Latihan 4 (mengirim `idMeal`) dengan cara Pertemuan 3 (mengirim seluruh objek `Meal`). Sebutkan satu kelebihan dan satu kekurangan masing-masing.
4. Tambahkan tombol **"Simpan ke Favorit"** di halaman detail yang menampilkan `SnackBar`. (Menyimpan datanya secara permanen belum diperlukan pada pertemuan ini.)
5. Tampilkan `meal.kategori` pada baris katalog. Apakah isinya muncul? Jelaskan hubungannya dengan jawaban Latihan 2 tugas nomor 2.
6. (Nilai tambah) Bungkus gambar di katalog dan di halaman detail dengan `Hero(tag: meal.id, child: ...)`, lalu amati animasinya saat berpindah halaman.
7. (Nilai tambah) Pisahkan kode menjadi `lib/models/meal.dart`, `lib/services/meal_service.dart`, `lib/pages/halaman_katalog.dart`, dan `lib/pages/halaman_detail.dart`.

> **Catatan asisten:** tugas nomor 5 selalu memicu diskusi bagus. Jawabannya: `kategori` **tidak muncul** karena endpoint `filter.php` tidak menyertakan `strCategory`, sehingga `fromJson` memakai nilai default `'-'`. Pilihan desainnya ada dua — biarkan default, atau ambil kategori dari endpoint detail. Sampaikan bahwa keduanya sah, tergantung kebutuhan.

---

## E. Tugas Mandiri (Dikumpulkan)

Bangun aplikasi **"Katalog Online"** dua halaman yang seluruh datanya diambil dari internet. Tema bebas (resep, produk, buku, wisata, dan sebagainya), tetapi sumber data harus berasal dari API publik yang dapat diakses tanpa API key.

**Sumber data yang boleh dipakai** (keduanya sudah diuji dan berjalan):

| API | Endpoint | Catatan |
|---|---|---|
| TheMealDB **(disarankan)** | `https://www.themealdb.com/api/json/v1/1/filter.php?c=Seafood` | Ada gambar, cocok untuk katalog |
| | `https://www.themealdb.com/api/json/v1/1/lookup.php?i=52772` | Detail satu item |
| JSONPlaceholder | `https://jsonplaceholder.typicode.com/posts` | Teks saja, tanpa gambar |
| | `https://jsonplaceholder.typicode.com/posts/1` | Detail satu item (bentuk respons **objek**, bukan array — perhatikan perbedaannya) |

Boleh memakai API lain asalkan **mahasiswa menguji endpoint di browser terlebih dahulu** dan mencantumkan hasilnya di laporan.

**Ketentuan wajib:**

1. **Dua endpoint berbeda** digunakan: satu untuk daftar (halaman katalog), satu untuk detail (halaman detail).
2. Halaman **Katalog**: `FutureBuilder` + `ListView.builder`, memuat minimal 10 item.
3. Halaman **Detail**: dibuka dengan mengirim **ID** saja, lalu mengambil datanya sendiri dari endpoint kedua.
4. **Ketiga keadaan ditangani di kedua halaman**: menunggu (indikator loading), gagal (pesan + tombol "Coba Lagi"), berhasil (data tampil).
5. Ada class model dengan `factory fromJson`, dan **semua** field yang mungkin bernilai `null` diberi nilai default.
6. Gambar dari internet memakai `Image.network` **beserta** `errorBuilder` (lewatkan bagian ini bila API yang dipilih tidak menyediakan gambar).
7. Halaman katalog dilengkapi `RefreshIndicator` (tarik untuk memuat ulang).
8. **Perpindahan kategori:** sediakan minimal 3 pilihan kategori (mis. `Seafood`, `Chicken`, `Dessert`) yang dapat dipilih pengguna — `ChoiceChip`, `DropdownButton`, atau `TabBar` — dan setiap pilihan memuat ulang data dari server dengan parameter berbeda.
9. Tampilan tetap rapi sesuai materi Pertemuan 2 dan 3: `Card`, `borderRadius`, `boxShadow`, warna tema konsisten.

**Nilai tambah (opsional):**
- Kolom pencarian yang mengirim kata kunci ke endpoint `search.php?s=...`.
- `Hero` animation pada gambar antara katalog dan detail.
- Memisahkan kode ke `lib/models/`, `lib/services/`, dan `lib/pages/`.
- Tombol "Simpan ke Favorit" dengan `SnackBar`.

**Pengumpulan:** seluruh file `.dart` (atau arsip project) + **screenshot 4 keadaan**: (a) loading, (b) berhasil, (c) gagal/error, (d) halaman detail + laporan singkat (PDF) yang berisi:

- Daftar endpoint yang dipakai beserta contoh potongan JSON-nya.
- Jawaban pertanyaan pada Latihan 1–4.
- Penjelasan alur data dari server sampai tampil di layar.
- Penjelasan singkat mengapa pada tugas ini halaman detail cukup menerima ID.

> **Cara membuktikan keadaan (c) gagal:** aktifkan mode pesawat pada perangkat, lalu tekan "Coba Lagi". Jika tombol tersebut tidak muncul, berarti penanganan error belum dikerjakan.

---

## F. Rubrik Penilaian (Total 100)

| Aspek | Bobot |
|---|---|
| Latihan 1–3 selesai dan jawaban pertanyaan benar | 25 |
| Latihan 4 (Katalog + Detail dari dua endpoint) sesuai semua ketentuan wajib | 30 |
| Tugas Mandiri: kelengkapan (2 endpoint, 3 keadaan, model + fromJson, kategori) | 25 |
| Tugas Mandiri: kerapian kode, struktur folder & kreativitas tampilan | 20 |

**Catatan penilaian:**
- Tugas Mandiri yang hanya memakai **satu** endpoint (halaman detail tidak memanggil server) dianggap belum memenuhi ketentuan nomor 1 dan 3.
- Nilai maksimal untuk aspek kelengkapan hanya diberikan bila **screenshot keadaan gagal** disertakan.
- Menyalin seluruh response API ke dalam variabel statis di dalam kode (bukan benar-benar memanggil server) tidak dinilai.

---

## G. Troubleshooting Umum

**Sebelum melapor error, lakukan empat langkah ini lebih dulu:**

1. Buka URL endpoint di **browser pada perangkat/emulator** yang sama. Jika JSON tampil, masalahnya ada di kode, bukan di jaringan.
2. Cetak `response.statusCode` dan `response.body` ke console.
3. Bandingkan ejaan key JSON (`strMeal`, `idMeal`, dan seterusnya) dengan yang tertulis di kode — huruf besar/kecil berpengaruh.
4. Tekan **hot restart** (`R`), bukan hot reload, setiap kali mengubah kode yang berkaitan dengan `initState` atau `pubspec.yaml`.

| Gejala | Penyebab umum | Solusi |
|---|---|---|
| `SocketException: Failed host lookup: 'www.themealdb.com'` | Perangkat tidak memiliki koneksi internet / DNS gagal | Periksa koneksi; emulator memakai jaringan komputer host |
| `ClientException: Connection closed before full header was received` | Koneksi terputus di tengah permintaan | Ulangi permintaan, periksa jaringan atau proxy kampus |
| `FormatException: Unexpected character (at character 1)` | `jsonDecode` dijalankan pada body yang bukan JSON (mis. halaman HTML error) | Periksa `statusCode` sebelum `jsonDecode`, cetak `response.body` |
| `type 'Null' is not a subtype of type 'String'` | Sebuah field JSON bernilai `null` atau key salah eja | Gunakan `as String?` + `?? 'nilai default'` |
| `type 'List<dynamic>' is not a subtype of type 'Map<String, dynamic>'` | Bentuk respons berupa array, bukan objek | Lihat karakter pertama respons: `[` → `List`, `{` → `Map` |
| `RangeError (index): Invalid value: Valid value range is empty: 0` | Memanggil `.first` pada list kosong (mis. ID tidak dikenal) | Periksa `daftar == null \|\| daftar.isEmpty` sebelum mengambil `.first` |
| `Exception: Server membalas status 404` | Endpoint salah tulis | Uji URL di browser, perbaiki penulisan |
| `MissingPluginException` atau package `http` tidak dikenali | `flutter pub add http` belum dijalankan / build lama | Jalankan `flutter pub get`, lalu jalankan ulang aplikasi |
| Permintaan HTTP terkirim terus-menerus tanpa henti | `Future` dibuat di dalam `build()` | Simpan `Future` di variabel dan tetapkan di `initState` (lihat Latihan 3 tugas nomor 3) |
| `setState() called after dispose()` | Respons tiba setelah halaman ditutup | Tambahkan `if (!mounted) return;` sebelum `setState` |
| Data tidak ikut berubah setelah hot reload | `initState` tidak dijalankan ulang | Tekan hot **restart** (`R`) |
| Gambar tampil sebagai kotak abu-abu atau ikon rusak | URL gambar salah / koneksi terbatas | Tambahkan `errorBuilder`, uji URL gambar di browser |
| `CLEARTEXT communication ... not permitted` | Memanggil alamat `http://` di Android 9+ | Gunakan `https://`; untuk server lokal, tambahkan `android:usesCleartextTraffic="true"` pada `AndroidManifest.xml` (khusus pengembangan) |
| Aplikasi lancar di debug, tetapi gagal saat dirilis (`SocketException`) | Izin INTERNET hanya ada di manifest debug/profile | Tambahkan `<uses-permission android:name="android.permission.INTERNET"/>` di `android/app/src/main/AndroidManifest.xml` |
| `XMLHttpRequest error` saat dijalankan di Chrome (Flutter Web) | Kebijakan CORS pada browser | Jalankan di emulator atau perangkat Android/iOS |
| Emulator tidak bisa mengakses `http://localhost:8080` | `localhost` pada emulator menunjuk ke emulator itu sendiri | Gunakan `10.0.2.2` (emulator Android) atau alamat IP LAN komputer (perangkat fisik) |
| `HandshakeException` | Sertifikat HTTPS bermasalah atau tanggal & jam perangkat salah | Perbaiki tanggal dan jam perangkat |

---

## H. Kaitan ke Pertemuan Berikutnya

Aplikasi hari ini sudah **membaca** data dari internet, tetapi masih memiliki dua keterbatasan: data tidak tersimpan di perangkat, dan pengguna belum bisa **mengirim** data ke server. Pada pertemuan berikutnya kita akan:

1. **Menyimpan data di perangkat** dengan `shared_preferences` — agar daftar favorit tetap ada setelah aplikasi ditutup (melanjutkan tombol "Simpan ke Favorit" pada Latihan 4).
2. **Mengirim data ke server** menggunakan `http.post` dengan body JSON, disertai penanganan `statusCode` 201 dan validasi `Form` + `TextFormField`.
3. **Berbagi data antar halaman** tanpa mengoper satu per satu, menggunakan `setState` tingkat lanjut atau pengelolaan state (Provider).

Tiga hal yang paling penting untuk diingat dari pertemuan ini: **selalu periksa `statusCode`**, **selalu tangani keadaan gagal**, dan **jangan pernah membuat `Future` di dalam `build()`**.

---

*Modul ini disusun untuk praktikum Pertemuan 4, sebagai kelanjutan langsung dari Modul Pertemuan 3. Seluruh endpoint API pada modul ini telah diuji dan berjalan pada saat modul disusun; bila di kemudian hari salah satu endpoint berubah, gunakan API publik lain dan sesuaikan kode `fromJson`-nya. Silakan sesuaikan waktu dan tingkat kesulitan dengan kondisi kelas.*
