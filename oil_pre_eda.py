import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('nrg_cb_oilm_linear.csv')
df['TIME_PERIOD'] = [int(x[:4]) * 12 + int(x[5:]) - 1 for x in df['TIME_PERIOD']]
df.sort_values(['geo', 'nrg_bal', 'unit', 'TIME_PERIOD'], inplace=True)

tpmin, tpmax = df['TIME_PERIOD'].min(), df['TIME_PERIOD'].max()

for column in df.columns:
    uvs = df[column].unique()
    print(column, uvs, len(uvs))

print(df.shape[0])
for value in ['e', 'p', 'u']:
    print(df[df['OBS_FLAG'] == value].shape[0])

# many nrg_bal & siec values
# 38 geos
# 2 OBS_FLAG [nan 'p']

# predict siec = O4671, nrg_bal = GID_CAL, unit = THS_T

plt.hist(df['OBS_VALUE'], bins=1000)
plt.show()

geos = sorted(df['geo'].unique())
nrg_bals = sorted(df['nrg_bal'].unique())
siecs = sorted(df['siec'].unique())
for geo in geos:
    df_by_geo = df[df['geo'] == geo]
    for siec in siecs:
        fig, axs = plt.subplots(len(nrg_bals))
        fig.suptitle(f'{geo} {siec}')
        for i in range(len(nrg_bals)):
            nrg_bal = nrg_bals[i]
            filtered_df = df_by_geo[(df['nrg_bal'] == nrg_bal) & (df['siec'] == siec)]
            axs[i].set_title(nrg_bal)
            axs[i].set_xlim([tpmin, tpmax])
            axs[i].plot(filtered_df['TIME_PERIOD'], filtered_df['OBS_VALUE'], marker='.', ms=3, linewidth=1)
        plt.show()

# missing values may be zero
