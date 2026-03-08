# 1. Program sprawdza wprowadzone hasło
# użytkownik ma 3 próby

main_passwd = 'piesek123'
passwd = input('Podaj haslo:  ')
licznik = 3

while passwd != main_passwd and licznik > 1:
    print('zle haslo, jeszcze raz')
    licznik = licznik - 1
    passwd = input('Podaj haslo:  ')

print('dalej')

# 2.
# dana jest lista pomiarów.
# program sprawdza i informuje ile pomiarów jest błędnych.
# prawidłowy pomiar 15 - 30
pomiary = [3.5, 16, 17.5, 24, 27.354, 19, 32, 35, 21]
za_male = 0
za_duze = 0
for pomiar in pomiary:
    if pomiar > 30:
        za_duze += 1
    elif pomiar < 15:
        za_male += 1
print(f'Liczba dobrych pomiarow: {len(pomiary) - za_male - za_duze}')

