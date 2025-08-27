"""
docr - Document OCR to Markdown converter.

A command-line tool that converts PDFs, images, and documents 
to Markdown format using OCR.
"""

__version__ = "0.1.0"
__author__ = "Erik Craddock"

from .processor import DocumentProcessor, get_supported_extensions, is_supported_file

__all__ = ['DocumentProcessor', 'get_supported_extensions', 'is_supported_file']