"""
Command-line interface for docr.
"""

import argparse
import sys
import os
from pathlib import Path
from typing import List

from .processor import DocumentProcessor, get_supported_extensions, is_supported_file
from . import __version__


def create_parser() -> argparse.ArgumentParser:
    """Create and configure argument parser."""
    parser = argparse.ArgumentParser(
        prog='docr',
        description='Convert documents, PDFs, and images to Markdown using OCR',
        epilog=f'Supported formats: {", ".join(get_supported_extensions())}'
    )
    
    parser.add_argument(
        'input_path',
        help='Path to input file or directory'
    )
    
    parser.add_argument(
        'output_path',
        help='Path to output Markdown file or directory'
    )
    
    parser.add_argument(
        '--no-force-ocr',
        action='store_true',
        help='Skip OCR for pages that already have text (default: force OCR on all pages)'
    )
    
    parser.add_argument(
        '--language', '-l',
        default='eng',
        help='OCR language code (default: eng)'
    )
    
    parser.add_argument(
        '--recursive', '-r',
        action='store_true',
        help='Process directories recursively'
    )
    
    parser.add_argument(
        '--overwrite',
        action='store_true',
        help='Overwrite existing output files'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'docr {__version__}'
    )
    
    return parser


def find_input_files(input_path: Path, recursive: bool = False) -> List[Path]:
    """Find all supported input files."""
    files = []
    
    if input_path.is_file():
        if is_supported_file(str(input_path)):
            files.append(input_path)
        else:
            print(f"Warning: Unsupported file type: {input_path.suffix}", file=sys.stderr)
    
    elif input_path.is_dir():
        pattern = "**/*" if recursive else "*"
        for file_path in input_path.glob(pattern):
            if file_path.is_file() and is_supported_file(str(file_path)):
                files.append(file_path)
    
    else:
        raise FileNotFoundError(f"Input path does not exist: {input_path}")
    
    return sorted(files)


def determine_output_path(input_file: Path, output_path: Path, is_single_file: bool) -> Path:
    """Determine the output path for a given input file."""
    if is_single_file:
        # Single file: output_path is the exact output file
        return output_path
    else:
        # Multiple files: output_path is directory, create .md file
        md_filename = input_file.stem + '.md'
        return output_path / md_filename


def main():
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    try:
        input_path = Path(args.input_path).resolve()
        output_path = Path(args.output_path).resolve()
        
        # Find all input files
        input_files = find_input_files(input_path, args.recursive)
        
        if not input_files:
            print("No supported files found.", file=sys.stderr)
            sys.exit(1)
        
        is_single_file = len(input_files) == 1 and input_path.is_file()
        
        # Create processor
        processor = DocumentProcessor(
            force_ocr=not args.no_force_ocr,
            language=args.language
        )
        
        # Process files
        total_files = len(input_files)
        successful = 0
        failed = 0
        
        for i, input_file in enumerate(input_files, 1):
            if args.verbose:
                print(f"[{i}/{total_files}] Processing: {input_file}")
            
            # Determine output file path
            output_file = determine_output_path(input_file, output_path, is_single_file)
            
            # Check if output already exists
            if output_file.exists() and not args.overwrite:
                print(f"Skipping {input_file} (output exists, use --overwrite to replace)")
                continue
            
            # Process the file
            success, error_msg, processing_time = processor.process_file(
                str(input_file), 
                str(output_file)
            )
            
            if success:
                successful += 1
                if args.verbose:
                    print(f"  ✓ Completed in {processing_time:.2f}s -> {output_file}")
                elif total_files == 1:
                    print(f"Successfully converted to {output_file}")
            else:
                failed += 1
                print(f"  ✗ Failed: {error_msg}", file=sys.stderr)
        
        # Print summary for multiple files
        if total_files > 1:
            print(f"\nProcessing complete: {successful} successful, {failed} failed")
        
        # Exit with error code if any files failed
        if failed > 0:
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nInterrupted by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()