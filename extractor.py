from PyPDF2 import PdfReader
import os
import csv
import re

path = "/home/georgia/projects/data_extractors/reports/NC_reports_for_analysis"
os.chdir(path)
file_list = [x for x in os.listdir(path) if ".~lock." not in x]

csv_columns = ['Assessment ID', "SECTION 64(1)", "SECTION 64(2)"]
csv_file = 'test_sn_extract.csv'


def get_text(file):
    reader = PdfReader(file)
    fulltext = ''
    for page in reader.pages:
        fulltext += page.extract_text()
    fulltext = fulltext.split('\n')
    cleaned_fulltext = list(
        filter(None, [re.sub('\s+', ' ', string).strip() for string in fulltext]))
    return cleaned_fulltext


s1_start_index = None


def get_sn_conditions(text):
    s1 = '64(1)'
    s2 = '64(2)'
    stop = ['Director will then decide', 'Director will']
    other_stop = ['BIBLIOGRAPHY', 'REFERENCES']
    indices = {
        's1': None,
        's2': None,
        'end': None
    }
    dict = {
        "SECTION 64(1)": None,
        "SECTION 64(2)": None
    }
    for i, line in enumerate(text):

        if s1 in line:
            indices['s1'] = i+1
        if s2 in line:
            indices['s2'] = i+1
        if any(string in line for string in stop):
            indices['end'] = i
        elif indices['end'] == None:
            if any(string in line for string in other_stop):
                indices['end'] = i
    if (indices['s1'] != None) and (indices['s2'] == None):
        dict = {"SECTION 64(1)": (''.join(text[indices['s1']:indices['end']])),
                "SECTION 64(2)": 'None'}
    if (indices['s2'] != None) and (indices['s1'] == None):
        dict = {"SECTION 64(1)": 'None',
                "SECTION 64(2)": text[indices['s2']:indices['end']]}
    if indices['s1'] and indices['s2'] != None:
        dict = {"SECTION 64(1)": (''.join(text[indices['s1']:(indices['s2']-1)])),
                "SECTION 64(2)": (''.join(text[indices['s2']:indices['end']]))}
    return dict


def get_other_headers(text):
    dict


all_assessments_data = []
for file in file_list:
    assessment_id = file.split('.pdf')[0]
    if 'NA' in assessment_id:
        continue
    else:
        data_dict = {
            'Assessment ID': assessment_id
        }
        print(assessment_id)
        text = get_text(file)
        data_dict.update(get_sn_conditions(text))
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

    # fulltext = fulltext.split('\n')
    # cleaned_fulltext = list(filter(None,[string.strip() for string in fulltext]))
    # print(cleaned_fulltext[0])

# data_dict = {}

# # data_dict['Assessment Report'] = cleaned_fulltext[0].split(': ')[1]

# # sn_string_start_index = None
# # sn_string_end_index = None

# # ohs_e_start_index = None
# # ohs_e_end_index = None

# # ph_e_start_index = None
# # ph_e_end_index = None

# # hh_e_start_index = None
# # hh_e_end_index = None

# # ohs_risk_start_index = None
# # ohs_risk_end_index = None

# # ph_risk_start_index = None
# # ph_risk_end_index = None

# hh_start_index = None
# hh_end_index = None

# sn_64_1_start_index = None
# sn_64_1_end_index = None

# sn_64_2_start_index = None
# sn_64_2_end_index = None


# for index, line in enumerate(cleaned_fulltext_no_contents):
#     if line.replace(' ','').upper == 'HAZARDCLASSIFICATION':
#         print(index)
#         data_dict['Hazard classification'] = cleaned_fulltext_no_contents[index+1]
#     if line.replace(' ','').upper() == 'HUMANHEALTHRISKASSESSMENT':
#         hh_start_index = index+1

#     if line.replace(' ','').upper() == 'ENVIRONMENTALRISKASSESSMENT':
#         hh_end_index = index

#     if 'UNDERSECTION64(1)OFTHEACT' in line.replace(' ','').upper():

#         sn_64_1_start_index = index+1
#     if 'UNDERSECTION64(2)OFTHEACT' in line.replace(' ','').upper():
#         sn_64_1_end_index = index-1
#         sn_64_2_start_index = index+1
#     if 'THEDIRECTORWILLTHENDECIDE' in line.replace(' ','').upper():
#         sn_64_2_end_index = index-1
#     if line.replace(' ', '') == 'CHEMICALNAME':
#         data_dict['Chemical name'] = cleaned_fulltext_no_contents[index+1]
#     if line.replace(' ','') == 'CASNUMBER':
#         data_dict['CAS RN'] = cleaned_fulltext_no_contents[index+1]
#     if line.replace(' ','') == 'USE':
#         data_dict['Use'] = cleaned_fulltext_no_contents[index+1]


# data_dict['Human health risk assessment'] = ''.join(cleaned_fulltext_no_contents[hh_start_index:hh_end_index])
# data_dict['Section 64(1)'] = ''.join(cleaned_fulltext_no_contents[sn_64_1_start_index: sn_64_1_end_index])
# data_dict['Section 64(2)'] = ''.join(cleaned_fulltext_no_contents[sn_64_2_start_index: sn_64_2_end_index])


# #     if line.startswith('9.2.1.'):
# #         ohs_e_start_index = index+1
# #     if line.startswith('9.2.2.'):
# #          ohs_e_end_index = index-1
# #          ph_e_start_index = index+1
# #     if line.startswith('9.2.3.'):
# #         ph_e_end_index = index-1
# #         hh_e_start_index = index+1
# #     if line.startswith('9.2.4.'):
# #        hh_e_end_index = index-1
# #        ohs_risk_start_index = index+1
# #     if line.startswith('9.2.5.'):
# #         ohs_risk_end_index = index-1
# #         ph_risk_start_index = index+1
# #     if line.startswith('10.'):
# #         ph_risk_end_index = index-1
# #     if line.startswith('10.1.'):
# #         data_dict['Hazard classification'] = cleaned_fulltext_no_contents[index+1]
# #     if line.startswith('12.1'):
# #         sn_string_start_index = index+1
# #     if line.startswith('13.'):
# #         sn_string_end_index = index-1

# # data_dict['SN Conditions'] = cleaned_fulltext_no_contents[sn_string_start_index:sn_string_end_index]
# # data_dict['Occupational health and safety - exposure assessment'] = cleaned_fulltext_no_contents[ohs_e_start_index: ohs_e_end_index]
# # data_dict['Public health - exposure assessment'] = cleaned_fulltext_no_contents[ph_e_start_index:ph_e_end_index]
# # data_dict['Human health - affections assessment'] = cleaned_fulltext_no_contents[hh_e_start_index: hh_e_end_index]
# # data_dict['Occupational health and safety - risk characterisation'] = cleaned_fulltext_no_contents[ohs_risk_start_index: ohs_risk_end_index]
# # data_dict['Public health - risk assessment'] = cleaned_fulltext_no_contents[ph_risk_start_index:ph_risk_end_index]


# print(data_dict)
