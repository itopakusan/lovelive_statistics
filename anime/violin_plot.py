import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams

if __name__ == '__main__':

    df = pd.read_csv('data.csv', index_col=0)
    df_color = pd.read_csv('color.csv')

    # Scale the unit from second to min.
    df = df/60

    # font setting
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['IPAexGothic',
                                   'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']

    sns.set_palette(df_color['Color'])

    fig, ax = plt.subplots(figsize=(8, 6))

    ax = sns.violinplot(data=df, color='0.7', inner='quartile')
    ax = sns.swarmplot(data=df)

    ax.set_title('会話時間比較')
    ax.set_xlabel('キャラクター')
    ax.set_ylabel('会話時間 (min)')
    ax.set_ylim([0, 10])
    fig.savefig('violinplot.svg')
    fig.savefig('violinplot.png', dpi=300)
