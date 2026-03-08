moja_lista = [1, 3, 5, 6, 5, 3]

for i in range(len(moja_lista)):
    if moja_lista[i] > 3:
        print(f'Element {moja_lista[i]} jest duży')
    else:
        print(f'Element {moja_lista[i]} jest maly')

for i in moja_lista:
    if i > 3:
        print(f'Element {i} jest duży')
    else:
        print(f'Element {i} jest maly')

