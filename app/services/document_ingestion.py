from pypdf import PdfReader
from io import BytesIO
from pathlib import Path

def extract_document_text(filename: str, file_content: bytes):

    file_extension = Path(filename).suffix.lower()

    if file_extension == ".pdf":

        pdf_file = BytesIO(file_content)

        reader = PdfReader(pdf_file)

        extracted_text = ""

        for page in reader.pages:

            extracted_text += page.extract_text() or ""

        source_type = "pdf"

    elif file_extension == ".txt":

        extracted_text = file_content.decode(
            "utf-8",
            errors="replace"
        )

        source_type = "txt"

    else:

        raise ValueError("Only PDF and TXT files are supported.")

    return {
        "filename": filename,
        "content": extracted_text,
        "source_type": source_type
    }