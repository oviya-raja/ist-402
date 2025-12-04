# Markdown to PDF Converter

Convert Markdown files to professional PDF documents using pandoc and playwright.

## Installation

The script requires:
- `pandoc` - Install with: `brew install pandoc`
- `playwright` - Will be auto-installed if missing

## Usage

```bash
# Basic usage - output will be README.pdf
python3 tools/markdown_to_pdf/markdown_to_pdf.py README.md

# Specify output location
python3 tools/markdown_to_pdf/markdown_to_pdf.py README.md output.pdf

# Convert from any location
python3 tools/markdown_to_pdf/markdown_to_pdf.py learning-path/W07/README.md W07_Final_Report.pdf
```

## Features

- ✅ Professional typography and styling
- ✅ Table of contents with page numbers
- ✅ Numbered sections
- ✅ High-quality image rendering
- ✅ Code syntax highlighting
- ✅ Professional color scheme
- ✅ Proper page margins and formatting (A4)

## Examples

```bash
# Convert W07 README
python3 tools/markdown_to_pdf/markdown_to_pdf.py learning-path/W07/README.md learning-path/W07/W07_Final_Report.pdf

# Convert any markdown file
python3 tools/markdown_to_pdf/markdown_to_pdf.py docs/notes.md docs/notes.pdf
```

## Command-Line Options

```bash
python3 tools/markdown_to_pdf/markdown_to_pdf.py <input.md> [output.pdf]

Arguments:
  input       Input markdown file (.md)
  output      Output PDF file (optional, defaults to input filename with .pdf extension)
```

## How It Works

1. Converts markdown to HTML using `pandoc` with professional styling
2. Converts HTML to PDF using `playwright` (headless Chromium browser)
3. Creates a high-quality PDF with proper formatting, images, and table of contents

