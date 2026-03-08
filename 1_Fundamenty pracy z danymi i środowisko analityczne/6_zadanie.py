w_domu = ['makaron', 'mydlo', 'mleko', 'krem']

przedmioty = ['krem', 'losos']
for i in range (len(przedmioty)):
    if przedmioty[i] in w_domu:
        print(przedmioty[i],'masz to')
        print(f'Masz w domu: {przedmioty[i]}, nie kupuj')
        print('Masz w domu: {przedmioty[i]}, nie kupuj')
    else:
        print(przedmioty[i],'kup to')





# program mówi, czy mam przedmiot w domu
