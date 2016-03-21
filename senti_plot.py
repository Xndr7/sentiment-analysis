import matplotlib.pyplot as plots
import matplotlib.animation as anime
from matplotlib import style

style.use("ggplot")

fig = plots.figure()                                                      #init figure
ax1 = fig.add_subplot(1, 1, 1)                                          #init subplot


def animate(i):
    pull_data = open("twitter-out.txt", "r").read()                      #read sentiment values
    data = pull_data.split('\n')

    xar = []
    yar = []

    x = 0
    y = 0

    for l in data[-200:]:                                              #load recent sentiments
        x += 1
        if "pos" in l:
            y += 1                                                     #increment based on sentiment detected
        elif "neg" in l:
            y -= 1

        xar.append(x)
        yar.append(y)

    ax1.clear()
    ax1.plot(xar, yar)
ani = anime.FuncAnimation(fig, animate, interval=1000)
plots.show()