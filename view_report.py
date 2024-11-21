
import pymupdf  # PyMuPDF
import re
import csv
import os
import re

def extract_text_without_headers(pdf_path, header_height_threshold=50, footer_height_threshold=50):
    doc = pymupdf.open(pdf_path)

    all_text = []

    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        
        # Extract text blocks with their position
        text_blocks = page.get_text("blocks")
        
        page_text = ""
        page_height = page.rect.height 
        for block in text_blocks:
            x0, y0, x1, y1, text, num1, num2 = block  # Get the coordinates (x0, y0) and text of each block

            
            # Skip blocks that are near the top of the page (header area)
            if y0 < header_height_threshold:  # Assuming headers are at the top of the page
                continue  # Skip this block (it's a header)
            
            if y1 > page_height - footer_height_threshold:  
                continue  # Skip this block (it's a footer)
            
            page_text += text + "\n"  # Add the text from the block to the page content

        all_text.append(page_text)
    
    processed_text_string = ''.join(all_text)
    split_paragraphs_string = [x.strip() for x in re.split('\n', processed_text_string)]
    return split_paragraphs_string


file = 'reports/NC_reports_for_analysis/STD1415.pdf'
assessment_id = file.split('.pdf')[0]
extracted_text = extract_text_without_headers(file)
print(extracted_text[:600])

