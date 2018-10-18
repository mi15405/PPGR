import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def main():
    fig, ax = plt.subplots()
    #xdata, ydata = [], []

    x = np.linspace(0, 2*np.pi, 128)
    y = np.sin(x)

    ln, = ax.plot(x, y, 'r--', linewidth = 4, markersize = 3, animated=True)
    line, = ax.plot(x, y, 'go--', linewidth=2, markersize=2)
    time = 0

    def init():
        ax.set_xlim(0, 2*np.pi)
        ax.set_ylim(-1, 1)
        return ln,

    def animate(frame):
        '''
        xdata.append(frame)
        ydata.append(np.sin(frame))
        ln.set_data(xdata, ydata)
        '''
        ln.set_ydata(np.sin(x + frame/10.0))
        return ln,


    ani = animation.FuncAnimation(
            fig, animate, x, init_func=init, blit=True, interval = 30)

    plt.show()



if __name__ == '__main__':
    main()
