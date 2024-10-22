from PyPDF2 import PdfReader
import re

reader = PdfReader('./reports/STD_1647 - New Chemical Assessment - 20 August 2018.pdf')

fulltext = ''
for page in reader.pages:
    fulltext += page.extract_text()
    
fulltext = fulltext.split('\n')
cleaned_fulltext = list(filter(None,[string.strip() for string in fulltext]))
cleaned_fulltext_no_contents = cleaned_fulltext[cleaned_fulltext.index('CONCLUSIONS AND REGULATORY OBLIGATIONS')+1:]


data_dict = {}

# data_dict['Assessment Report'] = cleaned_fulltext[0].split(': ')[1]

# sn_string_start_index = None
# sn_string_end_index = None

# ohs_e_start_index = None
# ohs_e_end_index = None

# ph_e_start_index = None
# ph_e_end_index = None

# hh_e_start_index = None
# hh_e_end_index = None

# ohs_risk_start_index = None
# ohs_risk_end_index = None

# ph_risk_start_index = None
# ph_risk_end_index = None

hh_start_index = None
hh_end_index = None

sn_64_1_start_index = None
sn_64_1_end_index = None

sn_64_2_start_index = None
sn_64_2_end_index = None


for index, line in enumerate(cleaned_fulltext_no_contents):
    if line.replace(' ','').upper == 'HAZARDCLASSIFICATION':
        print(index)
        data_dict['Hazard classification'] = cleaned_fulltext_no_contents[index+1]
    if line.replace(' ','').upper() == 'HUMANHEALTHRISKASSESSMENT':
        hh_start_index = index+1

    if line.replace(' ','').upper() == 'ENVIRONMENTALRISKASSESSMENT':
        hh_end_index = index

    if 'UNDERSECTION64(1)OFTHEACT' in line.replace(' ','').upper():

        sn_64_1_start_index = index+1
    if 'UNDERSECTION64(2)OFTHEACT' in line.replace(' ','').upper():
        sn_64_1_end_index = index-1
        sn_64_2_start_index = index+1
    if 'THEDIRECTORWILLTHENDECIDE' in line.replace(' ','').upper():
        sn_64_2_end_index = index-1
    if line.replace(' ', '') == 'CHEMICALNAME':
        data_dict['Chemical name'] = cleaned_fulltext_no_contents[index+1]
    if line.replace(' ','') == 'CASNUMBER':
        data_dict['CAS RN'] = cleaned_fulltext_no_contents[index+1]    
    if line.replace(' ','') == 'USE':
        data_dict['Use'] = cleaned_fulltext_no_contents[index+1]
        
        
        
data_dict['Human health risk assessment'] = ''.join(cleaned_fulltext_no_contents[hh_start_index:hh_end_index])
data_dict['Section 64(1)'] = ''.join(cleaned_fulltext_no_contents[sn_64_1_start_index: sn_64_1_end_index])
data_dict['Section 64(2)'] = ''.join(cleaned_fulltext_no_contents[sn_64_2_start_index: sn_64_2_end_index])
        
        
        
        
        
        
        
        
#     if line.startswith('9.2.1.'):
#         ohs_e_start_index = index+1
#     if line.startswith('9.2.2.'):
#          ohs_e_end_index = index-1
#          ph_e_start_index = index+1
#     if line.startswith('9.2.3.'):
#         ph_e_end_index = index-1
#         hh_e_start_index = index+1
#     if line.startswith('9.2.4.'):
#        hh_e_end_index = index-1
#        ohs_risk_start_index = index+1
#     if line.startswith('9.2.5.'):
#         ohs_risk_end_index = index-1
#         ph_risk_start_index = index+1
#     if line.startswith('10.'):
#         ph_risk_end_index = index-1
#     if line.startswith('10.1.'):
#         data_dict['Hazard classification'] = cleaned_fulltext_no_contents[index+1]
#     if line.startswith('12.1'):
#         sn_string_start_index = index+1
#     if line.startswith('13.'):
#         sn_string_end_index = index-1

# data_dict['SN Conditions'] = cleaned_fulltext_no_contents[sn_string_start_index:sn_string_end_index]
# data_dict['Occupational health and safety - exposure assessment'] = cleaned_fulltext_no_contents[ohs_e_start_index: ohs_e_end_index]
# data_dict['Public health - exposure assessment'] = cleaned_fulltext_no_contents[ph_e_start_index:ph_e_end_index]
# data_dict['Human health - affections assessment'] = cleaned_fulltext_no_contents[hh_e_start_index: hh_e_end_index]
# data_dict['Occupational health and safety - risk characterisation'] = cleaned_fulltext_no_contents[ohs_risk_start_index: ohs_risk_end_index]
# data_dict['Public health - risk assessment'] = cleaned_fulltext_no_contents[ph_risk_start_index:ph_risk_end_index]
        
        
print(data_dict)