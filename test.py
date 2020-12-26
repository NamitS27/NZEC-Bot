import matplotlib.pyplot as plt

x = [2,4,6,8,10]
y = [1,3,5,7,9]

x1 = [1,3,5,7,9]
y2 = [2,4,6,8,10]

plt.plot(x,y)
plt.plot(x1,y2)
plt.savefig("test.png")