import pandas as pd
from pandas.core.indexes.datetimes import date_range
import requests
import os
import glob
import matplotlib.dates as mdates
import matplotlib.pyplot as plt


class openrec_data_collection():

    def __init__(self):

        self.movie_list = pd.DataFrame()
        self.csv_directory = 'yell_collection/'

    def import_movie_list(self, path):

        dataframe = pd.read_csv(path)
        self.movie_list = dataframe

    def get_yell_list(self, movie_id):

        i = 1
        url = 'https://public.openrec.tv/external/api/v5/yell-logs?movie_id=' + movie_id + '&page='
        page = str(i)

        print(url + page)
        response = requests.get(url + page)
        dataframe = pd.DataFrame.from_dict(response.json())
        if dataframe.empty:
            return dataframe

        dataframe = pd.concat(
            [dataframe, pd.json_normalize(dataframe['yell']), pd.json_normalize(dataframe['user'])], axis=1)

        while len(response.json()) != 0:

            i += 1
            page = str(i)
            print(url + page)
            response = requests.get(url + page)

            if len(response.json()) != 0:

                dataframe_i = pd.DataFrame.from_dict(response.json())
                dataframe_i = pd.concat(
                    [dataframe_i, pd.json_normalize(dataframe_i['yell']), pd.json_normalize(dataframe_i['user'])], axis=1)
                dataframe = pd.concat([dataframe, dataframe_i])

        dataframe['movie_id'] = movie_id

        return dataframe

    def get_title(self, movie_id):
        # Doesn't work here!!! why????????

        url = 'https://public.openrec.tv/external/api/v5/movies/' + movie_id

        response = requests.get(url)
        pd.DataFrame.from_dict(response.json())

    def save_yell_as_csv(self):

        for movie in self.movie_list['Movie']:

            filename = self.csv_directory + movie + '.csv'

            if os.path.isfile(filename):
                continue
            else:
                dataframe = self.get_yell_list(movie)
                if not dataframe.empty:
                    dataframe.to_csv(filename, mode='w', header=True)

    def collect_all_yells(self):

        files = glob.glob(self.csv_directory + '*.csv')
        dataframe = pd.DataFrame()

        for file in files:

            if dataframe.empty:
                dataframe = pd.read_csv(file)
            else:
                dataframe = pd.concat(
                    [dataframe, pd.read_csv(file)])

        dataframe['date'] = dataframe['created_at'].str.extract('(.+)T')
        dataframe['date'] = pd.to_datetime(dataframe['date'])
        dataframe = dataframe.drop(
            columns=['created_at', 'yell', 'user', 'to_user', 'chat_setting', 'badges'])
        dataframe = dataframe.dropna(how='all', axis=1)

        return dataframe

    def visualization(self, dataframe):

        dataframe = dataframe[['date', 'yells']]
        dataframe = dataframe.sort_values('date')
        dataframe = dataframe.set_index('date')
        dataframe = dataframe.resample('D').sum()
        dataframe['cum_yells'] = dataframe['yells'].cumsum()

        plt.style.use('ggplot')
        fig = plt.figure(figsize=(8.0, 6.0))
        ax = fig.add_subplot(111)

        ydates = mdates.MonthLocator(interval=3)
        mtdates = mdates.MonthLocator()
        dates_fmt = mdates.DateFormatter('%y/%m')

        ax.xaxis.set_major_locator(ydates)
        ax.xaxis.set_major_formatter(dates_fmt)

        ax.xaxis.set_minor_locator(mtdates)

        ax.scatter(dataframe.index, dataframe['cum_yells'])

        ax.ticklabel_format(style='plain', axis='y')
        ax.set_title('Total Amount of Yell')
        ax.set_xlabel('Date')
        ax.set_ylabel("Mayuchi's salary (Yen)")
        ax.yaxis.set_major_formatter(plt.FuncFormatter(
            lambda x, loc: "{:,}".format(int(x))))
        fig.tight_layout()
        fig.savefig('scatter.svg')
        fig.savefig('scatter.png', dpi=300)

    def distribution(self, dataframe):

        dataframe = dataframe[['date', 'yells']]
        dataframe = dataframe.sort_values('date')
        dataframe = dataframe.set_index('date')

        plt.style.use('ggplot')
        fig = plt.figure(figsize=(8.0, 6.0))
        ax = fig.add_subplot(111)

        ax.hist(dataframe['yells'], bins=50, range=(0, 10000))

        ax.set_title('Histgram')
        ax.set_xlabel('Amount of yell (Yen)')
        ax.set_ylabel("The number of event")
        ax.xaxis.set_major_formatter(plt.FuncFormatter(
            lambda x, loc: "{:,}".format(int(x))))
        ax.yaxis.set_major_formatter(plt.FuncFormatter(
            lambda x, loc: "{:,}".format(int(x))))

        fig.tight_layout()
        fig.savefig('histgram.svg')
        fig.savefig('histgram.png', dpi=300)


if __name__ == '__main__':

    yell = openrec_data_collection()
    yell.import_movie_list('movie_list.csv')
    yell.save_yell_as_csv()

    dataframe = yell.collect_all_yells()
    dataframe.to_csv('yell_collection.csv')

    yell.visualization(dataframe)
    yell.distribution(dataframe)
