# 1. Oczyt pliku csv z zapisem poszczególnych pól

with open('rozliczenie.csv', 'r') as plik_rozliczenie:
    content = plik_rozliczenie.readlines()

print(content[4])
print(type(content))

for i in range(len(content)):
    content[i] = content[i].split(',')

print(content)
print(content[3])
print(content[3][2])

# 2. Obliczanie średniej wypłaty
total = 0
for i in range(1, len(content)):
    print(f'wyplata: {content[i][1]}')
    total += float(content[i][1])
print(f'Suma wyplat: {total}')
print(f'Średnia wypłata: {   round   (total / (len(content) - 1),   2)   }')

# 3. Ile kobiet na macierzynskim
total = 0
for i in range(1, len(content)):
    print(f'czy na macierzynskim: {content[i][4]}')

