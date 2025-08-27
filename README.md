# docr - Document OCR to Markdown

A lightweight command-line tool that converts documents, PDFs, and images to Markdown format using OCR (Optical Character Recognition).

## Features

- **Multiple Format Support**: PDF, images (JPG, PNG, TIFF, BMP), Word documents (DOCX, DOC), text files (TXT, CSV), and more
- **OCR Processing**: Uses Tesseract OCR via OCRmyPDF for high-quality text extraction
- **LLM-Ready Output**: Generates clean, sanitized Markdown perfect for language model processing
- **Batch Processing**: Process single files or entire directories
- **Smart Conversion**: Automatically handles format conversion (images→PDF, documents→PDF)
- **Fallback Extraction**: Multiple text extraction methods ensure maximum success rate

## Installation

### System Dependencies

First, install the required system packages:

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install tesseract-ocr tesseract-ocr-eng libreoffice ghostscript fonts-dejavu unpaper
```

**macOS:**
```bash
brew install tesseract libreoffice ghostscript
```

**Windows:**
- Install [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki)
- Install [LibreOffice](https://www.libreoffice.org/download/download/)

### Python Package

Install using uv (recommended):
```bash
# Clone the repository
git clone https://github.com/evcraddock/docr.git
cd docr

# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install dependencies and create virtual environment
uv sync

# Install in editable mode
uv pip install -e .
```

Or using pip:
```bash
# Clone the repository
git clone https://github.com/evcraddock/docr.git
cd docr

# Install in development mode
pip install -e .
```

## Usage

### Basic Usage

Convert a single file:
```bash
docr input.pdf output.md
```

Convert an image to markdown:
```bash
docr scan.jpg document.md
```

### Advanced Usage

```bash
# Process all files in a directory
docr /path/to/documents/ /path/to/output/

# Process recursively with verbose output
docr /path/to/docs/ /path/to/output/ --recursive --verbose

# Skip OCR for files that already have text
docr document.pdf output.md --no-force-ocr

# Use different OCR language
docr document.pdf output.md --language fra

# Overwrite existing output files
docr input.pdf output.md --overwrite
```

### Command Options

- `input_path`: Path to input file or directory
- `output_path`: Path to output Markdown file or directory
- `--no-force-ocr`: Skip OCR for pages with existing text (default: force OCR)
- `--language, -l`: OCR language code (default: eng)
- `--recursive, -r`: Process directories recursively
- `--overwrite`: Overwrite existing output files
- `--verbose, -v`: Enable verbose output
- `--version`: Show version information

### Supported Formats

**Input Formats:**
- **PDFs**: `.pdf`
- **Images**: `.jpg`, `.jpeg`, `.png`, `.tiff`, `.tif`, `.bmp`
- **Documents**: `.docx`, `.doc`, `.odt`, `.rtf`
- **Text**: `.txt`, `.csv`

**Output Format:**
- **Markdown**: `.md` with LLM-optimized formatting

## How It Works

1. **Format Detection**: Automatically detects input file format
2. **PDF Conversion**: Converts images and documents to PDF using LibreOffice/img2pdf
3. **OCR Processing**: Applies OCR using OCRmyPDF with Tesseract engine
4. **Markdown Conversion**: Extracts text and converts to Markdown using PyMuPDF4LLM
5. **Text Sanitization**: Cleans output for LLM compatibility (removes non-ASCII, normalizes whitespace)
6. **Fallback Handling**: Uses alternative extraction methods if primary conversion fails

## Configuration

### OCR Languages

docr supports all Tesseract language codes. Install additional language packs as needed:

```bash
# Install French language pack
sudo apt install tesseract-ocr-fra

# Use with docr
docr document.pdf output.md --language fra
```

Common language codes:
- `eng` - English (default)
- `fra` - French
- `deu` - German
- `spa` - Spanish
- `ita` - Italian
- `por` - Portuguese
- `rus` - Russian
- `chi_sim` - Chinese Simplified
- `jpn` - Japanese

## Examples

### Single File Processing
```bash
# Convert a scanned PDF to markdown
docr scanned-document.pdf clean-text.md

# Process a Word document
docr report.docx report.md

# Convert an image with text
docr screenshot.png extracted-text.md
```

### Batch Processing
```bash
# Process all PDFs in a folder
docr ./documents/ ./output/

# Process all files recursively
docr ./archive/ ./processed/ --recursive --verbose

# Process with custom settings
docr ./scans/ ./text/ --language deu --overwrite
```

## Performance

- **Parallel Processing**: OCR uses multiple cores automatically
- **Memory Efficient**: Processes files one at a time
- **Fast Conversion**: Optimized OCR parameters for speed vs. quality balance

Typical processing times (varies by document complexity):
- Simple PDF (10 pages): 30-60 seconds
- Scanned document (5 pages): 45-90 seconds
- Image with text: 10-30 seconds

## Troubleshooting

### Common Issues

**"tesseract not found"**
- Install Tesseract OCR system package
- Ensure it's in your PATH

**"libreoffice command not found"**
- Install LibreOffice
- Add to PATH if needed

**OCR produces poor results**
- Try `--force-ocr` flag
- Check image/PDF quality
- Verify language setting matches document

**Permission errors**
- Check file/directory permissions
- Ensure output directory is writable

## Development

### Project Structure
```
docr/
├── docr/
│   ├── __init__.py
│   ├── cli.py          # Command-line interface
│   ├── processor.py    # Core processing logic
│   └── __main__.py     # Entry point for python -m docr
├── pyproject.toml     # Project configuration and dependencies
└── README.md          # This file
```

### Running Tests
```bash
# Install development dependencies with uv
uv sync --all-extras

# Run tests
uv run pytest tests/

# Run with coverage
uv run pytest --cov=docr tests/

# Or activate the virtual environment and run directly
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pytest tests/
pytest --cov=docr tests/
```

## License

MIT License - see LICENSE file for details.

## Credits

Built with:
- [OCRmyPDF](https://github.com/ocrmypdf/ocrmypdf) - OCR processing
- [Tesseract](https://github.com/tesseract-ocr/tesseract) - Text recognition
- [PyMuPDF4LLM](https://github.com/pymupdf/PyMuPDF4LLM) - PDF to Markdown conversion
- [LibreOffice](https://www.libreoffice.org/) - Document conversion

Inspired by [exaOCR](https://github.com/ikantkode/exaOCR) for the core processing approach.