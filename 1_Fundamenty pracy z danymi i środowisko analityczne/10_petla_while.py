liczba_prob = 0
liczba_do_zgadniecia = 7
while liczba_prob < 3:
    liczba_uzytkownika = int(input('Podaj liczbe '))
    if liczba_uzytkownika != liczba_do_zgadniecia:
        print('Nie zgadles')
        liczba_prob = liczba_prob + 1
    else:
        print('zgadles')
        liczba_prob = 3
print('koniec')


