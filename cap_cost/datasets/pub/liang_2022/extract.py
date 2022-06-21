"""
This script is designed to extract data from pdfs using a template generated by the tabula web interface. The actual extraction happens with the camelot python package
"""

#%%
import os
import pandas as pd
import json
import es_utils
from dotenv import load_dotenv
load_dotenv()


#PDF location info
pdf_folder = os.getenv('PDF_FOLDER_PATH')
pdf_fn =  r"Liang et al_2022_Key components for Carnot Battery.pdf"
pdf_path = os.path.join(pdf_folder,pdf_fn)

#This is the default 'flavor' for the table extraction (lattice = table has lines, stream = opposite)
DEFAULT_FLAVOR = 'stream'

template_path = 'tabula_template.json'
with open(template_path, 'r') as f:
    templates= json.load(f)

#If extraction settings don't exist make a blank dictionary
if not os.path.exists('extract_settings.json'):
    dummy_settings = [{}]*len(templates)
    with open('extract_settings.json', 'w') as f:
        json.dump(dummy_settings,f)

template_path = 'extract_settings.json'
with open(template_path, 'r') as f:
    extract_settings= json.load(f)

for i in range(len(extract_settings)):
    extract_settings[i]['template'] = templates[i]

    if 'camelot_kwargs' not in extract_settings[i]: extract_settings[i]['camelot_kwargs'] = {}
    extract_settings[i]['camelot_kwargs'].update({'flavor': DEFAULT_FLAVOR})
#%%

dfs = es_utils.pdf.extract_dfs(pdf_path, extract_settings)
#%%

#Setup table dictionary and do any processing here. 

tables = {}

#TODO: need to specifiy columns of continued table part for table 1 to be formed correctly 
# dfs[1].columns = dfs[0].columns
# tables['table_1'] = pd.concat([dfs[0], dfs[1]])
tables['table_A1'] = dfs[2]

dfs[4].columns = dfs[3].columns
tables['table_A2'] = pd.concat([dfs[3], dfs[4]])
tables['table_A3'] = dfs[5]

# tables = {'table_{}'.format(i+1): dfs[i] for i in range(len(dfs))}

#%%

dash_characters = ['\u2013','\u2212', '(cid:0) ']

for table in tables:
    for dash_character in dash_characters:
        # tables[table].columns = [c.strip().replace(dash_character,'-') for c in tables[table].columns]
        for column in tables[table].columns:
            tables[table][column] = tables[table][column].str.replace(dash_character,'-', regex=False)

# %%

output_folder = 'tables'
if not os.path.exists(output_folder): os.mkdir(output_folder)

for fn in os.listdir(output_folder):
    os.remove(os.path.join(output_folder, fn))

for table in tables:
    tables[table].to_csv('{}/{}.csv'.format(output_folder, table), index=False)
# %%
