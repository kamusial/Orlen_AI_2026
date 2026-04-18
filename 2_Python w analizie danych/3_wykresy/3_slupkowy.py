import matplotlib.pyplot as plt
import random

names = ['Ala', 'Ola', 'Kamil', 'Anita', 'Kasia']
points = [4, 6, 7, 4, 1]

plt.bar(names, points, color=['red', 'green', 'yellow'])
plt.xticks(names)
plt.yticks(points)
plt.show()