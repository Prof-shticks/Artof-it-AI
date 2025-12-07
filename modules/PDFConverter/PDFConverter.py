import PyPDF2
from typing import Optional, Tuple
import io
import uuid
import os


class PDFConverter:

    def __init__(self):
        pass

    def convert_pdf_to_text(self, pdf_file: bytes, output_dir: str = "files_txt_view") -> Optional[Tuple[str, str]]:

        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file))

            text_content = ""
            for page in pdf_reader.pages:
                text_content += page.extract_text() + "\n"

            text_content = text_content.strip()

            file_uuid = str(uuid.uuid4())
            file_path = os.path.join(output_dir, f"{file_uuid}.txt")

            # Save text content to file
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text_content)

            return text_content, file_path

        except PyPDF2.errors.PdfReadError:
            print("Error: Invalid PDF file")
            return None
        except Exception as e:
            print(f"Error converting PDF to text: {str(e)}")
            return None

    def get_pdf_info(self, pdf_file: bytes) -> Optional[dict]:

        try:
            pdf_reader = PyPDF2.PdfReader(io.BytesIO(pdf_file))

            info = pdf_reader.metadata
            return {
                "pages": len(pdf_reader.pages),
                "title": info.title,
                "author": info.author,
                "subject": info.subject,
                "creator": info.creator,
                "producer": info.producer
            }

        except Exception as e:
            print(f"Error getting PDF info: {str(e)}")
            return None
