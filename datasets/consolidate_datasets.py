#%%
import os
import numpy as np
import pandas as pd
from mat2vec.processing import MaterialsTextProcessor
mtp = MaterialsTextProcessor()

def mat2vec_process(f):
    return mtp.process(f)[0][0]

dataset_index = pd.read_csv('dataset_index.csv', index_col=0)

col_select = ['material_name', 'molecular_formula']
datasets = []

for source, row in dataset_index.iterrows():
    fp = os.path.join('.', row['path'])
    df = pd.read_csv(fp)
    col_select_present = [col for col in col_select if col in df.columns]
    df = df[col_select_present]

    df = df.drop_duplicates() #TODO: some have duplicates by year

    df['source'] = source

    datasets.append(df)

df = pd.concat(datasets).reset_index(drop=True)

df['material_name'] = df['material_name'].str.lower()
df['molecular_formula_norm'] = df['molecular_formula'].astype(str).apply(mat2vec_process)
df


#%%



pubchem_lookup = pd.read_csv(r'../mat_cost\pubchem_lookup.csv', index_col=0)

#TODO: lowercase original pubchem lookup
pubchem_lookup = pubchem_lookup.reset_index()
pubchem_lookup['index'] = pubchem_lookup['index'].str.lower()
pubchem_lookup = pubchem_lookup.drop_duplicates(subset=['index'])
pubchem_lookup = pubchem_lookup.set_index('index')

pubchem_lookup

#%%

pubchem_forms = pubchem_lookup['pubchem_top_formula'].astype(str).apply(mat2vec_process)
pubchem_forms = pubchem_forms.replace('nan', np.nan)
pubchem_forms

#%%

pubchem_forms.where(pubchem_forms.duplicated(False)).dropna()
#%%

def join_material_dups(df_dup, column):
    source_list = ", ".join(df_dup[column].dropna())
    return source_list


s_mat_sources = df.groupby('material_name').apply(join_material_dups, column='source')
s_mat_sources.name = 'source'

df_material = pd.concat([s_mat_sources, pubchem_forms.loc[s_mat_sources.index]], axis=1)
df_material.to_csv('material_sources.csv')

# s_mat_sources.to_csv('material_sources.csv')

#%%

# form_process = [mat2vec_process(f) for f in df_molecular.index]
# df_molecular['formula_processed'] = form_process

s_molecular_sources = df.groupby('molecular_formula_norm').apply(join_material_dups, column='source')
s_molecular_sources.name = 'source'
df_molecular = s_molecular_sources.to_frame()

df_molecular['material_names']= df.groupby('molecular_formula_norm').apply(join_material_dups, column='material_name')

df_molecular = df_molecular.drop('nan')

df_molecular.to_csv('molecular_sources.csv')

# s_molecular_sources.to_csv('molecular_sources.csv')

#%%
for idx, row in df_material.iterrows():
    f = row['pubchem_top_formula']
    if f != 'nan':
        if f in df['molecular_formula_norm'].dropna().values:
            print("{} : {}".format(idx, f))
# %%