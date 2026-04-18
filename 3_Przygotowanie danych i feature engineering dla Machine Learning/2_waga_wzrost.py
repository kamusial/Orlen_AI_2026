import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('dane\\weight-height.csv', sep=';')
print(type(df))
print(df)

print(f'Wartosci w gender:\n{df.Gender.value_counts()}')

df.Height *= 2.54
# df.Height = df.Height * 2.54
df.Weight /= 2.2
print('Po zmianie wartości:')
print(df)

plt.hist(df.query("Gender=='Male'").Weight, bins=30)
plt.hist(df.query("Gender=='Female'").Weight, bins=30)
plt.show()

# sns.histplot - niedziela

print('Descibe:')
print(df.describe())

df = pd.get_dummies(df)   # usunięcie danych nienumerycznych
del (df['Gender_Male'])
df = df.rename(columns={'Gender_Female': 'Gender'})
print(df)

from sklearn.linear_model import LinearRegression
model = LinearRegression()
model.fit(df[['Height','Gender']], df['Weight'])
print(f'Wspolczynnik kierunkowy: {model.coef_}')
print(f'wyraz wolny: {model.intercept_}')

print(f'waga = wzrost * 1.06960294 + plec * -8.80805024 -102.52081454490131')
print(model.predict([[192, 0], [192, 1], [160, 1], [100, 1]]))
