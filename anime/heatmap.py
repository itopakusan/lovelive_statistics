import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams

if __name__ == '__main__':

    df = pd.read_csv('data.csv', index_col=0)

    # Scale the unit from second to min.
    df = df/60

    # font setting
    rcParams['font.family'] = 'sans-serif'
    rcParams['font.sans-serif'] = ['IPAexGothic',
                                   'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']

    plt.figure()

    ax = sns.heatmap(df.T, square=True, cmap='viridis',
                     cbar_kws={'label': '会話時間 (min)'})
    ax.set(xlabel='話', ylabel='キャラクター')

    plt.savefig('heatmap.svg', bbox_inches="tight")
    plt.savefig('heatmap.png', dpi=300, bbox_inches="tight")

    ax = sns.clustermap(df.T, metric='correlation', cmap='viridis',
                        z_score=0, cbar_kws={'label': 'Raw Z-score'})

    plt.savefig('clustermap.svg', bbox_inches="tight")
    plt.savefig('clustermap.png', dpi=300, bbox_inches="tight")
