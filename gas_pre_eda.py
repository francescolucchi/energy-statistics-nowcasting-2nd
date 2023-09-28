import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('nrg_cb_gasm_linear.csv')
df['TIME_PERIOD'] = [int(x[:4]) * 12 + int(x[5:]) - 1 for x in df['TIME_PERIOD']]
df.sort_values(['geo', 'nrg_bal', 'unit', 'TIME_PERIOD'], inplace=True)

tpmin, tpmax = df['TIME_PERIOD'].min(), df['TIME_PERIOD'].max()

for column in df.columns:
    uvs = df[column].unique()
    print(column, uvs, len(uvs))

print(df.shape[0])
for value in ['e', 'p', 'u']:
    print(df[df['OBS_FLAG'] == value].shape[0])

# 16 nrg_bal values
# 2 units
# 40 geos
# 6 OBS_FLAG [nan 'p' 'e' 'n' 'u' 'z']

# predict siec = G3000, nrg_bal = IC_CAL_MG, unit = TJ_GCV

plt.hist(df['OBS_VALUE'], bins=1000)
plt.show()

geos = sorted(df['geo'].unique())
nrg_bals = sorted(df['nrg_bal'].unique())
units = sorted(df['unit'].unique())
for geo in geos:
    df_by_geo = df[df['geo'] == geo]
    fig, axs = plt.subplots(len(nrg_bals), 2)
    fig.suptitle(geo)
    for j in range(len(units)):
        unit = units[j]
        for i in range(len(nrg_bals)):
            nrg_bal = nrg_bals[i]
            filtered_df = df_by_geo[(df['nrg_bal'] == nrg_bal) & (df['unit'] == unit)]
            axs[i, j].set_title(f'{nrg_bal} {unit}')
            axs[i, j].set_xlim([tpmin, tpmax])
            axs[i, j].plot(filtered_df['TIME_PERIOD'], filtered_df['OBS_VALUE'], marker='.', ms=3, linewidth=1)
    plt.show()

# missing values may be zero
