# Laporan Praktikum Pemrograman Mobile

**Nama:** Ammar  
**NIM:** 2024573010129  
**Kelas:** TI3B  
**Matkul:** Praktikum Pemrograman Mobile (With Flutter)

---

## Latihan 3 — GridView: Halaman Kategori

### Langkah 1: Mempersiapkan Kode Latihan 3

Pada langkah ini, seluruh isi file `lib/main.dart` diganti dengan kode grid kategori yang menggunakan `GridView.builder`.

### Langkah 2: Mengubah Nilai crossAxisCount (Tugas 1)

Nilai `crossAxisCount` pada `SliverGridDelegateWithFixedCrossAxisCount` diubah menjadi 3, kemudian diubah lagi menjadi 1 untuk mengamati perbedaan tampilan:

```dart
// Pengujian crossAxisCount: 3
gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
  crossAxisCount: 3, // Diubah menjadi 3, lalu 1
  mainAxisSpacing: 12,
  crossAxisSpacing: 12,
  childAspectRatio: 1.1,
),
```

![Perbandingan crossAxisCount: 3 dan 1](./images/image1.png)

> **Analisis:**
>
> - Ketika `crossAxisCount` bernilai 3, layar dibagi menjadi 3 kolom secara horizontal. Ukuran setiap kartu menjadi lebih kecil dan sempit, sehingga jarak antar elemen ikut menyusut.
>
> - Ketika `crossAxisCount` bernilai 1, layar hanya menampilkan 1 kolom (menyerupai `ListView`). Ukuran kartu menjadi sangat lebar dan membentang dari sisi kiri hingga sisi kanan layar.

### Langkah 3: Menguji Perubahan childAspectRatio (Tugas 2)

Nilai `childAspectRatio` diubah menjadi 0.7 (lebih tinggi daripada lebar), kemudian diubah menjadi 1.6 (lebih lebar daripada tinggi) untuk mengamati dampaknya terhadap tampilan:

```dart
// Pengujian childAspectRatio: 1.6
gridDelegate: const SliverGridDelegateWithFixedCrossAxisCount(
  crossAxisCount: 2,
  mainAxisSpacing: 12,
  crossAxisSpacing: 12,
  childAspectRatio: 1.6, // Diubah menjadi 0.7, lalu 1.6
),
```

![Perbandingan childAspectRatio: 0.7 dan 1.6](./images/image2.png)

> **Analisis:**
>
> - Formula perhitungan dimensi item adalah: `Tinggi Item = Lebar Item / childAspectRatio`.
>
> - Pada nilai 0.7, kartu menjadi sangat memanjang secara vertikal (tinggi).
>
> - Pada nilai 1.6, kartu menjadi sangat pipih atau gepeng secara horizontal. Isi kartu (ikon dan teks) mulai terpotong atau mengalami *overflow* ketika nilai `childAspectRatio` terlalu besar (misalnya >= 1.6), karena tinggi item menjadi terlalu sempit untuk menampung `Icon`, `SizedBox`, dan `Text` yang ada di dalamnya.

### Langkah 4: Mengganti GridView.builder dengan GridView.count (Tugas 3)

Implementasi pada `body` Scaffold diubah dari `GridView.builder` menjadi `GridView.count`:

```dart
body: GridView.count(
  padding: const EdgeInsets.all(16),
  crossAxisCount: 2,
  mainAxisSpacing: 12,
  crossAxisSpacing: 12,
  childAspectRatio: 1.1,
  children: daftarKategori.map((kategori) => kartuKategori(kategori)).toList(),
),
```

![GridView.count vs GridView.builder](./images/image3.png)

> **Analisis Perbedaan Penulisan:**
>
> `GridView.count` menerima daftar widget secara langsung (*explicit list*) pada properti `children`. Seluruh item dirender sekaligus saat widget dibangun, sehingga cocok digunakan untuk data statis dengan jumlah yang sedikit.
>
> `GridView.builder` menggunakan fungsi `itemBuilder` dan `itemCount`. Item dirender secara dinamis (*lazy rendering*), yaitu hanya saat item tersebut muncul di layar. Pendekatan ini jauh lebih hemat memori untuk data dalam jumlah banyak atau data yang bersifat dinamis.

### Langkah 5: Menambahkan Interaksi onTap dan SnackBar (Tugas 4)

`Container` pada widget `kartuKategori` dibungkus menggunakan `InkWell` (atau `GestureDetector`) agar dapat merespons sentuhan pengguna:

```dart
Widget kartuKategori(BuildContext context, Kategori kategori) {
  return InkWell(
    borderRadius: BorderRadius.circular(16),
    onTap: () {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Kategori dipilih: ${kategori.nama}'),
          duration: const Duration(seconds: 1),
        ),
      );
    },
    child: Container(
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
    ),
  );
}
```

![Tampilan Interaksi onTap dan SnackBar](./images/image4.png)

## Latihan 4 — Proyek Mini: Katalog dan Halaman Detail

### Langkah 1: Mempersiapkan Kode Dasar Katalog dan Navigasi Detail

Pada langkah awal ini, isi file `lib/main.dart` diganti dengan kode acuan katalog menu beserta halaman detail yang telah terhubung menggunakan `Navigator.push` dan `Navigator.pop`.

### Langkah 2: Mengubah HalamanDetail Menjadi StatefulWidget dan Menambahkan Level Pedas (Tugas 2)

Kelas `HalamanDetail` diubah dari `StatelessWidget` menjadi `StatefulWidget` agar dapat menyimpan status pilihan level pedas menggunakan `ChoiceChip`:

```dart
class HalamanDetail extends StatefulWidget {
  const HalamanDetail({super.key, required this.menu});
  final MenuItem menu;

  @override
  State<HalamanDetail> createState() => _HalamanDetailState();
}

class _HalamanDetailState extends State<HalamanDetail> {
  int _selectedLevel = 1; // Menyimpan state level pedas yang dipilih

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.menu.nama),
        backgroundColor: warnaTema,
        foregroundColor: Colors.white,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Ikon dan Nama Menu
            CircleAvatar(
              radius: 56,
              backgroundColor: warnaTema.shade50,
              child: Icon(widget.menu.ikon, size: 56, color: warnaTema),
            ),
            const SizedBox(height: 24),
            Text(
              widget.menu.nama,
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Text(
              formatRupiah(widget.menu.harga),
              textAlign: TextAlign.center,
              style: const TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: warnaTema,
              ),
            ),
            const SizedBox(height: 24),
            const Divider(),

            // Komponen ChoiceChip untuk Level Pedas
            const Text(
              'Pilihan Level Pedas:',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: List.generate(3, (index) {
                final level = index + 1;
                return ChoiceChip(
                  label: Text('Level $level'),
                  selected: _selectedLevel == level,
                  onSelected: (selected) {
                    if (selected) {
                      setState(() {
                        _selectedLevel = level;
                      });
                    }
                  },
                );
              }),
            ),
            const SizedBox(height: 16),
            const Divider(),
            const Text(
              'Deskripsi',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Text(widget.menu.deskripsi, style: const TextStyle(height: 1.5)),
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
```

![HalamanDetail StatefulWidget dengan ChoiceChip Level Pedas](./images/image5.png)

> **Analisis Perubahan:**
>
> - Kelas diubah menjadi `StatefulWidget` dan logika tampilan dipindahkan ke dalam kelas `_HalamanDetailState`.
>
> - Ditambahkan variabel `int _selectedLevel` untuk mencatat level pedas yang sedang aktif.
>
> - Fungsi `setState()` dipanggil pada *callback* `onSelected` milik `ChoiceChip` agar Flutter melakukan *re-render* pada UI saat level pedas yang dipilih berubah.
>
> - Pengaksesan properti `menu` dari widget induk kini dilakukan melalui `widget.menu`.

### Langkah 3: Menambahkan Fitur Jumlah dan Perhitungan Total Harga (Tugas 3)

Variabel `int _jumlah` beserta tombol penambah dan pengurang ditambahkan di bawah pilihan level pedas:

```dart
int _jumlah = 1; // State jumlah porsi

// Di dalam widget build (Column):
Row(
  mainAxisAlignment: MainAxisAlignment.center,
  children: [
    IconButton(
      onPressed: _jumlah > 1 ? () => setState(() => _jumlah--) : null,
      icon: const Icon(Icons.remove_circle_outline),
    ),
    Text('$_jumlah', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
    IconButton(
      onPressed: () => setState(() => _jumlah++),
      icon: const Icon(Icons.add_circle_outline),
    ),
  ],
),
const SizedBox(height: 8),
Text(
  'Total: ${formatRupiah(widget.menu.harga * _jumlah)}',
  textAlign: TextAlign.center,
  style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: warnaTema),
),
```

![Fitur Jumlah Porsi dan Total Harga](./images/image6.png)

### Langkah 4: Menambahkan Animasi Transisi Hero Widget (Tugas 4)

`CircleAvatar` pada `HalamanKatalog` dan `HalamanDetail` dibungkus menggunakan widget `Hero` dengan tag unik berupa `menu.nama`:

Pada `HalamanKatalog`:

```dart
leading: Hero(
  tag: menu.nama,
  child: CircleAvatar(
    backgroundColor: warnaTema.shade50,
    child: Icon(menu.ikon, color: warnaTema),
  ),
),
```

Pada `HalamanDetail`:

```dart
Hero(
  tag: widget.menu.nama,
  child: CircleAvatar(
    radius: 56,
    backgroundColor: warnaTema.shade50,
    child: Icon(widget.menu.ikon, size: 56, color: warnaTema),
  ),
),
```

![Animasi Hero Widget saat Navigasi](./images/image7.png)

> **Analisis Efek Animasi:**
>
> Saat item pada daftar ditekan, ikon `CircleAvatar` yang berukuran kecil di halaman katalog tidak langsung berganti halaman secara kasar. Sebaliknya, ikon tersebut "terbang" dan membesar secara halus (*smooth transition*) menuju posisi `CircleAvatar` yang lebih besar di halaman detail. Transisi ini memberikan pengalaman navigasi yang lebih mulus dan intuitif bagi pengguna.

### Langkah 5: Refactoring Arsitektur File dan Folder Proyek (Tugas 5 — Nilai Tambah)

Struktur kode dipisahkan menjadi 3 file modular sesuai dengan standar arsitektur Flutter:

**`lib/models/menu_item.dart`**

```dart
import 'package:flutter/material.dart';

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
```

**`lib/pages/halaman_detail.dart`**

```dart
import 'package:flutter/material.dart';
import '../models/menu_item.dart';

class HalamanDetail extends StatefulWidget {
  const HalamanDetail({super.key, required this.menu});
  final MenuItem menu;

  @override
  State<HalamanDetail> createState() => _HalamanDetailState();
}

class _HalamanDetailState extends State<HalamanDetail> {
  int _selectedLevel = 1;
  int _jumlah = 1;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(widget.menu.nama),
        backgroundColor: warnaTema,
        foregroundColor: Colors.white,
      ),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(24),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Hero(
              tag: widget.menu.nama,
              child: CircleAvatar(
                radius: 56,
                backgroundColor: warnaTema.shade50,
                child: Icon(widget.menu.ikon, size: 56, color: warnaTema),
              ),
            ),
            const SizedBox(height: 24),
            Text(
              widget.menu.nama,
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Text(
              formatRupiah(widget.menu.harga),
              textAlign: TextAlign.center,
              style: const TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
                color: warnaTema,
              ),
            ),
            const SizedBox(height: 24),
            const Divider(),
            const Text(
              'Pilihan Level Pedas:',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceEvenly,
              children: List.generate(3, (index) {
                final level = index + 1;
                return ChoiceChip(
                  label: Text('Level $level'),
                  selected: _selectedLevel == level,
                  onSelected: (selected) {
                    if (selected) {
                      setState(() => _selectedLevel = level);
                    }
                  },
                );
              }),
            ),
            const SizedBox(height: 16),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                IconButton(
                  onPressed: _jumlah > 1 ? () => setState(() => _jumlah--) : null,
                  icon: const Icon(Icons.remove_circle_outline),
                ),
                Text('$_jumlah', style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                IconButton(
                  onPressed: () => setState(() => _jumlah++),
                  icon: const Icon(Icons.add_circle_outline),
                ),
              ],
            ),
            const SizedBox(height: 8),
            Text(
              'Total: ${formatRupiah(widget.menu.harga * _jumlah)}',
              textAlign: TextAlign.center,
              style: const TextStyle(fontSize: 20, fontWeight: FontWeight.bold, color: warnaTema),
            ),
            const SizedBox(height: 16),
            const Divider(),
            const Text(
              'Deskripsi',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Text(widget.menu.deskripsi, style: const TextStyle(height: 1.5)),
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
```

**`lib/pages/halaman_katalog.dart`**

```dart
import 'package:flutter/material.dart';
import '../models/menu_item.dart';
import 'halaman_detail.dart';

class HalamanKatalog extends StatelessWidget {
  const HalamanKatalog({super.key});

  final List<MenuItem> daftarMenu = const [
    MenuItem(
      nama: 'Mie Aceh',
      deskripsi: 'Mie tebal dengan kuah bumbu rempah khas Aceh, disajikan dengan acar bawang dan emping.',
      harga: 25000,
      ikon: Icons.ramen_dining,
    ),
    MenuItem(
      nama: 'Kopi Sanger',
      deskripsi: 'Kopi robusta Gayo diseduh dengan susu kental manis, disajikan panas dalam gelas kaca.',
      harga: 15000,
      ikon: Icons.local_cafe,
    ),
    MenuItem(
      nama: 'Ayam Tangkap',
      deskripsi: 'Ayam goreng khas Aceh yang ditaburi daun kari dan daun pandan goreng.',
      harga: 35000,
      ikon: Icons.lunch_dining,
    ),
    MenuItem(
      nama: 'Pisang Goreng Keju',
      deskripsi: 'Pisang goreng renyah dengan topping keju parut dan susu kental manis.',
      harga: 12000,
      ikon: Icons.bakery_dining,
    ),
    MenuItem(
      nama: 'Es Timun Serut',
      deskripsi: 'Minuman segar dari timun serut, jeruk nipis, dan sirup gula.',
      harga: 10000,
      ikon: Icons.local_drink,
    ),
    MenuItem(
      nama: 'Timphan',
      deskripsi: 'Kue tradisional Aceh dari tepung ketan berisi serikaya, dibungkus daun pisang.',
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
              contentPadding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
              leading: Hero(
                tag: menu.nama,
                child: CircleAvatar(
                  backgroundColor: warnaTema.shade50,
                  child: Icon(menu.ikon, color: warnaTema),
                ),
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
```

**`lib/main.dart`**

```dart
import 'package:flutter/material.dart';
import 'pages/halaman_katalog.dart';

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
```

![Struktur File Setelah Refactoring](./images/image8.png)
