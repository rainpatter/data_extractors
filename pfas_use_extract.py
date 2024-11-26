
import pymupdf  # PyMuPDF
import re
import csv
import os
import re

path = "/home/georgia/projects/data_extractors/reports/NC_reports_for_analysis"
os.chdir(path)
list_of_assessments = [
    'EX5',
    'NA626',
    'NA651',
    'NA46',
    'NA588',
    'NA589',
    'NA576',
    'NA54',
    'NA479',
    'NA482',
    'NA428',
    'EX224',
    'LTD2047',
    'NA5',
    'LTD2031',
    'EX211',
    'EX213',
    'LTD1990',
    'NA317',
    'NA240',
    'LTD1986',
    'LTD1962',
    'EX209',
    'LTD1493',
    'LTD1892',
    'EX190',
    'LTD1667',
    'LTD1902',
    'STD1409',
    'LTD1498',
    'NA6',
    'NA241',
    'NA340',
    'STD1556',
    'NA12',
    'STD1535',
    'STD1551',
    'LTD1536',
    'LTD1539',
    'LTD1629',
    'STD1499',
    'EX187',
    'STD1479',
    'PLC22',
    'PLC1136',
    'LTD1559',
    'EX182',
    'STD1415',
    'LTD1597',
    'NA49',
    'PLC916',
    'LTD1532',
    'STD1302',
    'NA228',
    'NA227',
    'LTD1285',
    'NA216',
    'PLC671',
    'PLC675',
    'STD1076',
    'PLC504',
    'PLC550',
    'NA174',
    'PLC467',
    'PLC466',
    'NA161',
    'EX53',
    'NA164',
    'PLC384',
    'STD1035',
    'LTD1058',
    'PLC314',
    'STD1019',
    'NA137',
    'NA136',
    'LTD1003',
    'EX32',
    'NA920',
    'NA918',
    'NA949',
    'NA919',
    'NA85',
    'PLC156',
    'NA848',
    'NA803',
    'PLC175',
    'PLC155',
    'PLC154',
    'LTD2155'
]
file_list = [x for x in os.listdir(path) if ".~lock." not in x]
pfas_list = []
for item in list_of_assessments:
    for file in file_list:
        if item == file[:-4]:
            pfas_list.append(file)
            
print(pfas_list)
print(len(pfas_list))




csv_columns = ['Assessment ID', "Use", "Persistence Tag", "Perfluoro Tag", "Essential Tag", "Not suitable tag", "Recommended tag", "Fire Tag"]
csv_file = 'pfas_extract.csv'

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
            "Perfluoro Tag": None,
            "Essential Tag": None, 
            "Not suitable tag": None, 
            "Recommended tag": None, 
            "Fire Tag": None}
    persistence_lines = [line for line in text if 'persistent' in line or 'Persistent' in line]
    if persistence_lines:
        dict['Persistence Tag'] = '; '.join(persistence_lines)
        dict['Persistence Tag'] = re.sub(r'\n', '', dict['Persistence Tag']) 
    perfluoro_lines = [line for line in text if 'PERFLUORO' in line.upper() or 'POLYFLUORO' in line.upper()]
    if perfluoro_lines:
        dict['Perfluoro Tag'] = '; '.join(perfluoro_lines)
        dict['Perfluoro Tag'] = re.sub(r'\n', '', dict['Perfluoro Tag']) 
    essential_lines = [line for line in text if 'ESSENTIAL' in line.upper()]
    if essential_lines:
        dict['Essential Tag'] = '; '.join(essential_lines)
        dict['Essential Tag'] = re.sub(r'\n', '', dict['Essential Tag']) 
    not_suitable_lines = [line for line in text if 'NOT SUITABLE' in line.upper()]
    if not_suitable_lines:
        dict['Not suitable tag'] = '; '.join(not_suitable_lines)
        dict['Not suitable tag'] = re.sub(r'\n', '', dict['Not suitable tag']) 
    recommended_lines = [line for line in text if 'RECOMMENDED' in line.upper()]
    if recommended_lines:
        dict['Recommended tag'] = '; '.join(recommended_lines)
        dict['Recommended tag'] = re.sub(r'\n', '', dict['Recommended tag']) 
    fire_lines = [line for line in text if 'FIRE' in line.upper() or 'FLAME' in line.upper()]
    if fire_lines:
        dict['Fire Tag'] = '; '.join(fire_lines)
        dict['Fire Tag'] = re.sub(r'\n', '', dict['Fire Tag']) 
    return dict 

# Example usage
all_assessments_data = []
for file in pfas_list:
# file = 'reports/NC_reports_for_analysis/PLC1465.pdf'
    assessment_id = file.split('.pdf')[0]
    print(assessment_id)
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

