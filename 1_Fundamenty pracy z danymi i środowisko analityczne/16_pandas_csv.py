import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('rozliczenie.csv')
print(df)
# df['wyplata'] = df['wyplata'] * 0.22
df['wyplata w Euro'] = df['wyplata'] * 0.22
del df['czy na macie']

print(df.head())
print(df.describe())



# print(f'Histogram')
# plt.hist(df.wyplata)
# plt.show()
#
# print(f'Wykres punktowy')
# plt.scatter(df.wyplata, df['liczba dni urlopu'])
# plt.show()

print("Wykres słupkowy")
imiona = ['Kamil', 'Gabrysia', 'Igor', 'Tomek', 'Kacper', 'Maciek']
punkty = [8, 12, 3, 21, 4, 23]
plt.bar(imiona, punkty, color=['green', 'blue', 'red'])
plt.xticks(imiona)
plt.yticks(punkty)
plt.xlabel('imiona')
plt.ylabel('punkty')
plt.show()

print('\nWykres kołowy')
wydatki = ['mieszkanie',  'media', 'jedzenie', 'rozrywka', 'nauka', 'inwestycje']
wartosci = [3000, 300, 800, 200, 400, 1000]
wysun = [0 for i in wydatki]
wysun[2] = 0.3

plt.pie(wartosci, labels=wydatki, explode=wysun, shadow=True)
plt.show()