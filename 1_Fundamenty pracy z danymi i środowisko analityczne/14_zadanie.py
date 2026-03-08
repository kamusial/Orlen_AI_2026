current_passwd = 'piesek'
counter = 0
while True:
    user_passwd = input('Wpisz haslo:   ')
    counter += 1
    if user_passwd == current_passwd:
        break
    else:
        print('Zle haslo')
        if counter < 3:
            print('Jeszcze raz')
        else:
            print('Wykorzystales 3 proby. Koniec')
            quit()
print('Idziemy dalej')
