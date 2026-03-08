# program ma listę rzeczyw domu
# program pyta ile rzeczy chcemy kuić
# program pyta o rzeczy do kupienia i mówi, czy mamy czy nie

w_domu = ['marchew', 'pomidor', 'koperek', 'drukarka']

decyzja = input('Czy chcesz sprawdzic produkt?  t/n')
while decyzja == 't':
    produkt = input('Co chcesz kupić?  ')
    if produkt in w_domu:
        print(f'{produkt}: nie kupuj')
    else:
        print(f'{produkt}: kup')
    decyzja = input('Czy chcesz sprawdzic produkt?  t/n')
print('koniec')
