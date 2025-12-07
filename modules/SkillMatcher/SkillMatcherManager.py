from typing import Optional, Tuple, Dict, Any
import os
from modules.PDFConverter.PDFConverter import PDFConverter


class SkillMatcherManager:

    def __init__(self):
        self.pdf_converter = PDFConverter()
        self.resume_txt_dir = "file_resume_txt"

    def process_resume_pdf(self, pdf_file: bytes, filename: str = None) -> Optional[Dict[str, Any]]:

        try:
            # Convert PDF to text and save to file_resume_txt directory
            conversion_result = self.pdf_converter.convert_pdf_to_text(pdf_file, self.resume_txt_dir)

            if conversion_result is None:
                return None

            text_content, file_path = conversion_result

            # Get PDF metadata
            pdf_info = self.pdf_converter.get_pdf_info(pdf_file)

            return {
                "success": True,
                "filename": filename,
                "text_content": text_content,
                "saved_path": file_path,
                "metadata": pdf_info,
                "text_length": len(text_content),
                "output_directory": self.resume_txt_dir
            }

        except Exception as e:
            print(f"Error processing resume PDF: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "filename": filename
            }

    def get_resume_text(self, file_uuid: str) -> Optional[str]:

        try:
            file_path = os.path.join(self.resume_txt_dir, f"{file_uuid}.txt")
            if os.path.exists(file_path):
                with open(file_path, 'r', encoding='utf-8') as f:
                    return f.read()
            return None
        except Exception as e:
            print(f"Error reading resume text: {str(e)}")
            return None

    def list_processed_resumes(self) -> list:

        try:
            if not os.path.exists(self.resume_txt_dir):
                return []

            files_info = []
            for filename in os.listdir(self.resume_txt_dir):
                if filename.endswith('.txt'):
                    file_path = os.path.join(self.resume_txt_dir, filename)
                    file_uuid = filename.replace('.txt', '')
                    file_size = os.path.getsize(file_path)

                    files_info.append({
                        "uuid": file_uuid,
                        "filename": filename,
                        "path": file_path,
                        "size": file_size,
                        "created": os.path.getctime(file_path)
                    })

            return files_info
        except Exception as e:
            print(f"Error listing resume files: {str(e)}")
            return []
