import pandas as pd
from pandas.core.indexes.datetimes import date_range
import requests
import os
import glob
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import openrec_yell as oy

if __name__ == '__main__':

    yell = oy.openrec_data_collection()
