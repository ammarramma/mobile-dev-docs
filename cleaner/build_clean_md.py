#!/usr/bin/env python3
"""
Script untuk:
1. Mengekstrak gambar Base64 dari Laprak_Mobile_6.md ke folder ./images/
2. Membuat Laprak_Mobile_6_Clean.md dengan format Markdown yang rapi
"""

import re
import os
import base64

# Path
BASE_DIR = '/home/ramma/Data/KULIAH_5/mobile'
INPUT_MD = os.path.join(BASE_DIR, 'Laprak_Mobile_6.md')
OUTPUT_MD = os.path.join(BASE_DIR, 'Laprak_Mobile_6_Clean.md')
IMAGES_DIR = os.path.join(BASE_DIR, 'images')

# Buat folder images
os.makedirs(IMAGES_DIR, exist_ok=True)

# Baca file MD asli
with open(INPUT_MD, 'r', encoding='utf-8') as f:
    content = f.read()

# Ekstrak gambar base64
pattern = r'!\[\]\(data:image/(\w+);base64,([A-Za-z0-9+/=\n]+)\)'
matches = list(re.finditer(pattern, content))
print(f'Ditemukan {len(matches)} gambar')

image_paths = []
for i, m in enumerate(matches):
    ext = m.group(1)
    data = m.group(2).replace('\n', '')
    img_filename = f'image{i+1}.{ext}'
    img_path = os.path.join(IMAGES_DIR, img_filename)
    with open(img_path, 'wb') as f:
        f.write(base64.b64decode(data))
    image_paths.append(f'./images/{img_filename}')
    print(f'  Gambar {i+1} disimpan: {img_path}')

# Ganti placeholder gambar
def replace_image(match, idx=[0]):
    result = f'![Gambar {idx[0]+1}]({image_paths[idx[0]]})'
    idx[0] += 1
    return result

clean_content = re.sub(pattern, replace_image, content)

# --- Bersihkan dan format Markdown ---
lines = clean_content.split('\n')
result_lines = []

def strip_line(line):
    """Hapus trailing whitespace berlebih tapi pertahankan indentasi kode"""
    return line.rstrip()

def is_code_line(line):
    """Deteksi baris yang terlihat seperti kode Dart (indentasi 2+ spasi atau baris kode)"""
    stripped = line.strip()
    return False  # Kita tentukan per blok

# State machine untuk parsing
in_code_block = False
prev_was_empty = False
code_buffer = []
pending_code_lang = None

# Label gambar yang akan dibuat
IMAGE_LABELS = [
    "crossAxisCount: 3 vs 1",
    "childAspectRatio: 0.7 vs 1.6",
    "GridView.count vs GridView.builder",
    "onTap SnackBar Interaksi",
    "HalamanDetail StatefulWidget + ChoiceChip",
    "Fitur Jumlah & Total Harga",
    "Animasi Transisi Hero Widget",
    "Arsitektur Refactoring File/Folder"
]
image_counter = [0]

def make_clean_md():
    # Bersihkan isi dengan regex lebih agresif
    text = clean_content

    # Perbaiki header identitas di awal
    # Hapus trailing spaces (\\  di akhir baris)
    text = re.sub(r'  \n', '\n', text)
    text = re.sub(r'  $', '', text, flags=re.MULTILINE)

    # Hapus baris yang hanya berisi spasi
    text = re.sub(r'^\s+$', '', text, flags=re.MULTILINE)

    # Normalisasi multiple blank lines -> max 1
    text = re.sub(r'\n{3,}', '\n\n', text)

    return text

# Buat Markdown bersih yang terformat
def build_formatted_md():
    """Buat konten MD yang terformat dengan baik"""
    
    raw = clean_content
    
    # Parse baris per baris
    lines = raw.split('\n')
    out = []
    
    # State
    in_code = False
    code_lines = []
    code_lang = 'dart'
    prev_blank = True
    img_idx = 0
    
    # Label keterangan gambar
    img_captions = [
        "Perbandingan crossAxisCount: 3 dan 1",
        "Perbandingan childAspectRatio: 0.7 dan 1.6",
        "GridView.count vs GridView.builder",
        "Tampilan Interaksi onTap dan SnackBar",
        "HalamanDetail StatefulWidget dengan ChoiceChip Level Pedas",
        "Fitur Jumlah Porsi dan Total Harga",
        "Animasi Hero Widget saat Navigasi",
        "Struktur File Setelah Refactoring"
    ]
    
    i = 0
    while i < len(lines):
        line = lines[i]
        stripped = line.strip()
        
        # Gambar placeholder
        if re.match(r'!\[Gambar \d+\]', stripped):
            caption = img_captions[img_idx] if img_idx < len(img_captions) else f"Gambar {img_idx+1}"
            # Ganti keterangan gambar
            new_line = re.sub(r'!\[Gambar \d+\]', f'![{caption}]', stripped)
            if out and out[-1] != '':
                out.append('')
            out.append(new_line)
            out.append('')
            img_idx += 1
            i += 1
            continue
        
        # Deteksi kata kunci bahasa kode ("Dart")
        if stripped == 'Dart' or stripped == 'dart':
            code_lang = 'dart'
            i += 1
            continue
        
        # Deteksi awal blok kode (baris yang diindentasi dengan code-like content)
        # Kita akan mengumpulkan baris kode yang dimulai dengan keyword Dart/kode
        # Cek apakah baris berikutnya merupakan kode (dimulai dengan // atau keywords Dart)
        dart_keywords = ['class ', 'void ', 'final ', 'const ', 'int ', 'String ', 'Widget ', 
                        'return ', 'import ', 'override', '@', 'body:', 'children:', 'Row(',
                        'Column(', 'Container(', 'Text(', 'Icon(', 'Card(', 'Scaffold(',
                        'Navigator', 'setState', 'build(', 'AppBar(', 'ListView', 'GridView',
                        'ElevatedButton', 'IconButton', 'Hero(', 'CircleAvatar(', 'Divider()',
                        'ChoiceChip(', 'InkWell(', 'GestureDetector(', 'SizedBox(', 'Padding(',
                        'BorderRadius', 'BoxDecoration', 'decoration:', 'style:', 'padding:',
                        'child:', 'leading:', 'trailing:', 'onTap:', 'onPressed:',
                        '//', '/*', 'gridDelegate:', 'mainAxisSpacing:', 'crossAxisSpacing:',
                        'childAspectRatio:', 'crossAxisCount:', 'borderRadius:', 'backgroundColor:',
                        'foregroundColor:', 'TextStyle(', 'fontWeight:', 'fontSize:', 'color:',
                        'mainAxisAlignment:', 'contentPadding:', 'elevation:', 'maxLines:',
                        'overflow:', 'textAlign:', 'selected:', 'margin:', 'shape:', 'border:',
                        'List.generate', 'itemCount:', 'itemBuilder:', 'index)',
                        'leading:', 'subtitle:', 'title:', ']', ');', '},', '}', '  }',
                        'super.key', 'required', 'this.', 'widget.', 'context',
                        'int _', 'bool _', 'String _']
        
        is_code = any(stripped.startswith(kw) for kw in dart_keywords)
        
        # Baris sangat diindentasi (4+ spasi, bukan dari blok analisis)
        heavily_indented = line.startswith('    ') and not stripped.startswith('Analisis') and not stripped.startswith('Ketika') and not stripped.startswith('Pada') and not stripped.startswith('Mengubah') and not stripped.startswith('Menambahkan') and not stripped.startswith('Memindahkan') and not stripped.startswith('Menggunakan') and not stripped.startswith('Pengaksesan') and not stripped.startswith('Formula') and not stripped.startswith('Saat')
        
        if (is_code or heavily_indented) and not in_code:
            # Mulai blok kode
            in_code = True
            code_lines = []
            if out and out[-1] != '':
                out.append('')
            out.append(f'```{code_lang}')
            code_lines.append(stripped)
            out.append(stripped)
            i += 1
            continue
        
        if in_code:
            # Lanjutkan blok kode jika masih ada konten
            if stripped == '' or stripped == '   ':
                # Cek apakah baris berikutnya masih kode
                next_is_code = False
                if i + 1 < len(lines):
                    next_stripped = lines[i+1].strip()
                    next_is_code = (any(next_stripped.startswith(kw) for kw in dart_keywords) or 
                                   lines[i+1].startswith('    '))
                    # Juga cek baris sesudahnya
                    if not next_is_code and i + 2 < len(lines):
                        next2_stripped = lines[i+2].strip()
                        next_is_code = (any(next2_stripped.startswith(kw) for kw in dart_keywords) or
                                       lines[i+2].startswith('    '))
                
                if next_is_code:
                    out.append('')
                    i += 1
                    continue
                else:
                    # Tutup blok kode
                    in_code = False
                    out.append('```')
                    out.append('')
            else:
                out.append(stripped)
                i += 1
                continue
        
        # Proses baris normal
        if stripped == '' or stripped == '   ':
            if not prev_blank:
                out.append('')
                prev_blank = True
        else:
            prev_blank = False
            
            # Header besar (latihan)
            if stripped.startswith('🔶') or stripped.startswith('📱'):
                if out and out[-1] != '':
                    out.append('')
                out.append(f'## {stripped}')
                out.append('')
            # Langkah (sub-header)
            elif stripped.startswith('Langkah '):
                if out and out[-1] != '':
                    out.append('')
                out.append(f'### {stripped}')
                out.append('')
            # Analisis/Perubahan dalam blockquote
            elif stripped.startswith('Analisis Laporan') or stripped.startswith('Analisis Perubahan'):
                if out and out[-1] != '':
                    out.append('')
                out.append(f'> **{stripped}**')
            elif stripped.startswith('Ketika ') or stripped.startswith('Pada nilai') or stripped.startswith('Formula') or stripped.startswith('Saat '):
                out.append(f'> - {stripped}')
            elif stripped.startswith('Mengubah ') or stripped.startswith('Menambahkan ') or stripped.startswith('Memindahkan ') or stripped.startswith('Menggunakan ') or stripped.startswith('Pengaksesan '):
                out.append(f'> - {stripped}')
            elif stripped.startswith('GridView.count ') or stripped.startswith('GridView.builder '):
                out.append(f'> - {stripped}')
            # Identitas mahasiswa di awal
            elif stripped.startswith('Nama:') or stripped.startswith('Nim:') or stripped.startswith('Kelas:') or stripped.startswith('Matkul:'):
                out.append(f'**{stripped}**')
            # Item list dengan dash atau bullet
            elif stripped.startswith('- ') or stripped.startswith('* '):
                out.append(stripped)
            # Sub-item (diindentasi)
            elif line.startswith('    ') and not is_code:
                out.append(f'    - {stripped}')
            else:
                out.append(stripped)
        
        i += 1
    
    # Tutup blok kode jika masih terbuka
    if in_code:
        out.append('```')
        out.append('')
    
    # Post-processing
    result = '\n'.join(out)
    # Normalisasi multiple blank lines
    result = re.sub(r'\n{3,}', '\n\n', result)
    
    return result


# Buat header yang rapi
header = """# Laporan Praktikum Pemrograman Mobile

| Field  | Value                                    |
|--------|------------------------------------------|
| Nama   | Ammar                                    |
| NIM    | 2024573010129                            |
| Kelas  | TI3B                                     |
| Matkul | Praktikum Pemograman Mobile (With Flutter) |

---

"""

# Build konten utama
body = build_formatted_md()

# Hapus baris identitas awal yang sudah ada di header
body = re.sub(r'\*\*Nama:.*?\*\*\n', '', body)
body = re.sub(r'\*\*Nim:.*?\*\*\n', '', body)
body = re.sub(r'\*\*Kelas:.*?\*\*\n', '', body)
body = re.sub(r'\*\*Matkul:.*?\*\*\n', '', body)

# Hapus baris kosong di awal body
body = body.lstrip('\n')

final_content = header + body

# Tulis file output
with open(OUTPUT_MD, 'w', encoding='utf-8') as f:
    f.write(final_content)

print(f'\nFile Markdown bersih ditulis: {OUTPUT_MD}')
print(f'Total karakter: {len(final_content)}')
print(f'Total baris: {final_content.count(chr(10))}')
