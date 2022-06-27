#%%
import matplotlib.pyplot as plt
import seaborn as sns
import re
import os
from os.path import join as pjoin

from es_utils.units import read_pint_df
from es_utils.plot import annotate_points

import matplotlib as mpl
mpl.rcParams.update({'font.size':12})
from adjustText import adjust_text

from dotenv import load_dotenv
load_dotenv()
REPO_DIR = os.getenv('REPO_DIR')

output_dir = 'output'
if not os.path.exists(output_dir): os.makedirs(output_dir)

df = read_pint_df(pjoin(REPO_DIR,'cap_cost/data_consolidated/SM_data.csv'), index_col=[0,1], drop_units=True).reset_index('SM_type')

df.index = [re.sub('(\D)(\d)(\D|$)',r'\1_\2\3', s) for s in df.index] #Simple way to format chemical equations as latex. Assumes only time numbers are showing up. 

Ckwh_cutoff = 50
y_lim = (0.1, 100)
# %%


df_tc = df.where(df['SM_type'] == 'thermochemical').dropna(subset=['SM_type'])
df_tc = df_tc.dropna(axis=1,how='all')
df_tc = df_tc.where(df_tc['C_kwh'] < Ckwh_cutoff).dropna(how='all')

plt.figure(figsize=(7,8))
x_str='temperature'
y_str='C_kwh'

sns.scatterplot(data=df_tc, y=y_str, x=x_str, hue='sub_type', legend=True)

# df_tc.plot.scatter(y='C_kwh', x=x_str, sharex=False)


ax = plt.gca()

texts = annotate_points(df_tc, x_str,y_str, ax=ax)

plt.xlim(0,2000)
leg = plt.gca().get_legend()
leg.set_bbox_to_anchor([0,0,0.3,0.2])
leg.set_title('')

plt.yscale('log')
plt.ylim(y_lim)
# plt.ylim(0,10)

ax.hlines(10,0,2000, linestyle='--', color='gray')

plt.xlabel('Reaction Temperature (C)')
plt.ylabel("$C_{kWh,mat}$ (\$/kWh)")
plt.suptitle("Thermochemcial")
plt.tight_layout()

adjust_text(texts, arrowprops = dict(arrowstyle='->'), force_points=(0,5))

plt.savefig(pjoin(output_dir,'thermochem.png'))
# %%