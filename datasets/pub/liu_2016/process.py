
#%%
import pandas as pd
import os

if not os.path.exists('output'): os.mkdir('output')

df = pd.read_csv('tables/table_4.csv', index_col=0)

df = df.rename({
    'Cost/kg ($US/kg)': 'specific_price',
    'name': 'original_name',
    'Material': 'material_type'
}, axis=1)


df = df.set_index('original_name', drop=True)
df['material_type'] = df['material_type'].ffill()



df
#%%
from es_utils.chem import process_chem_lookup

chem_lookup = pd.read_csv('chem_lookup.csv')
chem_lookup = process_chem_lookup(chem_lookup)
df = pd.merge(df, chem_lookup, on='original_name').set_index('index')
#%%
df

from es_utils import extract_df_price
df_price = extract_df_price(df)
df_price.to_csv('output/mat_prices.csv')

