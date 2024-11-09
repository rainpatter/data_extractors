
import pymupdf  # PyMuPDF
import re
import csv
import os
import re

path = "/home/georgia/projects/data_extractors/reports/NC_reports_for_analysis"
os.chdir(path)
file_list = [x for x in os.listdir(path) if ".~lock." not in x]

csv_columns = ['Assessment ID', "Use", "Persistence Tag", "Perfluoro Tag"]
csv_file = 'test_use_extract.csv'

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
    split_paragraphs_string = [x.strip() for x in re.split('\n\n|\n \n', processed_text_string)]
    no_empty_strings = [x for x in split_paragraphs_string if x != '']
    return no_empty_strings

def extract_use(text):
    dict = {"Use": None}
    if 'ASSESSMENT DETAILS' in text:

        sliced_text = text[text.index('ASSESSMENT DETAILS'):]

        for i, para in enumerate(sliced_text):
            if (para.startswith('Use') or para.startswith('USE')) and not para == "USE":
                dict['Use'] = sliced_text[i]
            elif para.upper() == "USE":
                dict['Use'] = sliced_text[i+1]
    else:
        for i, para in enumerate(text):
            if para.upper() == "USE":
                dict['Use'] = text[i+1]   
            elif 'USE, VOLUME AND FORMULATION' in para:
                dict['Use'] = text[i+1]  
            elif para.startswith('Use') or para.startswith('USE'):
                dict['Use'] = text[i]   
    if dict['Use'] != None:
        dict['Use'] = re.sub(r'\n|Use|USE', '', dict['Use'])      
    return dict

def perfluoro_persistence_tagging(text):
    dict = {"Persistence Tag": None,
            "Perfluoro Tag": None}
    for i, para in enumerate(text):
        if "persistence" in para or "persistent" in para:
            dict["Persistence Tag"] = text[i]
        if "PERFLUORO" in para.upper() or "POLYFLUORO" in para.upper():
            dict['Perfluoro Tag'] = text[i]
    if dict['Persistence Tag'] != None:
        dict['Persistence Tag'] = re.sub(r'\n', '', dict['Persistence Tag'])
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
    data_dict.update(perfluoro_persistence_tagging(extracted_text))
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

