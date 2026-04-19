import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('dane\\otodom.csv')
print(df)
print(df.describe().T.round(2).to_string())

sns.heatmap(df.iloc[:,1:].corr(), annot=True)
plt.show()

sns.histplot(df.cena)
plt.show()

plt.scatter(df.powierzchnia, df.cena)
plt.show()