import pandas as pd

df = pd.read_csv('dane/weight-height.csv', sep=';')


df.Height *= 2.54
df.Weight /= 2.2
print(df)
print(f'Kształt danych {df.shape}')
print('\nDescribe')
print(df.describe().T.to_string())

print(f'\nZliczanie wartości kolumny Gender:\n{df.Gender.value_counts()}')

import matplotlib.pyplot as plt
import seaborn as sns

# plt.hist(df.query("Gender=='Male'").Weight)
# plt.hist(df.query("Gender=='Female'").Weight)
# plt.show()
#
# sns.histplot(df.query("Gender=='Male'").Weight)
# sns.histplot(df.query("Gender=='Female'").Weight)
# plt.show()

df = pd.get_dummies(df)
print(df)
# usunięcie kolumny "Gender_Male"
del (df['Gender_Male'])

# zmiana nazwy kolumny
df = df.rename(columns={'Gender_Female': 'Gender'})
# False - Facet, True - Kobieta
print(df)