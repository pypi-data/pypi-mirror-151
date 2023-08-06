import pandas as pd

from .info import pth_clean

params_avg = pd.read_csv(pth_clean / "table5.csv", sep=";", comment="#", index_col=['name'])
params_avg.loc['t_mbc', 'mean'] = 25  # [°C] from text just above fig1

params = pd.read_csv(pth_clean / "table8.csv", sep=";", comment="#", index_col=['cultivar'])
cmap = {
    'brin_cc': 'c_c',
    'brin_gc': 'g_c',
}
params = params[cmap.keys()].rename(columns=cmap)
params['q_10c'] = 2.17  # [?] from text just below fig3
params['t_0bc'] = 5  # [°C] from text just below fig3
params['t_mbc'] = 25  # [°C] from text just above fig1

params.loc['mean'] = params_avg['mean']
