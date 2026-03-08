import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('dane\\weight-height.csv', sep=';')
print(df)
print(df.head(3))
df.Height *= 2.54
df.Weight /= 2.2
print(df.describe())

plt.hist(df.Weight, bins=50)
plt.show()

plt.scatter(df.Weight, df.Height)
plt.show()