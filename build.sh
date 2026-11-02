#!/usr/bin/env bash
# build.sh — Markdown -> PDF / HTML untuk laporan praktikum
#
# Pemakaian:
#   ./build.sh <file.md>               # buat PDF  -> result/<nama>.pdf
#   ./build.sh <file.md> html          # preview HTML mandiri (buka di browser)
#   ./build.sh <file.md> check         # hanya periksa gambar + gaya penulisan
#   ./build.sh <file.md> pdf --toc     # PDF dengan daftar isi otomatis
#
# Pengaturan yang sering diubah ada di blok KONFIGURASI.

set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"        # selalu jalan dari folder skrip

# ---------------------------- KONFIGURASI -----------------------------------
CSS="style/laprak_style.css"
OUT_DIR="result"
FROM="markdown+hard_line_breaks"           # 1x enter = baris baru
HIGHLIGHT="breezedark"                     # tema warna kode (cocok dgn CSS)
LANG_DOC="id"
# ----------------------------------------------------------------------------

usage() {
  sed -n '2,11p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

MODE="pdf"; TOC=0; INPUT=""
while [[ $# -gt 0 ]]; do
  case "$1" in
    -h|--help) usage; exit 0 ;;
    -t|--toc)  TOC=1 ;;
    pdf|html|check) MODE="$1" ;;
    -*) echo "Opsi tidak dikenal: $1" >&2; usage; exit 2 ;;
    *)  INPUT="$1" ;;
  esac
  shift
done

[[ -n "$INPUT" ]] || { echo "Error: file .md belum disebutkan." >&2; usage; exit 2; }
[[ -f "$INPUT" ]] || { echo "Error: file tidak ditemukan: $INPUT" >&2; exit 2; }

# ---------------------------- PEMERIKSAAN -----------------------------------
check_images() {
  local missing=0 path alt
  echo "== Cek gambar =="
  while IFS= read -r path; do
    [[ "$path" =~ ^https?:// ]] && continue
    if [[ ! -f "$path" ]]; then
      echo "  x hilang: $path"
      alt="$(find . -iname "$(basename "$path")" 2>/dev/null | head -n1 || true)"
      [[ -n "$alt" ]] && echo "      mungkin maksudnya: $alt  (huruf besar/kecil & folder harus persis)"
      missing=$((missing + 1))
    fi
  done < <(grep -oP '!\[[^\]]*\]\(\K[^)\s]+' "$INPUT" | sort -u)
  if (( missing == 0 )); then echo "  semua gambar ditemukan"; else echo "  $missing gambar hilang"; fi
  return $(( missing > 0 ))
}

lint_style() {
  local found=0
  echo "== Cek gaya penulisan =="
  if grep -nE '^---+[[:space:]]*$' "$INPUT" | grep -v '^1:' >/dev/null; then
    echo "  ! ada baris '---' (tidak dipakai; hapus, heading sudah memisahkan):"
    grep -nE '^---+[[:space:]]*$' "$INPUT" | sed 's/^/      baris /'; found=1
  fi
  if grep -nE '<img|<br' "$INPUT" >/dev/null; then
    echo "  ! ada tag HTML <img>/<br> (pakai ![caption](path) atau ::: side-by-side):"
    grep -nE '<img|<br' "$INPUT" | sed 's/^/      baris /'; found=1
  fi
  if grep -nE '\\pagebreak|\\newpage' "$INPUT" >/dev/null; then
    echo "  ! ada perintah LaTeX (tidak jalan di weasyprint; pakai '::: pagebreak'):"
    grep -nE '\\pagebreak|\\newpage' "$INPUT" | sed 's/^/      baris /'; found=1
  fi
  if grep -nE '^## Daftar Isi' "$INPUT" >/dev/null; then
    echo "  ! ada 'Daftar Isi' manual (link-nya rusak di pandoc; pakai opsi --toc)"; found=1
  fi
  (( found == 0 )) && echo "  bersih"
  return 0
}

check_images || true
lint_style
[[ "$MODE" == "check" ]] && exit 0

# ---------------------------- BUILD -----------------------------------------
command -v pandoc >/dev/null || { echo "Error: pandoc belum terpasang." >&2; exit 1; }
[[ -f "$CSS" ]] || { echo "Error: CSS tidak ada: $CSS" >&2; exit 1; }
mkdir -p "$OUT_DIR"

NAME="$(basename "${INPUT%.md}")"
TITLE="$(grep -m1 '^# ' "$INPUT" | sed 's/^# //' || true)"
[[ -n "$TITLE" ]] || TITLE="$NAME"

ARGS=(
  "$INPUT"
  --from="$FROM"
  --standalone
  --css="$CSS"
  --resource-path=.
  --highlight-style="$HIGHLIGHT"
  --metadata "pagetitle=$TITLE"
  --variable "lang=$LANG_DOC"
  --variable "document-css=false"
)
(( TOC == 1 )) && ARGS+=(--toc --toc-depth=2)

case "$MODE" in
  pdf)
    if ! command -v weasyprint >/dev/null && [[ -x "$HOME/.venv/bin/weasyprint" ]]; then
      export PATH="$HOME/.venv/bin:$PATH"
    fi
    command -v weasyprint >/dev/null || { echo "Error: weasyprint belum terpasang." >&2; exit 1; }
    OUT="$OUT_DIR/$NAME.pdf"
    pandoc "${ARGS[@]}" --pdf-engine=weasyprint -o "$OUT"
    ;;
  html)
    OUT="$OUT_DIR/$NAME.html"
    pandoc "${ARGS[@]}" --embed-resources -o "$OUT"
    ;;
esac

echo "== Selesai =="
ls -lh "$OUT"
