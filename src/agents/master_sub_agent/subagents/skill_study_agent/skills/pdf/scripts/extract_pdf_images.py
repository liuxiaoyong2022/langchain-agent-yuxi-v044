"""Extract embedded images from PDF files.

This script extracts all embedded images from a PDF file and saves them
to /tmp/{pdf_filename}/image_extract/ directory with sequential numbering.

Usage:
    python extract_pdf_images.py <pdf_path>

Example:
    python extract_pdf_images.py document.pdf
    # Output: /tmp/document/image_extract/001.jpg, /tmp/document/image_extract/002.png, ...
"""

import os
import sys
from pathlib import Path
from typing import Optional

try:
    import fitz  # PyMuPDF
except ImportError:
    print("Error: PyMuPDF (fitz) is required. Install it with: pip install PyMuPDF")
    sys.exit(1)


def get_image_format(image_bytes: bytes) -> str:
    """Detect image format from bytes."""
    if image_bytes[:4] == b'\xff\xd8\xff\xe0' or image_bytes[:4] == b'\xff\xd8\xff\xe1':
        return 'jpg'
    elif image_bytes[:8] == b'\x89\x50\x4e\x47\x0d\x0a\x1a\x0a':
        return 'png'
    elif image_bytes[:4] == b'GIF8':
        return 'gif'
    elif image_bytes[:2] == b'BM':
        return 'bmp'
    elif image_bytes[:4] == b'II\x2a\x00' or image_bytes[:4] == b'MM\x00\x2a':
        return 'tiff'
    else:
        return 'jpg'  # Default fallback


def extract_images(pdf_path: str, output_base_dir: str = "/tmp") -> list[str]:
    """
    Extract all embedded images from a PDF file.

    Args:
        pdf_path: Path to the PDF file
        output_base_dir: Base directory for output (default: /tmp)

    Returns:
        List of paths to extracted images
    """
    pdf_path = Path(pdf_path).resolve()

    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    # Get PDF filename without extension
    pdf_name = pdf_path.stem

    # Create output directory: /tmp/{pdf_name}/image_extract/
    output_dir = Path(output_base_dir) / pdf_name / "image_extract"
    output_dir.mkdir(parents=True, exist_ok=True)

    extracted_files = []

    # Open PDF
    doc = fitz.open(str(pdf_path))

    image_counter = 0

    # Extract images from each page
    for page_num, page in enumerate(doc, start=1):
        image_list = page.get_images(full=True)

        for img_index, img in enumerate(image_list, start=1):
            xref = img[0]

            # Extract image
            base_image = doc.extract_image(xref)

            if base_image:
                image_bytes = base_image["image"]
                image_format = get_image_format(image_bytes)

                # Generate filename with sequential numbering
                filename = f"{image_counter + 1:03d}.{image_format}"
                output_path = output_dir / filename

                # Save image
                with open(output_path, "wb") as f:
                    f.write(image_bytes)

                extracted_files.append(str(output_path))
                print(f"Extracted: {output_path} (page {page_num}, image {img_index})")

                image_counter += 1

    doc.close()

    if image_counter == 0:
        print(f"No embedded images found in {pdf_path}")
    else:
        print(f"\nExtracted {image_counter} image(s) to: {output_dir}")

    return extracted_files


def main():
    if len(sys.argv) < 2:
        print("Usage: python extract_pdf_images.py <pdf_path> [output_base_dir]")
        print("\nExamples:")
        print("  python extract_pdf_images.py document.pdf")
        print("  python extract_pdf_images.py document.pdf /custom/output/path")
        sys.exit(1)

    pdf_path = sys.argv[1]
    output_base_dir = sys.argv[2] if len(sys.argv) > 2 else "/tmp"

    try:
        extract_images(pdf_path, output_base_dir)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
