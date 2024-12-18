
import pymupdf  # PyMuPDF
import re
import csv
import os
import re

path = "/home/georgia/projects/data_extractors/reports/NC_reports_for_analysis"
os.chdir(path)
file_list = [x for x in os.listdir(path) if ".~lock." not in x]

csv_columns = ['Assessment ID', "Use", "Persistence Tag", "Perfluoro Tag"]
csv_file = 'test_identity_exposure_extract.csv'

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
    split_paragraphs_string = [x.strip() for x in re.split('\n\n|\n \n|\n', processed_text_string)]
    no_empty_strings = [x for x in split_paragraphs_string if x != '']
    return no_empty_strings

def extract_use(text):
    dict = {'Exempt information': None,
        'Chemical name': None,
            "Other names": None,
            'Marketing names': None
            }
    exempt_information = False
    extracted_exempt_information = []
    
    chemical_name = False
    extracted_chemical_names = []
    
    other_names = False
    extracted_other_names = []
    
    marketing_names = False
    extracted_marketing_names = []
    if "EXEMPT INFORMATION (SECTION 75 OF THE ACT)" in text:
        index = text.index("EXEMPT INFORMATION (SECTION 75 OF THE ACT)")
        if index:
            dict['Exempt information'] = text[index + 1:text.index('VARIATION OF DATA REQUIREMENTS (SECTION 24 OF THE ACT)')]
    return dict

# Example usage
all_assessments_data = []
for file in file_list:
# file = 'reports/NC_reports_for_analysis/PLC1465.pdf'
    assessment_id = file.split('.pdf')[0]
    data_dict = {
            'Assessment ID': assessment_id
        }
    extracted_text = extract_text_without_headers(file)
# print(extracted_text)
    data_dict.update(extract_use(extracted_text))
    print(data_dict)
    all_assessments_data.append(data_dict)

os.chdir('/home/georgia/projects/data_extractors')

try:
    with open(csv_file, 'w+') as csv_file:
        writer = csv.DictWriter(
            csv_file, fieldnames=csv_columns, delimiter=",", escapechar='\\')
        writer.writeheader()
        for data in all_assessments_data:
            writer.writerow(data)

except IOError:
    print("I/O Error")

# Print the result (or save to a file)

