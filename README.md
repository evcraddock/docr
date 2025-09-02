# docr - Document OCR to Markdown

Convert documents, PDFs, and images to Markdown using OCR.

## Installation

**System Dependencies:**
```bash
# macOS
brew install tesseract libreoffice ghostscript

# Ubuntu/Debian
sudo apt install tesseract-ocr libreoffice ghostscript
```

**Install Package:**
```bash
git clone https://github.com/evcraddock/docr.git
cd docr
uv sync && uv pip install -e .
```

## Usage

```bash
# Convert single file
docr input.pdf output.md

# Process directory
docr /path/to/docs/ /path/to/output/ --recursive

# Use different language
docr document.pdf output.md --language fra
```

**Options:**
- `--recursive, -r`: Process directories recursively
- `--language, -l`: OCR language (default: eng)
- `--overwrite`: Overwrite existing files
- `--verbose, -v`: Verbose output

**Supported formats:** PDF, JPG, PNG, DOCX, TXT

## License

MIT