# Pandoc Conversion Guide: Laprak_Mobile_7.md → PDF

## Quick Start

### Option 1: Best Quality (Recommended)
```bash
pandoc Laprak_Mobile_7_OPTIMIZED.md \
  -o Laprak_Mobile_7.pdf \
  --css=style/laprak_style.css \
  --pdf-engine=weasyprint \
  --standalone \
  --toc
```

### Option 2: Maximum Compatibility
```bash
pandoc Laprak_Mobile_7_OPTIMIZED.md \
  -o Laprak_Mobile_7.pdf \
  --css=style/laprak_style.css \
  --pdf-engine=wkhtmltopdf \
  --standalone
```

### Option 3: Using HTML as Intermediary (Most Stable)
```bash
# Step 1: Markdown → HTML
pandoc Laprak_Mobile_7_OPTIMIZED.md \
  -o Laprak_Mobile_7.html \
  --css=style/laprak_style.css \
  --standalone

# Step 2: HTML → PDF
wkhtmltopdf Laprak_Mobile_7.html Laprak_Mobile_7.pdf
```

---

## Installation

### Ubuntu/Debian
```bash
# Install Pandoc
sudo apt-get update
sudo apt-get install pandoc

# Install PDF engines (choose one or both)
sudo apt-get install weasyprint
sudo apt-get install wkhtmltopdf
```

### macOS
```bash
brew install pandoc
brew install weasyprint
brew install wkhtmltopdf
```

### Windows
```bash
# Using Chocolatey
choco install pandoc
choco install weasyprint

# Or download from:
# - Pandoc: https://pandoc.org/installing.html
# - wkhtmltopdf: https://wkhtmltopdf.org/
```

---

## Analysis: What Changed for Better Compatibility

### ✅ Improvements Made

1. **Removed redundant separators**
   - Changed `---\n\n---` → Single `---`
   - Cleaner page break handling

2. **Fixed heading hierarchy**
   - Latihan 1, 2 → Now proper `h2` instead of `h1`
   - Better table of contents generation

3. **Standardized image syntax**
   - Removed HTML `<img>` tags
   - Converted to `![alt text](path)` Markdown format
   - Added descriptive captions with **bold text**

4. **Separated side-by-side images**
   - Changed from: `<img width="48%" /> <img width="48%" />`
   - To: Individual images with separate labels
   - More compatible with PDF rendering

5. **Improved list formatting**
   - More consistent spacing
   - Better hierarchical structure

6. **Enhanced code blocks**
   - Properly specified `dart` language
   - Consistent indentation
   - Better syntax highlighting in PDF

---

## Understanding Your CSS

### Key CSS Features in `laprak_style.css`

| Feature | Purpose | PDF Compatibility |
|---------|---------|------------------|
| `font-family: 'DejaVu Sans'` | Universal serif font | ✅ Excellent |
| `max-width: 180mm` | A4-friendly width | ✅ Good |
| `border-left: 4px solid #666666` | h2 accent | ✅ Good |
| `background: #f4f4f4` | h2 background | ✅ Good |
| `pre { background-color: #2b2b2b }` | Code block styling | ✅ Excellent |
| `@page { margin: 20mm }` | Page margins | ✅ Good |

**Note:** Not all CSS features are supported equally by all PDF engines:
- **weasyprint**: ~90% CSS3 support
- **wkhtmltopdf**: ~70% CSS support (but more stable)

---

## Pandoc Flags Explained

### Command: `pandoc [input] -o [output] [options]`

| Flag | Purpose | Example |
|------|---------|---------|
| `-o` | Output file | `-o Laprak_Mobile_7.pdf` |
| `--css` | CSS stylesheet | `--css=style/laprak_style.css` |
| `--pdf-engine` | PDF renderer | `--pdf-engine=weasyprint` |
| `--standalone` | Self-contained document | Auto page numbers, margins |
| `--toc` | Generate table of contents | Auto-linked TOC |
| `-N` | Number sections | `## Heading` → `1. Heading` |
| `--highlight-style` | Code syntax theme | `--highlight-style=tango` |
| `--variable` | Set template variables | `--variable=geometry:margin=2cm` |

---

## Troubleshooting Common Issues

### Problem 1: Images Not Showing

**Symptom:** Blank space where images should be

**Solutions:**
```bash
# Ensure images exist:
ls -la images/
ls -la images/latihan1/
ls -la images/latihan2/

# Check image paths in Markdown:
grep -n "!\[" Laprak_Mobile_7_OPTIMIZED.md

# Convert with relative path from current directory:
cd /home/ramma/Data/KULIAH_5/mobile
pandoc Laprak_Mobile_7_OPTIMIZED.md -o Laprak_Mobile_7.pdf --css=style/laprak_style.css
```

### Problem 2: CSS Not Applied

**Symptom:** PDF looks plain, no formatting

**Solutions:**
```bash
# Use absolute path to CSS:
pandoc Laprak_Mobile_7_OPTIMIZED.md \
  -o Laprak_Mobile_7.pdf \
  --css=$(pwd)/style/laprak_style.css \
  --pdf-engine=weasyprint

# Or convert to HTML first to verify CSS:
pandoc Laprak_Mobile_7_OPTIMIZED.md \
  -o test.html \
  --css=style/laprak_style.css \
  --standalone
# Then open test.html in browser to verify
```

### Problem 3: PDF Engine Not Found

**Symptom:** `Error: pdflatex not found`

**Solution:**
```bash
# Use weasyprint instead:
pandoc Laprak_Mobile_7_OPTIMIZED.md \
  -o Laprak_Mobile_7.pdf \
  --pdf-engine=weasyprint

# Or check what's installed:
which weasyprint
which wkhtmltopdf
which pdflatex
```

### Problem 4: Large File Size

**Symptom:** PDF is >50MB

**Solution:**
```bash
# Use wkhtmltopdf with optimization:
wkhtmltopdf --lowquality Laprak_Mobile_7.html Laprak_Mobile_7.pdf

# Or reduce image quality in CSS:
# Add to laprak_style.css:
# img { image-rendering: pixelated; }
```

### Problem 5: Page Breaks at Wrong Places

**Solution:** Add manual page breaks in Markdown:

```markdown
## Section 2

Content here...

\pagebreak

## Section 3

More content...
```

---

## Advanced Customization

### Add Page Numbers and Header/Footer

Create `header.md`:
```markdown
---
header: "Laporan Praktikum Mobile - Pertemuan 4"
footer: "Tanggal: 6-10-2026"
---
```

Then:
```bash
pandoc header.md Laprak_Mobile_7_OPTIMIZED.md \
  -o Laprak_Mobile_7.pdf \
  --css=style/laprak_style.css \
  --pdf-engine=weasyprint
```

### Generate Table of Contents with Custom Depth

```bash
pandoc Laprak_Mobile_7_OPTIMIZED.md \
  -o Laprak_Mobile_7.pdf \
  --toc \
  --toc-depth=2 \
  --css=style/laprak_style.css
```

### Set Custom Paper Size

```bash
pandoc Laprak_Mobile_7_OPTIMIZED.md \
  -o Laprak_Mobile_7.pdf \
  --variable=papersize:a4 \
  --variable=geometry:margin=20mm \
  --css=style/laprak_style.css
```

---

## Recommended Workflow

### Step 1: Prepare Files
```bash
cd /home/ramma/Data/KULIAH_5/mobile

# Verify structure
ls -la Laprak_Mobile_7_OPTIMIZED.md
ls -la style/laprak_style.css
ls -la images/
```

### Step 2: Convert to HTML (Verify Rendering)
```bash
pandoc Laprak_Mobile_7_OPTIMIZED.md \
  -o Laprak_Mobile_7_preview.html \
  --css=style/laprak_style.css \
  --standalone \
  --toc

# Open in browser to verify
firefox Laprak_Mobile_7_preview.html
```

### Step 3: Convert to PDF
```bash
pandoc Laprak_Mobile_7_OPTIMIZED.md \
  -o Laprak_Mobile_7.pdf \
  --css=style/laprak_style.css \
  --pdf-engine=weasyprint \
  --standalone \
  --toc
```

### Step 4: Verify Output
```bash
# Check file size
ls -lh Laprak_Mobile_7.pdf

# View in PDF reader
evince Laprak_Mobile_7.pdf

# Or use:
# - Adobe Reader
# - Firefox (built-in)
# - Chrome
```

---

## PDF Engine Comparison

| Feature | weasyprint | wkhtmltopdf | pdflatex |
|---------|-----------|-----------|----------|
| CSS3 Support | 90% | 70% | 30% |
| Image Handling | Excellent | Good | Fair |
| Table of Contents | ✅ Native | ✅ Pandoc | ✅ Pandoc |
| Page Breaks | ✅ Automatic | ✅ Good | ✅ Manual |
| Performance | Medium | Fast | Slow |
| Installation | Easy | Easy | Complex |
| Stability | Good | Excellent | Good |

**Recommendation for your use case:** **weasyprint** (best for CSS styling + good performance)

---

## One-Liner Commands

### Copy-paste ready commands:

**Best Quality:**
```bash
cd /home/ramma/Data/KULIAH_5/mobile && pandoc Laprak_Mobile_7_OPTIMIZED.md -o Laprak_Mobile_7.pdf --css=style/laprak_style.css --pdf-engine=weasyprint --standalone --toc
```

**Maximum Compatibility:**
```bash
cd /home/ramma/Data/KULIAH_5/mobile && pandoc Laprak_Mobile_7_OPTIMIZED.md -o Laprak_Mobile_7.pdf --css=style/laprak_style.css --pdf-engine=wkhtmltopdf --standalone
```

**With Syntax Highlighting:**
```bash
cd /home/ramma/Data/KULIAH_5/mobile && pandoc Laprak_Mobile_7_OPTIMIZED.md -o Laprak_Mobile_7.pdf --css=style/laprak_style.css --pdf-engine=weasyprint --highlight-style=tango --standalone --toc
```

---

## Batch Conversion (All Laprak Files)

```bash
#!/bin/bash
cd /home/ramma/Data/KULIAH_5/mobile

for md_file in Laprak_Mobile_*.md; do
  pdf_file="${md_file%.md}.pdf"
  echo "Converting $md_file → $pdf_file"
  pandoc "$md_file" -o "$pdf_file" \
    --css=style/laprak_style.css \
    --pdf-engine=weasyprint \
    --standalone \
    --toc
done

echo "Done! Check PDF files:"
ls -lh Laprak_Mobile_*.pdf
```

Save as `batch_convert.sh`, then:
```bash
chmod +x batch_convert.sh
./batch_convert.sh
```

---

## Next Steps

1. **Install Pandoc and engine** (if not already done)
2. **Test with the OPTIMIZED file** (better compatibility)
3. **Use the recommended command** for best results
4. **Adjust CSS** as needed for your style preferences

Questions? Check Pandoc docs: https://pandoc.org/
