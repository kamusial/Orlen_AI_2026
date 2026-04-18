# Napisz program w Pythonie, który będzie analizował wyniki uczniów zapisane w liście.
wyniki = [45, 67, 80, 54, 90, 32, 76, 88, 59, 41]
print(f'Wszystkie wyniki z listy: {wyniki}')
print(f'Liczba wszystkich wyników {len(wyniki)}')
print(f'Suma punktów: {sum(wyniki)}')
print(f'Średnia punktów: {sum(wyniki) / len(wyniki)}')
print(f'Najwyższy wynik: {max(wyniki)}')
print(f'Najwyższy wynik: {min(wyniki)}')

zdalo = 0
nie_zdalo = 0
studenci_70plus = []

for wynik in wyniki:
    if wynik >= 50:
        zdalo += 1
    else:
       nie_zdalo += 1
    if wynik >= 70:
        studenci_70plus.append(wynik)
    if wynik < 50:
        print(f'{wynik}: Nie zdal')
    elif wynik <= 79:
        print(f'{wynik}: Zdal')
    else:
        print(f'{wynik}: Bardzo dobry wynik')
print(f'Zdało: {zdalo} osób')
print(f'Nie zdało: {nie_zdalo} osób')