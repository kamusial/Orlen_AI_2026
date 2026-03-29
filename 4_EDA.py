import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

#df = pd.read_csv('dane_csv.csv', delimiter=None, header='infer', index_col=None, usecols=None, dtype=None, true_values=['T', 'Tak'], false_values=['N', 'Nie'], skipinitialspace=True, skiprows=2, nrows=None, na_filter=True, skip_blank_lines=True, dayfirst=True,thousands=None, decimal=',', quetechar="", doublequote=True, comment='#', encoding=None, encoding_errors='strict', on_bad_lines='error', float_precision=None)

url="https://raw.githubusercontent.com/rfordatascience/tidytuesday/master/data/2020/2020-03-31/beers.csv"

try:
    df=pd.read_csv(url)
    print('Dane pobrane')
except Exception as e:
    print(f'Błąd {e}')
    print('Używam danych zapasowych')
    data = {
        'nazwa': ['IPA', 'IPA', 'Lager', 'Stout', 'Pilsner', 'Wheat', 'Porter', 'Ale', 'Bock'],
        'alkohol': [6.5, 6.5, 5.0, 7.2, 4.8, 5.2, 5.8, 5.5, 6.8],
        'goryczka': [65, 65, np.nan, 45, 30, 15, 40, 35, 25],
        'ocena': [4.2, 4.2, 3.8, 4.5, 3.9, 3.7, 4.1, 4.0, 4.3],
        'styl': ['IPA', 'IPA', 'Lager', 'Ciemne', 'Lager', np.nan, 'Ciemne', 'Jasne', 'Ciemne']
    }
    df = pd.DataFrame(data)