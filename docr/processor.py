"""
Document processing module for docr.
Converts PDFs, images, and documents to Markdown using OCR.
"""

import subprocess
import os
import tempfile
import time
import re
from pathlib import Path
from typing import Tuple, Optional

import img2pdf
import pymupdf4llm
import pymupdf


class DocumentProcessor:
    """Handles document to markdown conversion with OCR."""
    
    def __init__(self, force_ocr: bool = True, language: str = 'eng'):
        """
        Initialize processor.
        
        Args:
            force_ocr: Whether to force OCR on all pages
            language: OCR language code (default: 'eng')
        """
        self.force_ocr = force_ocr
        self.language = language
    
    def process_file(self, input_path: str, output_path: str) -> Tuple[bool, Optional[str], float]:
        """
        Process a single file and convert to Markdown.
        
        Args:
            input_path: Path to input file
            output_path: Path to save Markdown output
            
        Returns:
            Tuple of (success, error_message, processing_time)
        """
        start_time = time.time()
        
        try:
            input_path = Path(input_path).resolve()
            output_path = Path(output_path).resolve()
            
            if not input_path.exists():
                return False, f"Input file does not exist: {input_path}", 0.0
            
            # Create output directory if needed
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with tempfile.TemporaryDirectory() as tmpdir:
                # Convert to PDF if needed
                pdf_path = self._convert_to_pdf(input_path, tmpdir)
                
                # Apply OCR
                ocr_pdf_path = self._apply_ocr(pdf_path, tmpdir)
                
                # Convert to Markdown
                markdown_text = self._convert_to_markdown(ocr_pdf_path)
                
                # Save output
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(markdown_text)
                
                processing_time = time.time() - start_time
                return True, None, processing_time
                
        except Exception as e:
            processing_time = time.time() - start_time
            return False, str(e), processing_time
    
    def _convert_to_pdf(self, input_path: Path, tmpdir: str) -> str:
        """Convert input file to PDF format."""
        ext = input_path.suffix.lower()
        
        if ext == '.pdf':
            return str(input_path)
        
        pdf_path = os.path.join(tmpdir, "input.pdf")
        
        if ext in ['.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp']:
            # Convert image to PDF using img2pdf
            with open(pdf_path, "wb") as f:
                f.write(img2pdf.convert(str(input_path)))
                
        elif ext in ['.txt', '.csv', '.docx', '.doc', '.odt', '.rtf']:
            # Convert document to PDF using LibreOffice
            result = subprocess.run([
                'libreoffice', '--headless', '--convert-to', 'pdf',
                '--outdir', tmpdir, str(input_path)
            ], check=True, capture_output=True, text=True)
            
            # LibreOffice creates PDF with same name as input
            converted_name = input_path.stem + '.pdf'
            converted_path = os.path.join(tmpdir, converted_name)
            
            if not os.path.exists(converted_path):
                raise FileNotFoundError(f"LibreOffice conversion failed: {converted_path}")
            
            pdf_path = converted_path
            
        else:
            raise ValueError(f"Unsupported file format: {ext}")
        
        return pdf_path
    
    def _apply_ocr(self, pdf_path: str, tmpdir: str) -> str:
        """Apply OCR to PDF using OCRmyPDF."""
        ocr_output = os.path.join(tmpdir, "ocr_output.pdf")
        
        # OCRmyPDF command with optimized parameters from reference
        cmd = [
            'ocrmypdf',
            '-l', self.language,
            '--deskew',
            '--clean',
            '--tesseract-timeout', '300',
            '--jobs', '2'
        ]
        
        # Add force OCR or skip text based on setting
        if self.force_ocr:
            cmd.append('--force-ocr')
        else:
            cmd.append('--skip-text')
        
        cmd.extend([pdf_path, ocr_output])
        
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        return ocr_output
    
    def _convert_to_markdown(self, pdf_path: str) -> str:
        """Convert OCR'd PDF to Markdown format."""
        try:
            # Primary method: PyMuPDF4LLM for LLM-optimized markdown
            md_text = pymupdf4llm.to_markdown(pdf_path, write_images=False)
            
            # Sanitize for LLM compatibility (from reference code)
            md_text = re.sub(r'[^\x00-\x7F]+', '', md_text)  # Remove non-ASCII
            md_text = re.sub(r'\s+', ' ', md_text).strip()   # Normalize whitespace
            
            return md_text
            
        except Exception as md_error:
            # Fallback: block-based text extraction
            return self._fallback_text_extraction(pdf_path, md_error)
    
    def _fallback_text_extraction(self, pdf_path: str, original_error: Exception) -> str:
        """Fallback text extraction method."""
        try:
            doc = pymupdf.open(pdf_path)
            fallback_text = f"# Document Conversion\n\n*Note: Primary markdown conversion failed ({str(original_error)}), using fallback extraction.*\n\n"
            
            for page in doc:
                try:
                    blocks = page.get_text("blocks", flags=pymupdf.TEXTFLAGS_TEXT)
                    fallback_text += f"\n## Page {page.number + 1}\n\n"
                    
                    for block in blocks:
                        text = block[4].strip()  # Block text content
                        if text:
                            fallback_text += f"{text}\n\n"
                            
                except Exception as page_error:
                    fallback_text += f"*[Page {page.number + 1}: Error extracting text: {str(page_error)}]*\n\n"
            
            doc.close()
            
            # Apply same sanitization
            fallback_text = re.sub(r'[^\x00-\x7F]+', '', fallback_text)
            fallback_text = re.sub(r'\s+', ' ', fallback_text).strip()
            
            return fallback_text
            
        except Exception as fallback_error:
            return f"# Conversion Failed\n\nBoth primary and fallback text extraction failed.\n\nPrimary error: {str(original_error)}\nFallback error: {str(fallback_error)}"


def get_supported_extensions():
    """Return list of supported file extensions."""
    return [
        '.pdf',
        '.jpg', '.jpeg', '.png', '.tiff', '.tif', '.bmp',
        '.txt', '.csv', '.docx', '.doc', '.odt', '.rtf'
    ]


def is_supported_file(file_path: str) -> bool:
    """Check if file extension is supported."""
    return Path(file_path).suffix.lower() in get_supported_extensions()