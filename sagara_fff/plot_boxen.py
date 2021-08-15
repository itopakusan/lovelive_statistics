import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from matplotlib import rcParams
import seaborn as sns

rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['IPAexGothic']

# Load CSV files
df = pd.read_csv('data.csv', index_col='Date',
                 parse_dates=True)
ch = pd.read_csv('channel.csv')

df = df.merge(ch, on='Channel')

plt.style.use('ggplot')
fig = plt.figure(figsize=(8.0, 8.0))
fig.subplots_adjust(left=0.4)
ax = fig.add_subplot(111)

ax = sns.boxenplot(y=df['Name'], x=df['Duration'],
                   orient='h', linewidth=0.5)

plt.ylabel(None)
plt.xlabel("各回放送時間（時間）")
plt.savefig("300_dpi_boxenplot.png", format="png", dpi=300)
