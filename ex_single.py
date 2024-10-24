from PyPDF2 import PdfReader


path = "reports/NC_reports_for_analysis/STD1491.pdf"

def get_text(file):
    reader = PdfReader(file)
    fulltext = ''
    for page in reader.pages:
        fulltext += page.extract_text()
    fulltext = fulltext.split('\n')
    cleaned_fulltext = list(
        filter(None, [string.strip() for string in fulltext]))
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
        dict = {"SECTION 64(1)": (''.join(text[indices['s1']:indices['end']]))}
    if (indices['s2']!= None) and (indices['s1'] == None):
        dict = {"SECTION 64(2)": text[indices['s2']:indices['end']]}
    if indices['s1'] and indices['s2'] != None:
        dict = {"SECTION 64(1)": (''.join(text[indices['s1']:(indices['s2'])])),
                "SECTION 64(2)": (''.join(text[indices['s2']:indices['end']]))}
    return dict  
    


data_dict = {
    
}
text = get_text(path)
print(text)
data_dict.update(get_sn_conditions(text))
print(data_dict)


