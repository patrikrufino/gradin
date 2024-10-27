# utils/tiling.py
import fitz
import os
import time
from django.conf import settings
from typing import Optional

class Tiling:
    def __init__(self, filepath: str) -> None:
        self.filepath = filepath
    
    def pdf_file(self, output_prefix: str, rows: int, cols: int) -> Optional[str]:  # Adicionando anotações de tipo
        pdf_doc = fitz.open(self.filepath)

        if len(pdf_doc) == 0:
            print("O PDF não contém páginas.")
            return None

        output_pdf = fitz.open()

        for page_number in range(len(pdf_doc)):
            page = pdf_doc[page_number]
            rect = page.rect

            piece_width = rect.width / cols
            piece_height = rect.height / rows

            for row in range(rows):
                for col in range(cols):
                    x0 = col * piece_width
                    y0 = row * piece_height
                    x1 = x0 + piece_width
                    y1 = y0 + piece_height

                    piece_rect = fitz.Rect(x0, y0, x1, y1)

                    new_page = output_pdf.new_page(width=piece_width, height=piece_height)
                    new_page.show_pdf_page(new_page.rect, pdf_doc, page_number, clip=piece_rect)

        timestamp = int(time.time())
        output_file_path: str = os.path.join(settings.MEDIA_ROOT, 'temp', f"{output_prefix}_{timestamp}.pdf")
        output_pdf.save(output_file_path)
        output_pdf.close()
        pdf_doc.close()

        return output_file_path
