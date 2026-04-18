import matplotlib.pyplot as plt

# funkcja 1: y = 5x - 2 ; funkcja 2: y = -2x + 5 ; funkcja 3: y = 3x + 3

X = []
for i in range(-10, 10):
    X.append(i)

y1 = []
for i in X:
    y1.append(5 * i - 2)

y2 = []
for i in X:
    y2.append(-2 * i + 5)

y3 = []
for i in X:
    y3.append(3 * i + 3)

print(X)
print(y1)
print(y2)
print(y3)

plt.axhline() # linia pozioma osi
plt.axvline() # linia pionowa osi
plt.plot(X, y1, 'ro-')
plt.plot(X, y2, 'b^-')
plt.plot(X, y3, 'gs-')
plt.xlabel("punkty x") # opis osi X
plt.ylabel("wartosci y") # opis osi Y
plt.title("Wykresy funkcji") # tytuł wykresu
plt.show()