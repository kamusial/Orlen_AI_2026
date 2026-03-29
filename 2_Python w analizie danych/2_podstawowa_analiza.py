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

from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(df[['Height','Gender']]     ,     df.Weight)
print(f'Współczynnik kierunkowy: {model.coef_}\nWyraz wolny: {model.intercept_}')
print(f'Weight = Height * {model.coef_[0]} + Gender * {model.coef_[1]} + {model.intercept_}')

print(f'Facet, 160cm wzrostu waży: {model.predict([[160, 0]])}')
print(f'Kobieta, 160cm wzrostu waży: {model.predict([[160, 1]])}')
print(f'Kobieta, 200cm wzrostu waży: {model.predict([[200, 1]])}')
print(f'Facet, 100cm wzrostu waży: {model.predict([[100, 0]])}')
print(f'Kobieta, 100cm wzrostu waży: {model.predict([[100, 1]])}')


