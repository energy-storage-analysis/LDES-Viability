#%%
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import matplotlib as mpl

plt.rcParams.update({
    # "figure.facecolor":  (1.0, 0.0, 0.0, 0.3),  # red   with alpha = 30%
    # "axes.facecolor":    (0.0, 1.0, 0.0, 0.5),  # green with alpha = 50%
    "savefig.facecolor": 'white',
    "font.size": 14
})
# %%

def calc_lcos(DD, CF, C_Ein, eta, C_kW, C_kWh, LT):
    elec_premium = C_Ein*((1/eta)-1)

    capital_term_dem = C_kW + C_kWh*DD
    capital_term_num = LT*8760*CF*eta 
    capital_term = capital_term_dem/capital_term_num

    lcos= elec_premium + capital_term
    return lcos



#%%

DD = np.logspace(np.log2(1),np.log2(1024), base=2, num=500)
num_cycles_year = np.logspace(np.log10(1),np.log10(10000), base=10, num=500)

DD_2d, ncy_2d = np.meshgrid(DD, num_cycles_year)

CF_2d = ncy_2d*(DD_2d/8760)
CF_2d

import xarray as xr

da_CF = xr.DataArray(CF_2d, coords={'DD':DD, 'ncy':num_cycles_year}, dims=['DD','ncy'])
da_CF.coords['DD'].attrs = dict(long_name='Discharge Duration', units='h')
da_CF.coords['ncy'].attrs = dict(long_name='Num. Cyc. Year')

da_CF = da_CF.where(da_CF <= 1)

da_CF

#%%
plt.figure()

da_CF.plot(norm=mpl.colors.LogNorm())
plt.xscale('log')
plt.yscale('log')

plt.suptitle('Capacity Factor')

plt.savefig('output/CF_2D_fig.png')

#%%

C_Ein = 0.05
eta = 0.8
C_kW = 100
C_kWh = 50
LT = 20

da_lcos = calc_lcos(da_CF.coords['DD'], da_CF, C_Ein=C_Ein, eta=eta, C_kW=C_kW, C_kWh=C_kWh, LT=LT)
da_lcos
# %%
plt.figure()

da_lcos.plot(norm=mpl.colors.LogNorm())
plt.xscale('log')
plt.yscale('log')

plt.suptitle('LCOS ($/kWh)')

plt.savefig('output/LCOS_2D_CF_fig.png')
# %%
plt.figure()
CFs = np.linspace(0.1,1,5)

for CF in CFs:
    lcos_CF1 = calc_lcos(DD, CF=CF, C_Ein=C_Ein, eta=eta, C_kW=C_kW, C_kWh=C_kWh, LT=LT)
    plt.plot(DD,lcos_CF1, label=str(CF))

plt.legend(title='Capacity Factor')

plt.xscale('log')
plt.yscale('log')

plt.ylim(0.01,5)

plt.xlabel('Discharge Duration')
plt.ylabel('LCOS ($/kWh)')

plt.savefig('output/LCOS_CF_fig.png')



#%%

plt.figure()
DDs = np.logspace(np.log10(1), np.log10(300), 5)

DDs = [round(n,3) for n in DDs] #TODO

C_kWh = np.logspace(np.log10(1), np.log10(1000), num=500)
LCOS_set = 0.05
DD_set = 10
PE = 0.05
for DD_set in DDs:
    C_kW = LT*8760*eta*( LCOS_set - ( (1/eta)-1 )*PE ) - C_kWh*DD_set

    plt.plot(C_kWh, C_kW, label=DD_set)
    plt.xscale('log')
    plt.yscale('log')


plt.legend(title='Discharge Duration')
plt.xlabel('Energy Capital Cost ($/kWh)')
plt.ylabel('Power Capital Cost ($/kW)')

plt.savefig('output/EP_capitaltradeoff.png')
# %%

plt.figure()

C_kW_set = 100
C_kWh = np.logspace(np.log10(1), np.log10(1000))

DD = ( LT*8760*eta*( LCOS_set - ( (1/eta)-1 )*PE ) - C_kW_set)/C_kWh

plt.plot(C_kWh, DD)
plt.xscale('log')
plt.yscale('log')