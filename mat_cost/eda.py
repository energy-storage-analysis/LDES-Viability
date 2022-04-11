
#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import seaborn as sns

mpl.rcParams.update({'font.size':13.5})

# %%


df_mat_data = pd.read_csv('data/mat_data.csv', index_col=0)
df_SMs = pd.read_csv('data/SM_data.csv', index_col=0)
df_all = pd.read_csv('data/C_kWh.csv', index_col=0)
# %%
plt.figure()

bins = np.logspace(np.log10(0.05), np.log10(2e3), 30)
df_mat_data['specific_price'].hist(bins=bins)

plt.xscale('log')

plt.suptitle("{} Material Prices".format(len(df_mat_data)))
plt.xlabel('Specific Price ($/kg)')

plt.locator_params(axis='y', integer=True)
plt.ylabel('Count')
plt.tight_layout()

plt.savefig('output_eda/mat_cost.png')


#%%

# plt.figure(figsize=(2,2))
plt.figure(figsize=(5,5))

df_mat_data['num_source'].value_counts().plot.bar()
plt.xlabel("# Sources")
plt.ylabel("Count")

plt.tight_layout()

plt.savefig('output_eda/source_count.png')

#%%

#These datapoints in SM dataset do not have data to calculate C_kwh, when dropping these it is the same length as df_all
missing_idx = [idx for idx in df_SMs.index if idx not in df_all.index.values]
len(missing_idx)

df_SMs.loc[missing_idx].dropna(how='all', axis=1).info()
#%%

df_SMs = df_SMs.drop(missing_idx)

#%%

plt.figure()

display_text = pd.read_csv('tech_lookup.csv', index_col=0)
bins = np.logspace(np.log10(1e-4), np.log10(1e2), 30)

df_all['energy_type'] = [display_text['energy_type'][s].replace('\\n','\n') for s in df_all['SM_type'].values]

df_all.groupby('energy_type')['specific_energy'].hist(bins=bins, legend=True, alpha=0.75)

plt.xscale('log')
plt.locator_params(axis='y', integer=True)
plt.suptitle("{} Storage Media".format(len(df_all)))
plt.xlabel('Energy Density (kWh/kg)')
plt.ylabel('Count')
plt.tight_layout()


plt.savefig('output_eda/SM_energy.png')

#%%

# df_all = df_all.dropna(subset=['C_kwh'])

#%%
#Has both price and energy data


df_both = df_all.dropna(subset = ['C_kwh'])

plt.figure()

bins = np.logspace(np.log10(1e-3), np.log10(1e6), 50)

df_both.groupby('energy_type')['C_kwh'].hist(bins=bins, legend=True, alpha=0.75)

plt.xscale('log')
plt.suptitle("{} Storage Media w/ Mat. Prices".format(len(df_both)))
plt.xlabel('Material Captial Cost ($/kWh)')
plt.ylabel('Count')

plt.gca().get_legend().remove()

plt.savefig('output_eda/SM_w_prices.png')
