import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib import rcParams

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['IPAexGothic']
cmap = plt.get_cmap("tab10")

# Load CSV files
df = pd.read_csv('data.csv', index_col='Date',
                 parse_dates=True)
ch = pd.read_csv('channel.csv')

channels = df['Channel'].unique()

# prefecenes for general plot setting
plt.style.use('ggplot')
fig = plt.figure(figsize=(8.0, 6.0))
ax = fig.add_subplot(111)

dates = mdates.MonthLocator(interval=6)
dates_fmt = mdates.DateFormatter('%Y/%m')

ax.xaxis.set_major_locator(dates)
ax.xaxis.set_major_formatter(dates_fmt)

for channel in channels:

    df_tmp = df[df['Channel'] == channel]
    df_tmp = df_tmp.sort_index()
    df_tmp['Duration'] = df_tmp['Duration'].cumsum()

    df_param = ch.loc[(ch['Channel'] == channel)]
    label = df_param.iat[0, 1]
    color = df_param.iat[0, 2]

    ax.scatter(df_tmp.index, df_tmp['Duration'], color=cmap(
        color), zorder=5, alpha=0.5, edgecolors='none', label=label)

ax.legend()

plt.title("累計放送時間")
plt.xlabel("放送日時")
plt.ylabel("累積放送時間 (時間)")
plt.savefig("scatter.svg", format="svg")
plt.savefig("scatter.png", format="png", dpi=300)
