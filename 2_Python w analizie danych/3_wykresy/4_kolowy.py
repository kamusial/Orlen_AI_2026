import matplotlib.pyplot as plt

wydatki = ['mieszkanie', 'media', 'rozrywka', 'nauka', 'pokemony']
values = [2000, 400, 120, 700, 1230]

wyciagnij = [0 for i in wydatki]
wyciagnij[2] = 0.3
wyciagnij[4] = 0.7


plt.pie(values, labels=wydatki, explode=wyciagnij)
plt.show()