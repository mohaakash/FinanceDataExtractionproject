import pypdf
import io
from pypdf.errors import PdfReadError


def extract_text_from_pdf(pdf_file_buffer: io.BytesIO) -> str:
    """
    Extracts text from a PDF file buffer using the pypdf library.

    Args:
        pdf_file_buffer: A file-like object containing the PDF data.

    Returns:
        A string containing all extracted text from the PDF, or an empty
        string if an error occurs.
    """
    try:
        # Use the modern pypdf library
        reader = pypdf.PdfReader(pdf_file_buffer)
        # Use a list comprehension and join for better performance over string concatenation
        page_texts = [page.extract_text() or "" for page in reader.pages]
        return "".join(page_texts)
    except PdfReadError as e:
        # Handle specific errors related to reading a corrupt/invalid PDF
        print(f"Error reading PDF file (likely corrupt or invalid): {e}")
        return ""
    except Exception as e:
        print(f"An unexpected error occurred while processing the PDF: {e}")
        return ""
